from flask import Flask, render_template, request, redirect, url_for
from pypg import helper
import json


app = Flask(__name__)

@app.route('/')
def login():
  return render_template("login.html")

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
@app.route('/patient')
def patientMain():
  return render_template("patient-main.html")

@app.route('/pharmacy')
def pharmacyMain():
  return render_template("pharmacy-main.html")



if __name__ == ("__main__"):
  # docker
  app.run(debug=True, host='0.0.0.0', port=5090)
  # other
  #app.run(debug=True)



