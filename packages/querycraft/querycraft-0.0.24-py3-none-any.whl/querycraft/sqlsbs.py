#!/usr/bin/env python3

import argparse
import os
from configparser import ConfigParser
from pprint import pprint

from querycraft.LRS import LRS
from querycraft.SQL import SQL
from querycraft.tools import existFile


def sbs(sql, verbose=False):
    if verbose:
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
    if verbose: print('fin')


def getQuery(args):
    if args.file:
        sqlTXT = ''
        with open(args.file, 'r') as f:
            sqlTXT += f.read()
    elif args.sql:
        sqlTXT = args.sql
    else:
        print('no sql file or sql string')
        exit(1)
    return sqlTXT


def stdArgs(parser, verbose=False):
    parser.add_argument('--debug', help='debug mode', action='store_true', default=False)
    parser.add_argument('-v', '--verbose', help='verbose mode', action='store_true', default=False)
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('-f', '--file', help='sql file')
    group.add_argument('-s', '--sql', type=str, help='sql string',
                       default='select * from etudiants join notes using(noetu) ;')


def dbConnectArgs(parser, defaultPort, defaultHost='localhost', defaultUser='desmontils-e', verbose=False):
    parser.add_argument('-d', '--db', help='database name', default='cours')
    parser.add_argument('-u', '--user', help=f'database user (by default {defaultUser})', default=defaultUser)  # 'desmontils-e')
    parser.add_argument('-p', '--password', help='database password', default='')
    parser.add_argument('--host', help=f'database host (by default {defaultHost})', default=defaultHost)  # 'localhost')
    parser.add_argument('--port', help=f'database port (by default {defaultPort})', default=defaultPort)  # '5432')


def mysql():
    parser = argparse.ArgumentParser(description="Effectue l'exécution pas à pas d'une requête sur MySQL\n (c) E. Desmontils, Nantes Université, 2024")
    dbConnectArgs(parser, '3306', defaultHost='localhost', verbose=True)
    stdArgs(parser)
    args = parser.parse_args()
    sqlTXT = getQuery(args)
    debug = args.debug
    verbose = args.verbose
    if debug:
        print('Infos BD : ', type, args.user, args.password, args.host, args.port, args.db)
    sql = SQL(db=(args.user, args.password, args.host, args.db), dbtype='mysql', debug=debug, verbose=verbose)
    sql.setSQL(sqlTXT)
    sbs(sql, verbose)  # Pas à pas


def pgsql():
    parser = argparse.ArgumentParser(description="Effectue l'exécution pas à pas d'une requête sur PostgreSQL\n (c) E. Desmontils, Nantes Université, 2024")
    dbConnectArgs(parser, '5432', defaultHost='localhost', verbose=True)
    stdArgs(parser)
    args = parser.parse_args()
    sqlTXT = getQuery(args)
    debug = args.debug
    verbose = args.verbose
    if debug:
        print('Infos BD : ', type, args.user, args.password, args.host, args.port, args.db)
    sql = SQL(db=f"dbname={args.db} user={args.user} password={args.password} host={args.host} port={args.port}",
              dbtype='pgsql', debug=debug, verbose=verbose)
    sql.setSQL(sqlTXT)
    sbs(sql, verbose)  # Pas à pas


def sqlite():
    parser = argparse.ArgumentParser(description="Effectue l'exécution pas à pas d'une requête sur SQLite\n (c) E. Desmontils, Nantes Université, 2024")
    parser.add_argument('-d', '--db', help='database name', default='../test/cours.db')
    stdArgs(parser)
    args = parser.parse_args()
    sqlTXT = getQuery(args)
    if not (existFile(args.db)):
        print('database file not found')
        exit(1)
    else:
        if args.verbose: print('database exists')
    debug = args.debug
    verbose = args.verbose
    if debug:
        print('Infos BD : ', type, args.user, args.password, args.host, args.port, args.db)
    sql = SQL(db=args.db,
              dbtype='sqlite', debug=debug, verbose=verbose)
    sql.setSQL(sqlTXT)
    sbs(sql, verbose)  # Pas à pas


def main():
    parser = argparse.ArgumentParser()
    # parser.add_argument('-d', '--db', help='database file (sqlite) or name (others)', default='./static/bdd/cours/cours.db')
    # parser.add_argument('--sgbd', help='database (pgsql, mysql or sqlite)', default='sqlite')
    parser.add_argument('--cfg', help='configuration file', default='config-sqlsbs.cfg')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-f', '--file', help='sql file')
    group.add_argument('-s', '--sql', type=str, help='sql string')

    args = parser.parse_args()
    sqlTXT = getQuery(args)

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
        if onLRS:
            lrs = LRS(cfg['LRS']['endpoint'], cfg['LRS']['username'], cfg['LRS']['password'], debug=debug)
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
        print('Infos BD : ', type, username, password, host, database)

    try:
        if type is None:
            raise Exception("Configuration non fournie")
        if type == 'sqlite':
            sql = SQL(db=database, dbtype='sqlite', debug=debug)
        elif type == 'pgsql':
            sql = SQL(db=f"dbname={database}", dbtype='pgsql', debug=debug)
        elif type == 'mysql':
            sql = SQL(db=('root', '', 'localhost', database), dbtype='mysql', debug=debug)
        else:
            raise Exception("Base de données non supportée")

        sql.setSQL(sqlTXT)

        # LRS : envoie du statement
        if onLRS: lrs.sendSBSExecute(sqlTXT)

    except Exception as e:
        pprint(e)
        # LRS : envoie du statement
        if onLRS: lrs.sendSBSExecute(sqlTXT, error=e)
        exit()

    sbs(sql)  # Pas à pas

    if onLRS: lrs.sendSBSpap(sqlTXT)

    # except Exception as e:
    #    # LRS : envoie du statement
    #    if onLRS :lrs.sendSBSpap(sqlTXT, e)
    #    print(f'Erreur SBS : {e}')


if __name__ == '__main__':
    main()
