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
  return render_template("hospital-main.html")

@app.route('/pharmacy', methods=["POST"])
def typeph():
  name = request.form.get("name")
  customerType="pharmacy"
  print(helper.typeInsert("customer",name,customerType))
  return render_template("pharmacy-main.html")

@app.route('/patient', methods=["POST"])
def typept():
  name = request.form.get("name")
  customerType="patient"
  print(helper.typeInsert("customer",name,customerType))
  return render_template("patient-main.html")



#병원
@app.route('/hospital')
def hospitalMain():
  return render_template("hospital-main.html")

@app.route('/register', methods=["POST"])
def hosRegister():
  name = request.form.get("name")
  phone = request.form.get("phone")
  record = request.form.get("record")

  print(f"{name}님이 신규 환자로 등록되었습니다.")
  print(helper.patientInsert("patient", name, phone, record))

  return render_template("hospital-main.html")

@app.route("/patient-list")
def patients_list_rest():
  result = helper.patients_list("patient") 
  result = json.dumps(result)

  return result

@app.route('/patient-search', methods=["POST"])
def select():
  name = request.form["name_to_search"]
  result = helper.select("patient", name)
  
  print(f"{name} 님이 검색되었습니다.")

  #result = json.dumps(result, ensure_ascii=False)
  rDict = result[0]
  pname = rDict['name']
  pphone = rDict['phone']
  precord = rDict['record']

  result = "이름 : "+pname+"  핸드폰 번호 : "+pphone+"  진료 기록 : "+precord
  
  return result

@app.route('/patient-delete', methods=["POST"])
def delete():
    name = request.form["name_to_delete"]

    print(f"{name} 삭제")
    print(helper.delete("patient",name))

    return render_template("hospital-main.html")

@app.route("/patient-reserve-list")
def patients_reserve_list():
  result = helper.patients_list("reservation") 
  result = json.dumps(result)

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

  return render_template("list.html", result=result)

@app.route('/select-hospital-subject', methods=["POST"])
def selectHospitalSubject():
  subject = request.form.get("subject")
  result = helper.selectHospitalSubject("hospital", subject)

  print(f"{subject} 검색중")

  return render_template("list.html", result=result)

@app.route('/select-hospital-address', methods=["POST"])
def selectHospitalAddress():
  address = request.form.get("address")
  result = helper.selectHospitalAddress("hospital", address)
  print(f"{address} 검색중")

  return render_template("list.html", result=result)

@app.route('/send', methods=["POST"])
def send():
  name = request.form.get("name")
  print(f"{name}을 자주가는 병원 목록에 추가했습니다.")
  print(helper.send("preferlist",name))

  return render_template("list.html")




if __name__ == ("__main__"):
  # docker
  app.run(debug=True, host='0.0.0.0', port=5090)
  # other
  #app.run(debug=True)



