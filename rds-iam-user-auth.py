import boto3
import pymysql
import sys
import os

# This script use a previously created IAM Role and associated with a DB User
# Useful to control the access to a DB using IAM
# Follow these instructions:
# https://gist.github.com/15be79777e619fddc364fab76e40fd3e

# rds_endpoint = 'my-db-cluster.cluster-12345678.us-east-1.rds.amazonaws.com'
# db_user = 'testapp'
# db_name = 'testdb'

def app():
    rds_endpoint = os.environ['RDSHOST']
    db_name = os.environ['DBNAME']
    db_user = os.environ['DBUSER']

    rds = boto3.client('rds',region_name='us-east-1')
    token = rds.generate_db_auth_token(rds_endpoint,3306, db_user)
    ssl = {'ca': 'ssl/rds-combined-ca-bundle.pem'}
    con = pymysql.connect(host=rds_endpoint, port=3306, user=db_user, password=token, ssl=ssl, db=db_name)

    try:
        cursor = con.cursor()
        sql = "SELECT * FROM users ORDER BY id_user ASC"
        cursor.execute(sql)
        for row in cursor:
            print("User Id: ", row[0])
            print("Username: ", row[1])
    finally:
        cursor.close()


# Program start from here
if __name__ == '__main__':
    try:
        app()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        sys.exit()