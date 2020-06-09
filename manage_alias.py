#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# INSERT INTO forwardings (address, forwarding,domain, dest_domain,is_list, active) 
# VALUES ('benjamin@rwx-berlin.de',
# 'bkubitz@rwx-berlin.de', 'rwx-berlin.de', 'rwx-berlin.de',1, 1);

import argparse
import datetime
from getpass import getpass
import sys
import mysql.connector as mariadb
# from mysql.connector import errorcode

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
    try:
        cursor.execute(sql_query_cmd)
        alias = cursor.fetchall()
    except mariadb_connection.Error as err:
        print('[ERROR] Unable to fetch alias for Domain {0} '.format(domain))
        print('MySql error {}'.format(err))
        sys.exit(1)
    finally:
        if mariadb_connection.is_connected():
            cursor.close()
            mariadb_connection.close()
            print('[INFO] connection is closed')
    if alias is not None:
        return alias
    else:
        return None


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
    try:
        # insert values to DB
        cursor.execute(sql_insert_alias_cmd)
        # do a DB commit
        cursor.commit()
        print('Alias {} inserted succesfully'.format(address))
    except mariadb_connection.Error as err:
        print('Unable to insert Alias {} to Domain {}'.format(address, domain))
        print('[ERROR] {}').format(err)
        # do rollback operation
        print('Performing rollback')
        mariadb_connection.rollback()
    finally:
        if mariadb_connection.is_connected():
            cursor.close()
            mariadb_connection.close()
            print('[INFO] connection is closed')

def add_forwarding(address, forwarding, domain):
    login_data = mysql_login()
    # INSERT INTO forwardings (address, forwarding, domain, dest_domain,is_list, active)
    sql_insert_forwarding_cmd = (
        "INSERT INTO forwardings " 
        "(address, forwarding, domain, dest_domain,is_list, active) "
        "VALUES ('%s', '%s', '%s' '%s', 1, 1)") % (address, forwarding, domain, domain)
      
    # create connection object
    mariadb_connection = mariadb.connect(
        user=login_data[0],
        password=login_data[1],
        database='vmail')
    # create cursor object
    cursor = mariadb_connection.cursor()
    try:
        # insert values to DB
        cursor.execute(sql_insert_forwarding_cmd)
        # do a DB commit
        cursor.commit()
        print('Mailforwarding {} created succesfully'.format(address))
    except mariadb_connection.Error as err:
        print('Unable to insert Mailforwarding {} to Domain {}'.format(address, domain))
        print('[ERROR] {}').format(err)
        # do rollback operation
        print('Performing rollback')
        mariadb_connection.rollback()
    finally:
        if mariadb_connection.is_connected():
            cursor.close()
            mariadb_connection.close()
            print('[INFO] connection is closed')


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
        help='Remove mail alias in table alias and remove destination entry in table forwardings ')
    parser.add_argument(
        '-ft',
        '--forward-to',
        action='store_true',
        help='The email-address to forward mails to alias -> real address')

    global ARGS
    ARGS = parser.parse_args()
    
    if ARGS.list:
        domain_alias = get_alias(ARGS.domain)
        print(domain_alias)
    
    if ARGS.add:
        add_alias(ARGS.address, ARGS.domain)
        add_forwarding(ARGS.address, ARGS.forwarding, ARGS.domain)

