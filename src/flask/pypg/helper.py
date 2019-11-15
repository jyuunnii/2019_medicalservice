import psycopg2 as pg
import psycopg2.extras #field명을 알 때 활용

#docker inside
db_connector = {
    'host': "postgres",
    'user': "dbuser",
    'dbname': "dbapp",
    'password': "1234"
}

connect_string = "host={host} user={user} dbname={dbname} password={password}".format(
    **db_connector)


def ykiho_list(table_name):
    sql = f'''SELECT hospitalid FROM {table_name};
    '''
    print(sql)
    try:
        conn=pg.connect(connect_string) 
        cur=conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(sql)
        result=cur.fetchall()  
       
        conn.close()
        return result
    except Exception as e:
        print(e)
        return[]


#병원
def patientInsert(table_name, name, phone, record):
    sql = f'''INSERT INTO {table_name} 
        VALUES('{name}', '{phone}', '{record}');
        '''
    print(sql)
    try:
        conn = pg.connect(connect_string) 
        cur = conn.cursor() 
        cur.execute(sql) 

        conn.commit()
        conn.close()
    except pg.OperationalError as e:
        print(e)
        return -1
    
    return 0

def patients_list(table_name):
    sql = f'''SELECT name, phone, record FROM {table_name};
    '''
    print(sql)
    try:
        conn=pg.connect(connect_string) 
        cur=conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(sql)
        result=cur.fetchall() 
      
        conn.close()
        return result
    except Exception as e:
        print(e)
        return[]




def select(table_name, name):
    sql = f'''SELECT name, phone, record FROM {table_name} WHERE name LIKE '%{name}%';
    '''
    print(sql)
    try:
        conn=pg.connect(connect_string) 
        cur=conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(sql)
        result=cur.fetchall()  
       
        conn.close()
        return result
    except Exception as e:
        print(e)
        return[]


def delete(table_name, name):
    sql = f'''DELETE FROM {table_name} WHERE name='{name}';
    '''
    print(sql)
    try:
        conn = pg.connect(connect_string) 
        cur = conn.cursor() 
        cur.execute(sql) 

        conn.commit()
        conn.close()
    except pg.OperationalError as e:
        print(e)
        return -1
    
    return 0


