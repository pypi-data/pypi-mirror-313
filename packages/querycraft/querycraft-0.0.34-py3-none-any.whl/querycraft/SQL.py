#!/usr/bin/env python3

import re  # https://regex101.com/
from pprint import pprint

from sqlglot import parse_one, exp
from sqlglot.expressions import From, Where, Group, Having, Limit, Offset, Order, Select, Join, Subquery, Table

from querycraft.tools import bold_substring,df_similaire,delEntete
from querycraft.Database import *
from querycraft.SQLException import *

# ======================================================================================================================
# ======================================================================================================================


# ======================================================================================================================
# ======================================================================================================================

class SQL(object):
    def __init__(self, db=None, dbtype=None, str=None, name=None, debug=False, verbose=False):
        self.debug = debug
        self.verbose = verbose
        self.group_by = None
        if db is not None:
            self.__db = Database.get(db, dbtype, debug,verbose)
        else:
            self.__db = None
        self.select = None
        self.distinct = None
        self.from_all = None
        self.from_join = None
        self.where = None
        self.group = None
        self.having = None
        self.order = None
        self.limit = None
        self.offset = None
        self.sqlTables = []
        if str is not None:
            if name is not None:
                self.name = name
            else:
                self.name = str
            self.setSQL(str)
        else:
            self.name = name
            self.__str = None
            self.__data = None
            self.__pl_data = None
            self.__col_names = None

    def setDebug(self):
        self.debug = True

    def unsetDebug(self):
        self.debug = False

    def setVerbose(self):
        self.verbose = True

    def unsetVerbose(self):
        self.verbose = False
    def setSQLTables(self, sqltbl):
        """
        Permet de positionner les tables et les alias d'une requête, sans l'analyser.
        :param sqltbl: La liste des tables et alias de la requête.
        :return:
        """
        self.sqlTables = sqltbl

    def printDBTables(self):
        self.__db.printDBTables()

    def load(self, file):
        """
        Charge une requête SQL depuis le fichier.
        :param file: Le fichier contenant la requête SQL.
        """
        if not existFile(file):
            raise SQLException("Le fichier n'existe pas.")
        else:
            txt = ""
            with open(file, 'r') as f:
                txt += f.read()
            self.setSQL(txt)

    def setSQL(self, req):
        self.__str = re.sub('\s+', ' ', req)
        if self.name is None: self.name = req
        self.execute()

    def similaire(self, sql2) -> int:
        return df_similaire(self.getPLTable(), sql2.getPLTable())

    def __str__(self) -> str:
        if self.__str is not None:
            return self.__str
        else:
            return 'Requête SQL absente.'

    def traite_doublons(self, description):
        # détection des colonnes avec même nom. Si c'est le cas, préfixage par nom de table.
        for (i, c) in enumerate(self.__col_names):
            # print(c)
            unique = True
            for j in range(i + 1, len(self.__col_names)):
                a = description[j].name
                if a == c:
                    id = description[j].table_oid
                    t = self.__db.dbPGID[id]
                    self.__col_names[j] = f"{self.getAlias(t)}.{c}"
                    unique = False
            if not unique:
                id = description[i].table_oid
                t = self.__db.dbPGID[id]
                self.__col_names[i] = f"{self.getAlias(t)}.{c}"

    def getAlias(self, t):
        """
        Retourne l'alias de la table t.
        :param t: La table.
        :return: L'alias de la table.
        """
        for alias in self.sqlTables:
            if alias[0] == t:
                if alias[1] is not None:
                    return alias[1]
                else:
                    return t
        return t

    def __addPrefix(self, att):
        if '.' not in att:
            if att in self.__db.dbAttributs:
                # if x in [y for (y, z) in self.sqlTables]
                lt = [x for x in self.__db.dbAttributs[att]]
                if lt:
                    return self.getAlias(lt[0]) + '.' + att
                else:
                    return att
            else:
                return att
        else:
            return att

    def pgsql_nommer(self, att):
        if att.table_oid:
            t = self.__db.dbPGID[att.table_oid]
            nom_att = f"{self.getAlias(t)}.{att.name}"
        else:
            nom_att = self.__addPrefix(att.name)
        return nom_att

    def execute(self):
        """
        Exécute la requête
        :return:
        """
        if self.__str is None:
            raise SQLException("La requête n'est pas renseignée.")
        elif self.__db is None:
            raise SQLException("La base de donnée n'est pas renseignée.")
        elif self.__str == "":
            raise SQLException("La requête est vide.")
        else:
            if self.debug: print('Exécution de la requête : ', self.__str)
            (description, self.__data) = self.__db.execute(self.__str)
            if self.__db.getType() == 'pgsql':
                self.__col_names = [self.pgsql_nommer(att) for att in description]
            else:  # MySQL ou SQLite où on ne peut pas identifier les tables de tuples !
                self.__col_names = [self.__addPrefix(des[0]) for des in description]
                # print(self.__col_names)
                for (i, t) in enumerate(self.__data):
                    self.__data[i] = list(t)
                ## détection des colonnes avec même nom. Si c'est le cas, suppression de la colonne en double.
                toDelete = list()
                for (i, c) in enumerate(self.__col_names):
                    unique = True
                    for j in range(i + 1, len(self.__col_names)):
                        a = self.__col_names[j]
                        if (a == c) and (self.__colonnes_egales(i, j)):
                            toDelete.append((c, j))
                            unique = False
                if self.debug and len(toDelete) > 0:
                    print(f"Colonnes dupliquées : {toDelete}")

                toDelete.reverse()
                for (c, i) in toDelete:
                    del self.__col_names[i]
                    for j in self.__data:
                        del j[i]
            # transformation en Polars pour l'affichage
            self.__pl_data = pl.DataFrame(self.__data, schema=self.__col_names, orient='row')

    def __colonnes_egales(self, a, b):
        """
        Détermine si la colonne a est égale à la colonne b dans self.__data
        :param a: colonne a
        :param b: colonne b
        :return: bool
        """
        egale = False
        for i in self.__data:
            egale = egale or i[a] == i[b]
        return egale

    def getTable(self):
        return self.__data

    def getPLTable(self):
        """
        Returns a Polars DataFrame
        """
        return self.__pl_data

    def getPDTable(self):
        """
        Returns a Pandas DataFrame
        """
        return self.__pl_data.to_pandas()

    def stringToQuery(self):
        # print(self.__str)
        stmt = parse_one(self.__str)
        # print(stmt)
        # pprint(stmt)

        self.select = stmt.expressions
        # print(', '.join([str(x) for x in self.select]))
        self.distinct = stmt.args["distinct"] is not None

        self.sqlTables = list()
        self.from_all = [stmt.find(From)]
        for t in self.from_all[0].find_all(exp.Table):
            if t.alias:
                self.sqlTables.append((t.this.this, str(t.alias)))
            else:
                self.sqlTables.append((t.this.this, None))
        self.from_join = None
        if 'joins' in stmt.args:
            joins = stmt.args["joins"]
            self.from_all.append(joins)
            for j in joins:
                for t in j.find_all(exp.Table):
                    if t.alias:
                        self.sqlTables.append((t.this.this, str(t.alias)))
                    else:
                        self.sqlTables.append((t.this.this, None))
            self.from_join = str(self.from_all[0]) + ' ' + ' '.join([str(j) for j in joins])
        else:
            self.from_join = str(self.from_all[0])

        self.where = stmt.find(Where)

        self.group_by = stmt.find(Group)
        if self.group_by :
            self.group = [str(x) for x in self.group_by]
        else :
            self.group = None

        self.having = stmt.find(Having)

        self.order = stmt.find(Order)
        self.limit = stmt.find(Limit)
        self.offset = stmt.find(Offset)

        if self.debug: print(self.sqlTables)
        return stmt

    def __parcoursFrom(self, smt, deep=0):
        if isinstance(smt, Select):
            if self.debug: print('\t' * deep, f"--> Select : {smt}")
            l = []
            l += self.__parcoursFrom(smt.args['from'], deep + 1)
            if "joins" in smt.args:
                joins = smt.args["joins"]
                req = f"Select * {smt.args['from']}"
                for j in joins:
                    l += self.__parcoursFrom(j, deep + 1)
                    req += f' {j}'
                    l += [f'{req} ; --(Sel)']
            if self.debug: print('\t' * deep, f"<-- Select...{l}")
            return l
        elif isinstance(smt, From):  # ok
            if self.debug: print('\t' * deep, f"--> From : {smt}")
            l = self.__parcoursFrom(smt.this, deep + 1)
            if self.debug: print('\t' * deep, f"<-- From...{l}")
            return l
        elif isinstance(smt, Table):  # ok
            if self.debug: print('\t' * deep, f"--> Table : {smt.this}")
            l = [f'Select * From {smt.this} ; --(Tab)']
            rep = f'Select * From {smt.this}'
            if "joins" in smt.args:
                joins = smt.args["joins"]
                for j in joins:
                    l += self.__parcoursFrom(j, deep + 1)
                    rep += f' {j}'
                    l += [f'{rep} ; --(TaJ)']
            if self.debug: print('\t' * deep, f"<-- Table...{l}")
            return l
        elif isinstance(smt, Join):  # ok
            if self.debug: print('\t' * deep, f"--> Join : {smt}")
            l = self.__parcoursFrom(smt.this, deep + 1)
            if self.debug: print('\t' * deep, f"<-- Join...{l}")
            return l
        elif isinstance(smt, Subquery):
            if self.debug: print('\t' * deep, f"--> Subquery : {smt.this}")
            l = self.__parcoursFrom(smt.this, deep + 1)
            rep = f'Select * From ({smt.this})'
            if "joins" in smt.args:
                joins = smt.args["joins"]
                for j in joins:
                    l += self.__parcoursFrom(j, deep + 1)
                    rep += f' {j}'
                    l += [f'{rep} ; --(Sub)']
            if self.debug: print('\t' * deep, f"<-- Subquery...{l}")
            return l
        else:
            if self.debug: print(f"==> Unknown Smt {type(smt)} : {smt} ")

    def sbs_sql(self):
        smt = self.stringToQuery()
        sql_lst = []

        if self.distinct:
            cls_distinct = ' Distinct '
        else:
            cls_distinct = ''
        cls_select_bis = ''
        if self.select is not None:
            cls_select = ', '.join([str(x) for x in self.select])
        else:
            cls_select = ''

        cls_from = ' ' + self.from_join

        # pprint(self.from_join)
        cls_joins = self.from_all  # self.__buildJoins(self.from_join)
        # pprint(cls_joins)

        if self.where is not None:
            cls_where = ' ' + str(self.where)
        else:
            cls_where = ''

        if self.group is not None:
            att_list = []
            for (t, a) in self.sqlTables:
                (id_t, des) = self.__db.dbTables[t]
                for att in des:
                    att_list.append(f"{self.getAlias(t)}.{att[0]}")
            cls_select_bis = ','.join(att_list)

            lgp = []
            for x in self.group:
                if '.' not in x:
                    for (t, a) in self.sqlTables:
                        (id_t, l) = self.__db.dbTables[t]
                        for y in l:
                            if x == y[0]:
                                lgp.append(self.getAlias(t) + '.' + x)
                else:
                    lgp.append(x)

            txt_group = ', '.join(lgp)
            cls_group_by = ' Group By ' + txt_group
            cls_group_by_bis = ' Order By ' + txt_group
            cls_group_by_ter = ' Order By ' + ', '.join(self.group)
        else:
            cls_group_by = ''
            cls_group_by_bis = ''
            txt_group = ''
        if self.having is not None:
            cls_having = ' ' + str(self.having)
            if cls_where == '':
                cls_where_tmp = ' Where (' + txt_group + ') in (select ' + txt_group + cls_from + cls_where + cls_group_by + cls_having + ')'
            else:
                cls_where_tmp = cls_where + ' and (' + txt_group + ') in (select ' + txt_group + cls_from + cls_where + cls_group_by + cls_having + ')'
        else:
            cls_having = ''
            cls_where_tmp = cls_where
        if self.order is not None:
            cls_order_by = ' ' + str(self.order)
        else:
            cls_order_by = ''
        if self.limit is not None:
            cls_limit = ' ' + str(self.limit)
        else:
            cls_limit = ''
        if self.offset is not None:
            cls_offset = ' ' + str(self.offset)
        else:
            cls_offset = ''

        sql_str = 'select ' + cls_distinct + cls_select + cls_from + cls_where + cls_group_by + cls_having + cls_order_by + cls_limit + cls_offset + ' ;'

        # Affichage des tables sources
        # et construction du FROM

        if self.debug: print('Gestion du From :')
        lfrom= self.__parcoursFrom(smt)
        for s in lfrom:
            sql_lst.append(SQL(db=self.__db.getDBCon(), dbtype=self.__db.getType(),
                              str=s,
                              name='§1-FROM§ ' + bold_substring(sql_str, s[14:-10]), debug=self.debug, verbose=self.verbose))

        # WHERE
        if self.where is not None:
            loc_str = 'select * ' + cls_from + cls_where + ' ;'
            if self.debug: print('Gestion du Where :', loc_str)
            s = SQL(db=self.__db.getDBCon(), dbtype=self.__db.getType(), str=loc_str,
                    name='§2-WHERE§ ' + bold_substring(sql_str, cls_from + cls_where), debug=self.debug, verbose=self.verbose)
            s.setSQLTables(self.sqlTables)
            sql_lst.append(s)

        # GROUP BY (1)
        if self.group is not None:
            loc_str = 'select  ' + cls_select_bis + cls_from + cls_where + cls_group_by_bis + ' ;'
            if self.debug: print('Gestion du Group By (1) : ', loc_str)
            s = SQL(db=self.__db.getDBCon(), dbtype=self.__db.getType(),
                    str=loc_str,
                    name='§3-GROUP BY ' + txt_group + '§ ' + bold_substring(sql_str,
                                                                            cls_from + cls_where + cls_group_by),
                    debug=self.debug, verbose=self.verbose)
            s.setSQLTables(self.sqlTables)
            sql_lst.append(s)

        # HAVING
        if self.having is not None:
            loc_str = 'select  ' + cls_select_bis + cls_from + cls_where_tmp + cls_group_by_bis + ' ;'
            if self.debug: print('Gestion du Having : ', loc_str)
            s = SQL(db=self.__db.getDBCon(), dbtype=self.__db.getType(),
                    str=loc_str,
                    name='§4-GROUP BY ' + txt_group + ' HAVING§ ' + bold_substring(sql_str,
                                                                                   cls_from + cls_where + cls_group_by + cls_having),
                    debug=self.debug, verbose=self.verbose)
            s.setSQLTables(self.sqlTables)
            sql_lst.append(s)

        #  GROUP BY (2) (avec ou sans HAVING)
        # if self.group is not None:
        #    sql_lst.append(SQL(db=self.__db, dbtype=self.__dbtype, str='select * ' + cls_from + cls_where + cls_group_by + cls_having + ' ;',
        #                       name='<3-GROUP BY ' + txt_group + ' HAVING> ' + bold_substring(sql_str,
        #                                                                                       cls_from + cls_where + cls_group_by + cls_having)))

        # SELECT
        loc_str = 'select ' + cls_select + cls_from + cls_where + cls_group_by + cls_having + ' ;'
        if self.debug: print('Gestion du Select : ', loc_str)
        s = SQL(db=self.__db.getDBCon(), dbtype=self.__db.getType(),
                str=loc_str,
                name='§5-SELECT§ ' + bold_substring(sql_str,
                                                    cls_select + cls_from + cls_where + cls_group_by + cls_having),
                debug=self.debug, verbose=self.verbose)
        s.setSQLTables(self.sqlTables)
        sql_lst.append(s)

        # DISTINCT
        if self.distinct:
            loc_str = 'select ' + cls_distinct + cls_select + cls_from + cls_where + cls_group_by + cls_having + ' ;'
            if self.debug: print('Gestion du Distinct : ', loc_str)
            s = SQL(db=self.__db.getDBCon(), dbtype=self.__db.getType(),
                    str=loc_str,
                    name='§6-DISTINCT§ ' + bold_substring(sql_str,
                                                          cls_distinct + cls_select + cls_from + cls_where + cls_group_by + cls_having),
                    debug=self.debug, verbose=self.verbose)
            s.setSQLTables(self.sqlTables)
            sql_lst.append(s)

        # ORDER BY
        if self.order is not None:
            loc_str = 'select ' + cls_distinct + cls_select + cls_from + cls_where + cls_group_by + cls_having + cls_order_by + ' ;'
            if self.debug: print('Gestion du Order By : ', loc_str)
            s = SQL(db=self.__db.getDBCon(), dbtype=self.__db.getType(),
                    str=loc_str,
                    name='§7-ORDER BY§ ' + bold_substring(sql_str,
                                                          cls_distinct + cls_select + cls_from + cls_where + cls_group_by + cls_having + cls_order_by),
                    debug=self.debug, verbose=self.verbose)
            s.setSQLTables(self.sqlTables)
            sql_lst.append(s)

        # LIMIT
        if self.limit is not None:
            loc_str = 'select ' + cls_distinct + cls_select + cls_from + cls_where + cls_group_by + cls_having + cls_order_by + cls_limit + ' ;'
            if self.debug: print('Gestion du Limit : ', loc_str)
            s = SQL(db=self.__db.getDBCon(), dbtype=self.__db.getType(),
                    str=loc_str,
                    name='§8-LIMIT§ ' + bold_substring(sql_str,
                                                       cls_distinct + cls_select + cls_from + cls_where + cls_group_by + cls_having + cls_order_by + cls_limit),
                    debug=self.debug, verbose=self.verbose)
            s.setSQLTables(self.sqlTables)
            sql_lst.append(s)

        # OFFSET
        if self.offset is not None:
            loc_str = 'select ' + cls_distinct + cls_select + cls_from + cls_where + cls_group_by + cls_having + cls_order_by + cls_limit + cls_offset + ' ;'
            if self.debug: print('Gestion du Offset : ', loc_str)
            s = SQL(db=self.__db.getDBCon(), dbtype=self.__db.getType(),
                    str=loc_str,
                    name='§9-OFFSET§ ' + bold_substring(sql_str,
                                                        cls_distinct + cls_select + cls_from + cls_where + cls_group_by + cls_having + cls_order_by + cls_limit + cls_offset),
                    debug=self.debug, verbose=self.verbose)
            s.setSQLTables(self.sqlTables)
            sql_lst.append(s)

        # pprint([x.__str__() for x in sql_lst])
        return sql_lst


    def __key(self, tbl):
        k = []
        for att, isKey, isKKey in tbl:
            if isKey: k.append(att)
        return k

    def __notkey(self, tbl):
        k = []
        for att, isKey, isKKey in tbl:
            if not isKey: k.append(att)
        return k

    """
    def __separateGroupByTable_old(self, df: pd.DataFrame, args_to_group_by: list[str], clr: bool) -> pd.DataFrame:
        # print(df)
        if args_to_group_by and clr:
            for col in self.__col_names:
                # on regarde les attributs qui peuvent avoir une valeur unique (autre que issus du group by)
                # algo prend comme hypothèse qu'il n'y a pas deux attributs de même nom avec une sémantique différente.
                unique = False
                for i in self.sqlTables:
                    v = self.dbTables[i]
                    if col in self.__notkey(v) and set(self.__key(v)).issubset(set(args_to_group_by)):
                        unique = True
                        break
                # ceux qui sont pas uniques sont remplacés par {...}
                if col not in args_to_group_by and not unique:
                    df[col] = df[col].apply(lambda x: '{...}' if x is not None else '')
        # print(df)
        grouped_dict = df.groupby(args_to_group_by).groups
        grouped_data = [
            df.loc[val, self.__col_names].values
            for key, val in grouped_dict.items()
        ]
        separated_data = []
        for group in grouped_data:
            for row in group:
                separated_data.append(row)
            separated_data.append(SEPARATING_LINE)

        df = pd.DataFrame(separated_data[:-1])
        return df

    def printTable_old(self, gb: str | None, clr=False, output=None) -> None:
        df = pd.DataFrame(self.__data, columns=self.__col_names)
        if gb is not None:
            df = self.__separateGroupByTable(df=df, args_to_group_by=gb.split(', '), clr=clr)
        print(tabulate(df.fillna(''), headers=self.__col_names, tablefmt="simple", showindex=False), file=output)

    def table_old(self):
        assert (self.__data is not None and self.__col_names is not None)
        print('==================================================================================================')
        print(self.name)
        if self.group is not None or self.name.startswith('<GROUP BY'):
            gp = re.search(r'<\bGROUP BY\b\s(\d)\s+(.+?)\s*(HAVING)?>', self.name)
            if self.name.startswith('<GROUP BY'):
                self.printTable(gb=gp[2], output=None, clr=gp[1] == '2')
            else:
                self.printTable(gb=self.group, output=None, clr=self.__str.startswith('select *'))
        else:
            self.printTable(gb=None, output=None)
        print('')
    

    def __separateGroupByTable(self, args_to_group_by: list[str], clr: bool) -> pd.DataFrame:
        df = self.getPDTable()
        print(df)
        if args_to_group_by and clr:
            for col in self.__col_names:
                # on regarde les attributs qui peuvent avoir une valeur unique (autre que issus du group by)
                # algo prend comme hypothèse qu'il n'y a pas deux attributs de même nom avec une sémantique différente.
                unique = False
                for i in self.sqlTables:
                    v = self.dbTables[i]
                    if col in self.__notkey(v) and set(self.__key(v)).issubset(set(args_to_group_by)):
                        unique = True
                        break
                # ceux qui sont pas uniques sont remplacés par {...}
                if col not in args_to_group_by and not unique:
                    df[col] = df[col].apply(lambda x: '{...}' if x is not None else '')
        print(df)
        cols = list(df.columns)
        lg = [i for i, v in enumerate(cols) if v in args_to_group_by]
        old = []
        separated_data = []
        for row in df.itertuples(name=None):
            if old == []:
                separated_data.append(row)
                for i in lg:
                    old.append(row[i])
            else:
                new = []
                for i in lg:
                    new.append(row[i])
                if new != old:
                    separated_data.append(SEPARATING_LINE)
                    old = new
                separated_data.append(row)
        print(separated_data)
        return pd.DataFrame(separated_data, columns=self.__col_names)
    """

    def clearTBL(self, df, args_to_group_by):
        """
        Permet de gérer le problème de SQLite en cas de Group By avec un Select *
        :param df: le tableau à traiter
        :param args_to_group_by: les arguments du group by
        :return: Le tableau modifié
        """
        for col in self.__col_names:
            # on regarde les attributs qui peuvent avoir une valeur unique (autre que issus du group by)
            # algo prend comme hypothèse qu'il n'y a pas deux attributs de même nom avec une sémantique différente.
            unique = False
            for i in self.sqlTables:
                (id_t, v) = self.__db.dbTables[i]
                if col in self.__notkey(v) and set(self.__key(v)).issubset(set(args_to_group_by)):
                    unique = True
                    break

            if col not in args_to_group_by and not unique:  # ceux qui sont pas uniques sont remplacés par {...}
                df = df.with_columns(
                    pl.apply(col, (lambda x: '{...}' if x is not None else ''), return_dtype=pl.datatypes.String))
            elif col not in args_to_group_by:
                df = df.with_columns(pl.col(col).list.first().alias(col))
        return df
    def printTable(self, gb: list | None, clr=False) -> None:
        with pl.Config() as cfg:
            cfg.set_tbl_cols(20)
            cfg.set_tbl_rows(20)
            if self.verbose: cfg.set_tbl_hide_dataframe_shape(False)
            else: cfg.set_tbl_hide_dataframe_shape(True)
            cfg.set_fmt_table_cell_list_len(-1)
            cfg.set_tbl_hide_column_data_types(True)
            if gb is not None:
                if clr:
                    cfg.set_fmt_table_cell_list_len(-1)
                lgroupby = [x for x in gb if x in self.__col_names]
                lothers = [x for x in self.__col_names if x not in gb]
                df = self.__pl_data.group_by(lgroupby, maintain_order=True).agg(lothers)
                if clr:
                    print(self.clearTBL(df, gb))
                else:
                    print(df)
            else:
                if clr:
                    print(self.clearTBL(self.__pl_data, self.group))
                else:
                    print(self.__pl_data)

    def table(self):
        if (self.__data is None or self.__col_names is None):
            if self.debug:
                print('---> No data or column names found. SQL query is executed')
            self.execute()
        print('==================================================================================================')
        if self.debug :
            print(self.name)
        else :
            print(delEntete(self.name,'§'))
        if self.debug : print(self.__str)
        step = re.search(r'\§(\d)\-(.+)\§\s(.*)$', self.name)
        if step[1] in ['1', '2']:  # From et Where
            self.printTable(gb=None)
        elif step[1] in ['3', '4']:  # Group-By et Having
            gp = re.search(r'GROUP BY\s+(.+?)(\sHAVING)?$', step[2])
            if self.__db.getType() == 'pgsql':
                lgp = []
                for att in gp[1].split(','):
                    if '.' in att:
                        tatt = att.split('.')
                        for (t, a) in self.sqlTables:
                            if a == tatt[0].strip():
                                lgp.append(a + '.' + tatt[1].strip())
                            elif t == tatt[0].strip():
                                lgp.append(att.strip())
                    else:
                        for (t, a) in self.sqlTables:
                            (id_t, l) = self.__db.dbTables[t]
                            for x in l:
                                if x[0] == att.strip():
                                    if a is None:
                                        lgp.append(t + '.' + att.strip())
                                    else:
                                        lgp.append(a + '.' + att.strip())
                                    break
                if self.debug: print(lgp)
                self.printTable(gb=lgp, clr=False)  # step == '3')
            else:
                lgp = [x.strip() for x in gp[1].split(',')]
                if self.debug: print(lgp)
                self.printTable(gb=lgp, clr=False)  # step == '3')
        else:  # Select, Distinct, Order By, Limit, Offset
            self.printTable(gb=None)
        print('')

    def sbs(self):
        for s in self.sbs_sql():
            # s.execute()
            s.table()


# TODO : Faire une fonction qui compare la syntaxe de deux requêtes


if __name__ == '__main__':
    sql_txt = """SELECT distinct  m.codemat as no, titre, count(*)
FROM matieres m left join notes n inner join etudiants using (noetu) on m.codemat = n.codemat 
where m.codemat in (select codemat from matieres where diplome = 'L2') and noteex > 5
group by m.codemat, titre
having count(*) >1 Order by titre Limit 10 Offset 2;"""
    # db = Database.get('../static/bdd/cours/cours.db', 'sqlite')
    # (dsc, data) = db.execute(sql_txt)
    # pprint(data)
    # pprint(dsc)
    # db = Database.get('dbname=cours', 'pgsql')
    # (dsc, data) = db.execute(sql_txt)
    # pprint(data)
    # pprint(dsc)
    # sql = SQL('../static/bdd/cours/cours.db', 'sqlite')
    # sql.setSQL(sql_txt)
    # sql.stringToQuery()
    db = Database.get(('dbname=cours'), 'pgsql', debug = False)
