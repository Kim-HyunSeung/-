from flask import request
import time
import pymysql as ps
from flask import Flask,render_template,url_for,session,request,redirect

conn = ps.connect(host = 'localhost',user='hyun',password='1234',db='P01',charset='utf8')
curs = conn.cursor()

app = Flask(__name__)
app.secret_key = "hyun1111"


sql = """SELECT * from login"""
curs.execute(sql)
sql_all=curs.fetchall()
conn.commit()
list = sql_all

for i in list:
	if i == ('hyun','1234'):
		ID = (i[0])
		PW = (i[1])

@app.route("/")
def home():
	if "userID" in session:
		return render_template("home.html",username = session.get("userID"),login = True)
	else:
		return render_template("home.html",login = False)

@app.route("/login", methods = ["GET"])
def login():
	global ID,PW
	_id_ = request.args.get("loginId")
	_password_ = request.args.get("loginPw")

	if ID == _id_ and _password_ == PW:
		session["userID"] = _id_
		sql = """SELECT * from loginflag4 order by date desc limit 10"""
#SELECT COUNT(*) FORM 로그인정보테이블 WHERE 아이디 = 입력한 아이디 AND 비밀번호 = 입력한 비밀번호
		curs.execute(sql)
		sql_all=curs.fetchall()
		conn.commit()

		success = "로그인에 성공하셨습니다."
#		if success is not None and flag2 ==0:
		if success is not None and ID ==_id_ and _password_ == PW:
			session["userID"] = _id_
			now = time.localtime()
			nowtime=("%04d/%02d/%02d %02d:%02d:%02d" %(now.tm_year,now.tm_mon,now.tm_mday,now.tm_hour,now.tm_min,now.tm_sec))
      	#sql 쿼리문 작성
			sql = """insert into loginflag4(success,date) values(%s,%s) """
			val = (success,nowtime)
      	#sql query 실행
			curs.execute(sql,val)
			time.sleep(1)
			conn.commit()
		return render_template('home.html',list=sql_all,login =True) 

	else:
		sql = """SELECT * from loginflag3 order by date desc limit 10"""
		curs.execute(sql)
		sql_all=curs.fetchall()
		conn.commit()

		fail = "로그인에 실패하셨습니다."
		if fail is not None:
			now = time.localtime()
			nowtime=("%04d/%02d/%02d %02d:%02d:%02d" %(now.tm_year,now.tm_mon,now.tm_mday, now.tm_hour,now.tm_min,now.tm_sec))
			sql = """insert into loginflag3(fail,date) values(%s,%s) """
			val = (fail,nowtime)
			curs.execute(sql,val)
			time.sleep(1)
			conn.commit()
		return render_template("home.html",list=sql_all,login=False)	


@app.route("/temp")
def temp():
	while True:
		sql = """SELECT * from temp5 order by date desc limit 10 """
		curs.execute(sql)
		sql_all=curs.fetchall()
		conn.commit()
		return render_template('index.html',list=sql_all)

@app.route("/logout")
def logout():
	session.pop("userID")
	return redirect(url_for("home"))

if __name__ == '__main__':
	app.run(host='0.0.0.0',port = '8080',debug='True')
