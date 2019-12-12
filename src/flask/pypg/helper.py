import psycopg2 as pg
import psycopg2.extras  

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

### 로그인

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

def new(table_name, name, phone, email, password):
    sql = f'''INSERT INTO {table_name} 
        VALUES('{name}','{phone}','{password}','','','{email}');
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



#사용자 타입 지정
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
    

#### 병원

#신규 환자 등록
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

#환자 검색
def select(table_name, name, phone, hospital):
    sql = f'''SELECT name, phone, description, pdate FROM {table_name} WHERE name LIKE '%{name}%' AND hospital='{hospital}' AND phone LIKE '%{phone}%';
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

#환자 관리 및 예약 삭제
def delete(table_name, name, hospital):
    sql = f'''DELETE FROM {table_name} WHERE name='{name}' AND hospital LIKE '%{hospital}%';
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

#예약 조회
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

#처방
def save(table_name, hospital, date, name, medicine, volume, times, period):
    sql = f'''UPDATE {table_name} SET pdate='{date}', pmedicine='{medicine}', pvolume='{volume}', ptimes='{times}', pperiod='{period}' 
    WHERE name='{name}' AND hospital='{hospital}';
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

#예약환자 등록 (방문 확인)
def check(table_name, name, phone, hospital):
    sql = f'''INSERT INTO {table_name} 
        VALUES('{name}','{phone}','','{hospital}');
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

def registerH(table_name, name, address, drcnt, subject, timeweek, timesat):
    sql = f'''INSERT INTO {table_name} 
        VALUES('{name}','{address}','','','{drcnt}','','{subject}','{timeweek}','{timesat}');
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


### 약국
#예약 조회
def reserve_list_ph(table_name, pharmacy):
    sql = f'''SELECT name, phone, time, prescription FROM {table_name} WHERE pharmacy LIKE '%{pharmacy}%';
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

#예약환자 등록 (방문 확인)
def checkMed(table_name, name, pharmacy):
    sql = f'''UPDATE {table_name} SET pharmacy='{pharmacy}' WHERE name='{name}';
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


#환자 관리 및 예약 삭제
def deleteMed(table_name, name, pharmacy):
    sql = f'''DELETE FROM {table_name} WHERE name='{name}' AND pharmacy LIKE '%{pharmacy}%';
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

def call(table_name, name, pharmacy):
    sql = f'''SELECT name, hospital, pdate, ptimes, pmedicine, pvolume, ptimes, pperiod FROM {table_name} 
    WHERE name=(SELECT name FROM reservation WHERE pharmacy LIKE '%{pharmacy}%' AND name='{name}' LIMIT 1) LIMIT 1;
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

#처방
def saveMed(table_name, pharamcy, date, text, hospital, patient):
    sql = f'''UPDATE {table_name} SET pharmacy='{pharamcy}', phdate='{date}', description='{text}' 
    WHERE name='{patient}' AND hospital LIKE '%{hospital}%';
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

#처방완료
def finish(table_name, name):
    sql = f'''UPDATE {table_name} SET prescription='완료' WHERE name='{name}';
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

### 환자

#병원 검색
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

#약국 검색
def selectPharmacyName(table_name, name):
    sql = f'''SELECT name,address,tel,prescribe FROM {table_name} WHERE name LIKE '%{name}%';
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

def selectPharmacyAddress(table_name, address):
    sql = f'''SELECT name,address,tel,prescribe FROM {table_name} WHERE address LIKE '%{address}%';
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


#자주가는 병원 등록
def send(table_name, customer, hospital):
    sql = f'''UPDATE {table_name} SET preferlist=((SELECT preferlist FROM {table_name} WHERE name='{customer}'),'{hospital}')
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

#최근 방문한 병원 조회
def recent(table_name,customer):
    sql = f'''SELECT name,address,drcnt,subject,timeweek,timesat  
    FROM hospital WHERE name=(
        SELECT hospital
        FROM {table_name} WHERE name LIKE '%{customer}%' LIMIT 1
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

#병원 예약
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

#약국 예약
def reserveMed(table_name, patient, phone, pharmacy, time):
    sql = f'''INSERT INTO {table_name}
    VALUES('{patient}','{phone}','','','{time}','{pharmacy}');
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

#지도 검색
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

#처방 내역 조회
def record(table_name, name):
    sql = f'''SELECT name, hospital, pdate, pmedicine, pvolume, ptimes, pperiod, pharmacy, phdate, description  FROM {table_name} WHERE name='{name}';
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
