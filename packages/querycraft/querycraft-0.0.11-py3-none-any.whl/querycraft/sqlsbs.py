#!/usr/bin/env python3

import argparse
import os

from querycraft.LRS import LRS
from querycraft.SQL import SQL

from configparser import ConfigParser
from pprint import pprint

def main():
    parser = argparse.ArgumentParser()
    # parser.add_argument('-d', '--db', help='database file (sqlite) or name (others)', default='./static/bdd/cours/cours.db')
    # parser.add_argument('--sgbd', help='database (pgsql, mysql or sqlite)', default='sqlite')
    parser.add_argument('--cfg', help='configuration file', default='config-sqlsbs.cfg')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-f', '--file', help='sql file')
    group.add_argument('-s', '--sql', type=str, help='sql string')

    args = parser.parse_args()
    if args.file:
        sqlTXT = ''
        with open(args.file, 'r') as f:
            sqlTXT += f.read()
        # print(sqlTXT)
    elif args.sql:
        sqlTXT = args.sql
    else:
        print('no sql file or sql string')
        exit(1)

    # db = Database.getPGSQLDB(dbcon='dbname=cours')
    # db = Database.getPGSQLDB(dbcon='dbname=cours')
    # db = Database.getSQLiteDB(dbcon='./static/bdd/cours/cours.db')
    # db = Database.getSQLiteDB(dbcon='./static/bdd/cours/cours.db')
    # db = Database.getDB('./static/bdd/cours/cours.db','sqlite')
    # exit()

    # ==================================================
    # === Gestion de la configuration =================
    # ==================================================

    cfg = ConfigParser()
    onLRS = False
    if cfg.read(args.cfg):

        # Debug ?
        debug = cfg.getboolean('Autre', 'debug')
        if debug:
            print("Mode debug activé")

        # xAPI configuration
        if onLRS :
            lrs = LRS(cfg['LRS']['endpoint'],cfg['LRS']['username'],cfg['LRS']['password'],debug=debug)
            lrs.setContextSBS()

        # Database configuration
        type = cfg['Database']['type']
        username = cfg['Database']['username']
        password = cfg['Database']['password']
        host = cfg['Database']['host']
        database = cfg['Database']['database']



    else:
        lrs = None
        type = None
        username = None
        password = None
        host = None
        database = None
        print("Configuration non fournie ou illisible")
        exit()

    if debug:
        print('Infos BD : ',type, username, password, host, database)

    try:
        if type is None:
            raise Exception("Configuration non fournie")
        if type == 'sqlite':
            sql = SQL(db=database, dbtype='sqlite',debug=debug)
        elif type == 'pgsql':
            sql = SQL(db=f"dbname={database}", dbtype='pgsql',debug=debug)
        elif type == 'mysql':
            sql = SQL(db=('root', '', 'localhost', database), dbtype='mysql',debug=debug)
        else:
            raise Exception("Base de données non supportée")

        sql.setSQL(sqlTXT)

        # LRS : envoie du statement
        if onLRS :lrs.sendSBSExecute(sqlTXT)

    except Exception as e:
        pprint(e)
        # LRS : envoie du statement
        if onLRS :lrs.sendSBSExecute(sqlTXT, error=e)
        exit()

    #try :
    print(f"Bonjour {os.getlogin()} !")
    print('==================================================================================================')
    print('======================================== Requête à analyser ======================================')
    print('==================================================================================================')
    print("--- Schéma de la base ---")
    sql.printDBTables()
    print('--- Requête à exécuter ---')
    print(sql)
    print('--- Table à obtenir ---')
    print(sql.getPLTable())
    print('==================================================================================================')
    print('========================================== Pas à pas =============================================')
    sql.sbs()
    print('fin')

    if onLRS :lrs.sendSBSpap(sqlTXT)

    #except Exception as e:
    #    # LRS : envoie du statement
    #    if onLRS :lrs.sendSBSpap(sqlTXT, e)
    #    print(f'Erreur SBS : {e}')


if __name__ == '__main__':
    main()
