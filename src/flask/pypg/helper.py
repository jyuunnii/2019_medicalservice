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

#로그인
def login(table_name, email, password):
    sql = f'''SELECT name FROM {table_name} WHERE email='{email}' AND password='{password}';
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

def typeInsert(table_name, name, customertype):
    sql = f'''UPDATE {table_name} SET customertype='{customertype}' WHERE name='{name}';
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
    

#병원
def patientInsert(table_name, name, phone, record, hospital):
    sql = f'''INSERT INTO {table_name} 
        VALUES('{name}','{phone}', '{record}','{hospital}');
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

def select(table_name, name, hospital):
    sql = f'''SELECT name, phone, description FROM {table_name} WHERE name LIKE '%{name}%' AND hospital='{hospital}';
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


def delete(table_name, name, hospital):
    sql = f'''DELETE FROM {table_name} WHERE name='{name}' AND hospital='{hospital}';
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

def reserve_list(table_name, hospital):
    sql = f'''SELECT name, phone, symptom, time FROM {table_name} WHERE hospital LIKE '%{hospital}%';
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


#환자
def selectHospitalName(table_name, name):
    sql = f'''SELECT name,address,drcnt,subject,timeweek,timesat  
    FROM {table_name} WHERE name LIKE '%{name}%';
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

def selectHospitalAddress(table_name, address):
    sql = f'''SELECT name,address,drcnt,subject,timeweek,timesat  
    FROM {table_name} WHERE address LIKE '%{address}%';
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

def selectHospitalSubject(table_name, subject):
    sql = f'''SELECT name,address,drcnt,subject,timeweek,timesat  
    FROM {table_name} WHERE subject LIKE '%{subject}%';
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

def send(table_name, name, customer):
    sql = f'''UPDATE {table_name} SET prefervisitlist=((SELECT prefervisitlist FROM {table_name} WHERE name='{customer}'),'{name}')
        WHERE name='{customer}';
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

def recent(table_name,customer):
    sql = f'''SELECT name,address,drcnt,subject,timeweek,timesat  
    FROM hospital WHERE name=(
        SELECT hospital
        FROM reservation WHERE name LIKE '%{customer}%'
    );
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

def reserve(table_name, patient, phone, symptom, hospital, time):
    sql = f'''INSERT INTO {table_name}
    VALUES('{patient}','{phone}','{symptom}','{hospital}','{time}')
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

    
def map(table_name, name):
    sql = f'''SELECT address FROM hospital WHERE name='{name}';
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