import requests
import urllib.request as ul
from urllib.error import HTTPError
import json
import csv
import xmltodict
from pypg import helper
#의료기관별상세정보서비스


try:
    lists = helper.ykiho_list("hos") #table_name
    result = json.dumps(lists) #string
    a = json.loads(result) #list

    for key in a:
        hospitalId = key['hospitalid']

        ServiceKey = "ohEpJQJYPNYJNVJbBM%2F9V48%2FaUBGwhwVsN4cw0nHeSqXDAeZMHwjlfeAKoen40SxCv5Txz4ek01UgMcmSAZL6w%3D%3D"
        # pageNo="1"
        # numOfRows="25" 
        url="http://apis.data.go.kr/B551182/medicInsttDetailInfoService/getMdlrtSbjectInfoList?kiho="+hospitalId+"&ServiceKey="+ServiceKey


        request = ul.Request(url)
        response = ul.urlopen(request)
        rescode = response.getcode()

        if(rescode == 200):
            responseData = response.read() #xml

            rD = xmltodict.parse(responseData)
            rDJ = json.dumps(rD)
            rDD = json.loads(rDJ) #dict
            
            w_data = rDD['response']['body']['items']['item'] #list [{},{},{},...]
            subjects=[]
            
            #진료과목 2과목 이상
            if type(w_data) is list:
                for a in w_data:
                    try:
                        hospitalSbj = a['dgsbjtCdNm']
                        hospitalSbjDrTotCnt = a['dgsbjtPrSdrCnt']

                        subjects.append(hospitalSbj)

                        # with open("./subject.csv", "a+") as f:
                        #     w = csv.writer(f)
                        #     #w.writeheader()          
                        #     w.writerow(values)

                    except KeyError:
                        print(KeyError)

                with open("./subject.csv", "a+") as f:
                    w = csv.writer(f)
                    w.writerow(subjects)
            
            #진료과목 1과목
            elif type(w_data) is dict:
                print("진료과목 1개")
                try:
                    hospitalSbj = w_data.get('dgsbjtCdNm')
                    subjects.append(hospitalSbj)

                    with open("./subject.csv", "a+") as f:
                        w = csv.writer(f)
                        w.writerow(subjects)
                    
                except KeyError:
                    print(KeyError)
            
            else:
                print("No data..")
            
        except TypeError:
            print(TypeError)
            print(key)
        
        except KeyError:
            print(KeyError)
            print(key)

except HTTPError as e:
    print(e)