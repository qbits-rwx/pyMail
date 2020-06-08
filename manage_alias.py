#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
import argparse
import datetime
from getpass import getpass
import mysql.connector as mariadb

def get_alias(domain):
    # get sql passwd for user pymail
    user_name = input('DB Username: ')
    passwd = getpass('Enter password: ')
    # SQL query to execute
    sql_query = ("select * from alias where domain = '{0}' ".format(domain))
    # create connection object
    mariadb_connection = mariadb.connect(user=user_name, password=passwd, database='vmail')
    # create cursor object
    cursor = mariadb_connection.cursor()
    # execute query
    cursor.execute(sql_query)
    # save result set to variable
    alias = cursor.fetchall()
    # close connection curser object
    cursor.close()
    # close the connection
    mariadb_connection.close()
    # return the result
    return alias

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Manage Postfix mail alias stuff')
    parser.add_argument('-H',
            help='Sample Script calls:  \
                  ADD: manage_alias.py --add foo@bar.com -ft real@bar,com -d sample@domain.com \
                  DELETE: manage_alias.py --remove foo@bar.com \
                  LIST: manage_alias.py --list bar.com')
    parser.add_argument('-d', '--domain', required=True, default='rwx-berlin.de')
    parser.add_argument('-l', '--list', action='store_true')
    parser.add_argument('-a', '--add', action='store_true', help='Add mail alias to table alias and create destination entry in table forwardings ')
    parser.add_argument('-r', '--remove', action='store_true', help='Remove mail alias to table alias and create destination entry in table forwardings ')
    parser.add_argument('-ft', '--forward-to', action='store_true', help='The email-address to forward mails to alias -> real address')

    global args

    args = parser.parse_args()

    domain = args.domain

    if args.list:
        domain_alias = get_alias(domain)
        print(domain_alias)
