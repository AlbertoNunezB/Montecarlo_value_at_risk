import sys
import psycopg2
from Montecarlo_value_at_risk import Montecarlo_value_at_risk

def main():
    #Get data from database
    db_host     =   'an_ip'
    db_port     =   5432
    db_db       =   'database_name'
    db_user     =   'database_user'
    db_pass     =   'database_pass'

    rows        =   None
    try:
        connection      =   psycopg2.connect(user=db_user,password=db_pass,host=db_host,port=db_port,database=db_db)
        cursor          =   connection.cursor()
        cursor.execute("SELECT * FROM A_CERTAIN_TABLE")
        rows            =   cursor.fetchall()
    except(Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        sys.exit(1)
    finally:
        if (connection):
            cursor.close()
            connection.close()
    data = [(x[0], x[1], x[2], x[3]) for x in rows]
    montecarlo = Montecarlo_value_at_risk(raw_data=data)
    num_iterations = 10000
    montecarlo.value_at_risk(num_iterations)
    montecarlo.plot()
if(__name__=='__main__'):
    main()