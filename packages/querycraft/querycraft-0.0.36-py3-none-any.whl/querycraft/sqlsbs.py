#!/usr/bin/env python3

import argparse
import importlib.resources
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
    #parser.add_argument('--debug', help='debug mode', action='store_true', default=False)
    parser.add_argument('-v', '--verbose', help='verbose mode', action='store_true', default=False)
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('-f', '--file', help='sql file')
    group.add_argument('-s', '--sql', type=str, help='sql string',
                       default='select * from etudiants join notes using(noetu) ;')

    parser.add_argument('--lrs', help='use en Veracity lrs', action='store_true', default=False)
    parser.add_argument('--lrs-user', help=f'lrs user (by default toto)', default='toto')  # 'desmontils-e')
    parser.add_argument('--lrs-password', help='lrs password (by default toto)', default='toto')
    parser.add_argument('--lrs-endpoint', help=f'lrs endpoint (by default http://local.veracity.it/querycraft/xapi/)',
                        default='http://local.veracity.it/querycraft/xapi/')  # 'localhost')


def dbConnectArgs(parser, defaultPort, defaultHost='localhost', defaultUser='desmontils-e', verbose=False):
    parser.add_argument('-d', '--db', help='database name', default='cours')
    parser.add_argument('-u', '--user', help=f'database user (by default {defaultUser})',
                        default=defaultUser)  # 'desmontils-e')
    parser.add_argument('-p', '--password', help='database password', default='')
    parser.add_argument('--host', help=f'database host (by default {defaultHost})', default=defaultHost)  # 'localhost')
    parser.add_argument('--port', help=f'database port (by default {defaultPort})', default=defaultPort)  # '5432')


def doSBS(db, dbtype, dbname, sqlTXT, debug, verbose, lrs=None):
    try:
        if lrs:
            lrs.setContextSBS()
        sql = SQL(db=db, dbtype=dbtype, debug=debug, verbose=verbose)
        sql.setSQL(sqlTXT)
        if lrs: lrs.sendSBSExecute(dbtype, dbname, sqlTXT)
        try:
            sbs(sql, verbose)  # Pas à pas
            if lrs: lrs.sendSBSpap(dbtype, dbname, sqlTXT)
        except Exception as e:
            # LRS : envoie du statement
            if lrs: lrs.sendSBSpap(dbtype, dbname, sqlTXT, error=e)
            print(f'Erreur SBS : {e}')
    except Exception as e:
        pprint(e)
        # LRS : envoie du statement
        if lrs: lrs.sendSBSExecute(dbtype, dbname, sqlTXT, error=e)
        exit()


def mysql():
    parser = argparse.ArgumentParser(
        description="Effectue l'exécution pas à pas d'une requête sur MySQL\n (c) E. Desmontils, Nantes Université, 2024")
    dbConnectArgs(parser, '3306', defaultHost='localhost', verbose=True)
    stdArgs(parser)
    args = parser.parse_args()
    sqlTXT = getQuery(args)
    debug = args.debug
    verbose = args.verbose
    if debug:
        print('Infos BD : ', type, args.user, args.password, args.host, args.port, args.db)
    if args.lrs:
        doSBS((args.user, args.password, args.host, args.db), 'mysql', args.db, sqlTXT, args.debug, args.verbose,
              LRS(args.lrs_endpoint, args.lrs_user, args.lrs_password, debug=args.debug))
    else:
        doSBS((args.user, args.password, args.host, args.db), 'mysql', args.db, sqlTXT, args.debug, args.verbose)


def pgsql():
    parser = argparse.ArgumentParser(
        description="Effectue l'exécution pas à pas d'une requête sur PostgreSQL\n (c) E. Desmontils, Nantes Université, 2024")
    dbConnectArgs(parser, '5432', defaultHost='localhost', verbose=True)
    stdArgs(parser)
    args = parser.parse_args()
    sqlTXT = getQuery(args)
    if args.debug:
        print('Infos BD : ', type, args.user, args.password, args.host, args.port, args.db)
    if args.lrs:
        doSBS(f"dbname={args.db} user={args.user} password={args.password} host={args.host} port={args.port}", 'pgsql',
              args.db, sqlTXT, args.debug, args.verbose,
              LRS(args.lrs_endpoint, args.lrs_user, args.lrs_password, debug=args.debug))
    else:
        doSBS(f"dbname={args.db} user={args.user} password={args.password} host={args.host} port={args.port}", 'pgsql',
              args.db, sqlTXT, args.debug, args.verbose)


def sqlite():
    parser = argparse.ArgumentParser(
        description="Effectue l'exécution pas à pas d'une requête sur SQLite\n (c) E. Desmontils, Nantes Université, 2024")
    parser.add_argument('-d', '--db', help='database name', default='../test/cours.db')
    stdArgs(parser)
    args = parser.parse_args()
    sqlTXT = getQuery(args)
    if not (existFile(args.db)):
        print('database file not found')
        exit(1)
    else:
        if args.verbose: print('database exists')
    if args.debug:
        print('Infos BD : ', type, args.user, args.password, args.host, args.port, args.db)
    if args.lrs:
        doSBS(args.db, 'sqlite', args.db, sqlTXT, args.debug, args.verbose,
              LRS(args.lrs_endpoint, args.lrs_user, args.lrs_password, debug=args.debug))
    else:
        doSBS(args.db, 'sqlite', args.db, sqlTXT, args.debug, args.verbose)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--lrs', help='use en Veracity lrs', action='store_true', default=False)
    parser.add_argument('-v', '--verbose', help='verbose mode', action='store_true', default=False)
    parser.add_argument('--debug', help='debug mode', action='store_true', default=False)
    parser.add_argument('-d', '--db', help='database file (sqlite) or name (others)', default=None)
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
    with importlib.resources.open_text("querycraft.config", "config-sbs.cfg") as fichier:
        cfg.read_file(fichier)

    onLRS = args.lrs
    # Debug ?
    debug = cfg.getboolean('Autre', 'debug') or args.debug
    verbose = cfg.getboolean('Autre', 'verbose') or args.verbose
    if debug:
        print("Mode debug activé")
    package_files = importlib.resources.files("querycraft.data")
    # Database configuration
    if args.db:
        if args.db.endswith('.db'):
            database = package_files / args.db
            if debug: print("SQLite database from parameter")
            type = 'sqlite'
            username = None
            password = None
            host = None
            port = None
        else:
            database = args.db
            if debug: print("PGSQL database from parameter")
            type = 'pgsql'  # Database configuration
            username = 'postgres'
            password = ''
            host = 'localhost'
            port = '5432'
    else:
        type = cfg['Database']['type']
        if type == 'sqlite':
            if debug: print("SQLite database from config file")
            database = package_files / cfg['Database'][
                'database']  # importlib.resources.resource_filename("querycraft.data", cfg['Database']['database'])
            username = None
            password = None
            host = None
            port = None
        else:
            if debug: print("PGSQL ou MYSQL database from config file")
            username = cfg['Database']['username']
            password = cfg['Database']['password']
            host = cfg['Database']['host']
            port = cfg['Database']['port']
            database = cfg['Database']['database']

    # xAPI configuration
    if onLRS:
        lrs = LRS(cfg['LRS']['endpoint'], cfg['LRS']['username'], cfg['LRS']['password'], debug=debug)
        lrs.setContextSBS()

    if debug:
        print('Infos BD : ', type, username, password, host, port, database)

    try:
        try:
            if type is None:
                raise Exception("Configuration non fournie")
            if type == 'sqlite':
                sql = SQL(db=database, dbtype='sqlite', debug=debug, verbose=verbose)
            elif type == 'pgsql': # f"dbname={database} user={username} password={password} host={host} port={port}"
                sql = SQL(f"dbname={database} user={username} password={password} host={host} port={port}", dbtype='pgsql', debug=debug, verbose=verbose)
            elif type == 'mysql': # (username, password, host ,database) # port ????
                sql = SQL(db=(username, password, host ,database), dbtype='mysql', debug=debug, verbose=verbose)
            else:
                raise Exception("Base de données non supportée")

            sql.setSQL(sqlTXT)

            # LRS : envoie du statement
            if onLRS: lrs.sendSBSExecute(type, database, sqlTXT)

        except Exception as e:
            pprint(e)
            # LRS : envoie du statement
            if onLRS: lrs.sendSBSExecute(type, database, sqlTXT, error=e)
            exit()

        sbs(sql, verbose)  # Pas à pas

        if onLRS: lrs.sendSBSpap(type, database, sqlTXT)

    except Exception as e:
        # LRS : envoie du statement
        if onLRS: lrs.sendSBSpap(type, database, sqlTXT, e)
        print(f'Erreur SBS : {e}')


if __name__ == '__main__':
    main()
