import requests
import urllib.request as ul
import json
import csv
import xmltodict

#의료기관별상세정보서비스
#ykiho = pk

#병원정보:이름, 주소, 홈페이지, 위치좌표 xy
ServiceKey = "LkNquBkUjN%2B0CaCfbHYpCajDMmcN3aWbcaKNnnc1KNZjy7QdVJ7kkJIjqHIi7B2EsFOje4DVA9uU5nonq1xTPg%3D%3D"
pageNo="1"
numOfRows="2" #total rows=17670
url="http://apis.data.go.kr/B551182/hospInfoService/getHospBasisList?pageNo="+pageNo+"&numOfRows="+numOfRows+"&sidoCd=110000&ServiceKey="+ServiceKey


request = ul.Request(url)

response = ul.urlopen(request)

rescode = response.getcode()

if(rescode == 200):
    responseData = response.read() #xml

    rD = xmltodict.parse(responseData)
    rDJ = json.dumps(rD)
    rDD = json.loads(rDJ) #dict
    
    w_data = rDD["response"]["body"]["items"]["item"] #list [{},{},{},...]
    
    for a in w_data:
        try:
            hospitalId = a['ykiho']
            hospitalNm = a['yadmNm']
            hospitalAd = a['addr']
            hospitalXpos = a['XPos']
            hospitalYpos = a['YPos']
            hospitalDrTotCnt = a['drTotCnt']

            values =[]
            values.extend((hospitalNm, hospitalAd, hospitalXpos, hospitalYpos, hospitalDrTotCnt, hospitalId))

            with open("./hospital.csv", "a+") as f:
                w = csv.writer(f)
                #w.writeheader()           
                w.writerow(values)

        except KeyError:
            print(KeyError)