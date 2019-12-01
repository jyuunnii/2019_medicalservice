from flask import Flask, render_template, request, redirect, url_for
from pypg import helper
import psycopg2
import json


app = Flask(__name__)


#------------------------------------------------------- 로그인 및 사용자 타입 지정
@app.route('/')
def main():
  return render_template("main.html")

@app.route('/login', methods=["POST"])  
def login():
  try:
    email = request.form.get("email")
    password = request.form.get("password")

    print(f"{email}님이 로그인 했습니다.")
    
    result = helper.login("customer",email,password)
    rDict = result[0]
    rname = rDict['name']
    result="enter.html"

  except IndexError as e:
    print(e)
    rname=""
    result="main.html"

  return render_template(result, rname=rname)

@app.route('/new', methods=["POST"])
def new():
  try:
    name = request.form.get("name")
    phone = request.form.get("phone")
    email = request.form.get("email")
    password = request.form.get("password")
    print(helper.new("customer", name, phone, email, password))
    print(f"{name} 가입완료")
    result="가입 성공"

  except psycopg2.errors.UniqueViolation as e:
    print(e)
    result="가입 실패(중복 사용자, 이메일)"

  return render_template("main.html", result=result)


#사용자 타입 지정
@app.route('/hospital', methods=["POST"])
def typeh():
  name = request.form.get("name")
  customerType="hospital"
  print(helper.typeInsert("customer",name,customerType))
  return render_template("hospital-main.html", name=name)

@app.route('/pharmacy', methods=["POST"])
def typeph():
  name = request.form.get("name")
  customerType="pharmacy"
  print(helper.typeInsert("customer",name,customerType))
  return render_template("pharmacy-main.html", name=name)

@app.route('/patient', methods=["POST"])
def typept():
  name = request.form.get("name")
  customerType="patient"
  print(helper.typeInsert("customer",name,customerType))
  return render_template("patient-main.html",name=name)



#------------------------------------------------------- 병원
@app.route('/hospital')
def hospitalMain():
  return render_template("hospital-main.html")

#환자 관리
@app.route('/register', methods=["POST"])
def register():
  hospital = request.form.get("hospital")
  name = request.form.get("name")
  phone = request.form.get("phone")
  record = request.form.get("record")

  print(f"{name}님이 {hospital}의 신규 환자로 등록되었습니다.")
  print(helper.patientInsert("hospitalvisitrecord", name, phone, record, hospital))

  return render_template("hospital-main.html")

@app.route('/patient-search', methods=["POST"])
def select():
  try:
    name = request.form.get("name")
    phone = request.form.get("phone")
    hospital = request.form.get("hospital")
    result = helper.select("hospitalvisitrecord", name, phone, hospital)
    
    print(f"{name} 님이 검색되었습니다.")

  except:
    print("검색값을 입력해주세요.")

  return render_template("hospital-patient-list.html",result=result, hospital=hospital)

@app.route('/patient-delete', methods=["POST"])
def delete():
  try:
    name = request.form.get("name")
    hospital = request.form.get("hospital")

    print(helper.delete("hospitalvisitrecord", name, hospital))
    print(f"{name} 삭제")

  except:
    print("삭제할 데이터를 선택해주세요.")

  return render_template("hospital-patient-list.html",hospital=hospital)


#예약내역 확인
@app.route('/reserve-admin', methods=["POST"])
def admin():
  try:
    hospital = request.form.get("hospital")
    result = helper.reserve_list("reservation", hospital) 

    print(f"{hospital}의 예약내역 검색중")

    if(hospital is ""):
      result="no data"
      
  except:
    print("검색값을 입력해주세요.")

  return render_template("hospital-reserve-list.html", result=result, hospital=hospital)

#예약환자 방문확인
@app.route('/reserve-check', methods=["POST"])
def check():
  try:
    name = request.form.get("name")
    phone = request.form.get("phone")
    hospital = request.form.get("hospital")

    print(helper.check("hospitalvisitrecord", name, phone, hospital))
    print(f"{name} 방문확인")
  
  except:
    print("확인할 데이터를 선택해주세요.")

  return render_template("hospital-reserve-list.html", hospital=hospital)

@app.route('/reserve-delete', methods=["POST"])
def cancel():
  try:
    name = request.form.get("name")
    hospital = request.form.get("hospital")

    print(helper.delete("reservation", name, hospital))
    print(f"{name} 예약취소")

    result="예약 취소되었습니다."

  except:
    print("삭제할 데이터를 선택해주세요.")

  return result


#처방
@app.route("/prescribe", methods=["POST"])
def prescribe():
  hospital = request.form.get("hospital")
  return render_template("prescribe.html", hospital=hospital)

@app.route("/save", methods=["POST"])
def save():
  try:
    hospital = request.form.get("hospital")
    date = request.form.get("date")
    name = request.form.get("patient")
    medicine = request.form.get("medicine")
    volume = request.form.get("volume")
    times = request.form.get("times")
    period = request.form.get("period")

    print(helper.save("hospitalvisitrecord",hospital,date,name,medicine,volume,times,period))

  except psycopg2.errors.InvalidDatetimeFormat as e:
    print(e)
    hospital=""

  return render_template("prescribe.html", hospital=hospital)


@app.route("/register-hospital", methods=["POST"])
def registerHospital():
  name = request.form.get("name")
  address = request.form.get("address")
  drcnt = request.form.get("drcnt")
  subject = request.form.get("subject")
  timeweek = request.form.get("timeweek")
  timesat = request.form.get("timesat")

  print(helper.registerH("hospital",name,address,drcnt,subject,timeweek,timesat))

  return render_template("hospital-main.html")



#------------------------------------------------------- 약국
#예약내역 확인
@app.route('/reserve-admin-ph', methods=["POST"])
def adminMed():
  try:
    pharmacy = request.form.get("pharmacy")
    result = helper.reserve_list_ph("reservation", pharmacy) 

    print(f"{pharmacy}의 예약내역 검색중")

    if(hospital is ""):
      result="no data"
      
  except:
    print("검색값을 입력해주세요.")

  return render_template("pharmacy-reserve-list.html", result=result, pharmacy=pharmacy)


#예약환자 방문확인
@app.route('/reserve-check-ph', methods=["POST"])
def checkMed():
  try:
    name = request.form.get("name")
    pharmacy = request.form.get("pharmacy")

    print(helper.checkMed("hospitalvisitrecord", name, pharmacy))
    print(f"{name} 방문확인")
  
  except:
    print("확인할 데이터를 선택해주세요.")

  return render_template("pharmacy-reserve-list.html", pharmacy=pharmacy)

@app.route('/finish', methods={"POST"})
def finish():
  name = request.form.get("name")
  print(helper.finish("reservation", name))

  return render_template("pharmacy-reserve-list.html")


@app.route('/reserve-delete-ph', methods=["POST"])
def cancelMed():
  try:
    name = request.form.get("name")
    pharmacy = request.form.get("pharmacy")

    print(helper.deleteMed("reservation", name, pharmacy))
    print(f"{name} 예약취소")

    result="예약 취소되었습니다."

  except:
    print("삭제할 데이터를 선택해주세요.")

  return result

@app.route('/prescribe-ph', methods=["POST"])
def prescribeMed():
  try:
    name = request.form.get("name")
    pharmacy = request.form.get("pharmacy")
    
    result = helper.call("hospitalvisitrecord", name, pharmacy)
  
  except:
    print("error")
  
  return render_template("prescribe-done.html", result=result, pharmacy=pharmacy)


@app.route("/save-ph", methods=["POST"])
def saveMed():
  hospital = request.form.get("hospital")
  patient = request.form.get("patient")
  pharmacy = request.form.get("pharmacy")
  date = request.form.get("date")
  text = request.form.get("text")
  
  print(helper.saveMed("hospitalvisitrecord",pharmacy,date,text,hospital,patient))

  return render_template("prescribe-done.html")





#------------------------------------------------------- 환자
#병원 검색
@app.route('/select-hospital-name', methods=["POST"])
def selectHospitalName():
  name = request.form.get("name")
  result = helper.selectHospitalName("hospital", name)
  print(f"{name} 검색중")

  return render_template("patient-hospital-list.html", result=result)

@app.route('/select-hospital-address', methods=["POST"])
def selectHospitalAddress():
  address = request.form.get("address")
  result = helper.selectHospitalAddress("hospital", address)
  print(f"{address} 검색중")

  return render_template("patient-hospital-list.html", result=result)

@app.route('/select-hospital-subject', methods=["POST"])
def selectHospitalSubject():
  subject = request.form.get("subject")
  result = helper.selectHospitalSubject("hospital", subject)

  print(f"{subject} 검색중")

  return render_template("patient-hospital-list.html", result=result)


#약국 검색
@app.route('/select-pharmacy-name', methods=["POST"])
def selectPharmacyName():
  name = request.form.get("phname")
  result = helper.selectPharmacyName("pharmacy", name)
  print(f"{name} 검색중")

  return render_template("patient-pharmacy-list.html", result=result)

@app.route('/select-pharmacy-address', methods=["POST"])
def selectPharmacyAddress():
  address = request.form.get("phaddress")
  result = helper.selectPharmacyAddress("pharmacy", address)
  print(f"{address} 검색중")

  return render_template("patient-pharmacy-list.html", result=result)


#자주가는 병원 추가
@app.route('/send', methods=["POST"])
def send():
  hospital = request.form.get("name")
  customer = request.form.get("customer")
  print(helper.send("customer", customer, hospital))
  print(f"{hospital}을 {customer}님의 자주가는 병원 목록에 추가했습니다.")

  return render_template("patient-hospital-list.html")

#최근 병원 방문 조회
@app.route('/recent', methods=["POST"])
def recent():
  customer = request.form.get("customer")
  result=helper.recent("reservation",customer)
  print(f"{customer}님의 최근 병원 방문 기록 조회중")
  
  return render_template("patient-hospital-list.html", result=result)

#병원예약
@app.route('/reserve', methods=["POST"])
def reserve():
  hospital = request.form.get("name")
  patient = request.form.get("patient")
  phone = request.form.get("phone")
  symptom = request.form.get("patient-symptom")
  time = request.form.get("time")
  print(helper.reserve("reservation", patient, phone, symptom, hospital, time))
  print(f"{patient}님의 {hospital} 예약 진행중")

  return render_template("patient-hospital-list.html")


#약국예약
@app.route('/reserve-med', methods=["POST"])
def reserveMed():
  pharmacy = request.form.get("name")
  patient = request.form.get("patient")
  phone = request.form.get("phone")
  time = request.form.get("time")
  print(helper.reserveMed("reservation", patient, phone, pharmacy, time))
  print(f"{patient}님의 {pharmacy} 예약 진행중")

  return render_template("patient-pharmacy-list.html")

#지도 검색
@app.route('/map', methods=["POST"])
def mapping():
  try:
    name = request.form.get("name")
    result = helper.map("hospital",name)
    print(result)
    result = result[0]
    result = result['address']
    print(f"{name} 지도 위치 검색중")
  except:
    print("주소값이 없습니다.")
  
  return render_template("map.html",result=result)


#처방내역 조회
@app.route('/record', methods=["POST"])
def record():
  try:
    name = request.form.get("name")
    result = helper.record("hospitalvisitrecord", name)
  
  except:
    print("처방 내역이 없습니다.")
  
  return render_template("patient-prescription.html", result=result, name=name)


if __name__ == ("__main__"):
  # docker
  app.run(debug=True, host='0.0.0.0', port=5090)
  # other
  #app.run(debug=True)



