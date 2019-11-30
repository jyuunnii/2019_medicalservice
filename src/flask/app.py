from flask import Flask, render_template, request, redirect, url_for
from pypg import helper
import json

app = Flask(__name__)

#로그인 및 사용자 타입 지정
@app.route('/')
def main():
  return render_template("main.html")

@app.route('/login', methods=["POST"])  
def login():
  email = request.form.get("email")
  password = request.form.get("password")

  print(f"{email}님이 로그인 했습니다.")
  
  result = helper.login("customer",email,password)
  rDict = result[0]
  rname = rDict['name']

  return render_template("enter.html", rname=rname)


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



#병원
@app.route('/hospital')
def hospitalMain():
  return render_template("hospital-main.html")

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
    hospital = request.form.get("hospital")
    result = helper.select("hospitalvisitrecord", name, hospital)
    
    print(f"{name} 님이 검색되었습니다.")

  except:
    print("검색값을 입력해주세요.")

  return render_template("hospital-patient-list.html",result=result, h=hospital)


@app.route('/patient-delete', methods=["POST"])
def delete():
  try:
    name = request.form.get("name")
    hospital = request.form.get("hospital")

    print(helper.delete("hospitalvisitrecord", name, hospital))
    print(f"{name} 삭제")

    result="삭제되었습니다."
  except:
    print("삭제할 데이터를 선택해주세요.")

  return result


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

  return render_template("hospital-reserve-list.html", result=result, h=hospital)

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

@app.route("/prescribe")
def prescribe():
  return render_template("prescribe.html")



#환자
#병원 검색
@app.route('/select-hospital-name', methods=["POST"])
def selectHospitalName():
  name = request.form.get("name")
  result = helper.selectHospitalName("hospital", name)
  print(f"{name} 검색중")

  return render_template("patient-hospital-list.html", result=result)

@app.route('/select-hospital-subject', methods=["POST"])
def selectHospitalSubject():
  subject = request.form.get("subject")
  result = helper.selectHospitalSubject("hospital", subject)

  print(f"{subject} 검색중")

  return render_template("patient-hospital-list.html", result=result)

@app.route('/select-hospital-address', methods=["POST"])
def selectHospitalAddress():
  address = request.form.get("address")
  result = helper.selectHospitalAddress("hospital", address)
  print(f"{address} 검색중")

  return render_template("patient-hospital-list.html", result=result)

@app.route('/send', methods=["POST"])
def send():
  name = request.form.get("name")
  customer = request.form.get("customer")
  print(helper.send("customerrecord",name, customer))
  print(f"{name}을 {customer}님의 자주가는 병원 목록에 추가했습니다.")

  return render_template("patient-hospital-list.html")

@app.route('/recent', methods=["POST"])
def recent():
  customer = request.form.get("customer")
  result=helper.recent("customerrecord",customer)
  print(f"{customer}님의 최근 병원 방문 기록 조회중")
  
  return render_template("patient-hospital-list.html", result=result)

@app.route('/reserve', methods=["POST"])
def reserve():
  hospital = request.form.get("name")
  patient = request.form.get("patient")
  phone = request.form.get("patient-phone")
  symptom = request.form.get("patient-symptom")
  time = request.form.get("time")
  print(helper.reserve("reservation", patient, phone, symptom, hospital, time))
  print(f"{patient}님의 {hospital} 예약 진행중")

  return render_template("patient-hospital-list.html")

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





if __name__ == ("__main__"):
  # docker
  app.run(debug=True, host='0.0.0.0', port=5090)
  # other
  #app.run(debug=True)



