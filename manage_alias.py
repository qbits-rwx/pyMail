#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# INSERT INTO forwardings (address, forwarding,domain,
# dest_domain,is_list, active) VALUES ('benjamin@rwx-berlin.de',
# 'bkubitz@rwx-berlin.de', 'rwx-berlin.de', 'rwx-berlin.de',1, 1);
import argparse
import datetime
from getpass import getpass
import mysql.connector as mariadb


def mysql_login():
    user_name = input('DB Username: ')
    passwd = getpass('Enter password: ')

    return [user_name, passwd]


def get_alias(domain):
    login_data = mysql_login()
    # SQL query to execute
    sql_query_cmd = (
        "select * from alias where domain = '{0}' ".format(domain))
    # create connection object
    mariadb_connection = mariadb.connect(
        user=login_data[0],
        password=login_data[1],
        database='vmail')
    # create cursor object
    cursor = mariadb_connection.cursor()
    # execute query
    cursor.execute(sql_query_cmd)
    # save result set to variable
    alias = cursor.fetchall()
    # close connection curser object
    cursor.close()
    # close the connection
    mariadb_connection.close()
    # return the result
    return alias


def add_alias(address, domain):
    login_data = mysql_login()
    # INSERT INTO alias (address, domain, active) VALUES
    # ('benjamin@rwx-berlin.de', 'rwx-berlin.de', 1);
    sql_insert_alias_cmd = (
        "INSERT INTO alias (address, domain, active) VALUES ('{0}', '{1}', 1)".format(
            address, domain))
    # create connection object
    mariadb_connection = mariadb.connect(
        user=login_data[0],
        password=login_data[1],
        database='vmail')
    # create cursor object
    cursor = mariadb_connection.cursor()
    # insert values to DB
    cursor.execute(sql_insert_alias_cmd)
    # do a DB commit
    cursor.commit()

    print(cursor.rowcount, "was inserted.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Manage Postfix mail alias stuff')
    parser.add_argument('-H',
                        help='Sample Script calls:  \
                  ADD: manage_alias.py --add foo@bar.com -ft real@bar,com -d sample@domain.com \
                  DELETE: manage_alias.py --remove foo@bar.com \
                  LIST: manage_alias.py --list bar.com')
    parser.add_argument(
        '-d',
        '--domain',
        required=True,
        default='rwx-berlin.de')
    parser.add_argument('-l', '--list', action='store_true')
    parser.add_argument(
        '-a',
        '--add',
        action='store_true',
        help='Add mail alias to table alias and create destination entry in table forwardings ')
    parser.add_argument(
        '-r',
        '--remove',
        action='store_true',
        help='Remove mail alias to table alias and create destination entry in table forwardings ')
    parser.add_argument(
        '-ft',
        '--forward-to',
        action='store_true',
        help='The email-address to forward mails to alias -> real address')

    global ARGS

    ARGS = parser.parse_args()

    domain = ARGS.domain

    if ARGS.list:
        domain_alias = get_alias(domain)
        print(domain_alias)
