#!/usr/bin/env python3

import argparse
import os

from querycraft.SQL import SQL


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '--db', help='database name', default='cours')
    parser.add_argument('-u', '--user', help='database user', default='postgres')
    parser.add_argument('-p', '--password', help='database password', default='')
    parser.add_argument('--host', help='database host', default='localhost')
    parser.add_argument('--port', help='database port', default='5432')

    parser.add_argument('--debug', help='debug mode', action='store_true', default=False)
    parser.add_argument('-v', '--verbose', help='verbose mode', action='store_true', default=False)

    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('-f', '--file', help='sql file')
    group.add_argument('-s', '--sql', type=str, help='sql string',
                       default='select * from etudiants join notes using(noetu) ;')

    args = parser.parse_args()
    if args.file:
        sqlTXT = ''
        with open(args.file, 'r') as f:
            sqlTXT += f.read()
    elif args.sql:
        sqlTXT = args.sql
    else:
        print('no sql file or sql string')
        exit(1)

    debug = args.debug
    verbose = args.verbose

    if debug:
        print('Infos BD : ', type, args.user, args.password, args.host, args.port, args.db)
    sql = SQL(db=f"dbname={args.db} user={args.user} password={args.password} host={args.host} port={args.port}",
              dbtype='pgsql', debug=debug, verbose=verbose)
    sql.setSQL(sqlTXT)

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


if __name__ == '__main__':
    main()
