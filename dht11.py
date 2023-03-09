import Adafruit_DHT
import time
#from DB import Database #DB
import pymysql as ps


dht = Adafruit_DHT.DHT11 #dht변수선언
dhtPin = 14 # dht 연결 핀번호

#ps = Database() #현재시간

#DB 연결 시킨후 변수에 저장하고 변수에 연결 커서 저장하기
conn = ps.connect(host = 'localhost',user='hyun',password='1234',db='P01',charset='utf8')
curs = conn.cursor()

#온도와 습도 담을 그릇 생성
humi,temp = Adafruit_DHT.read_retry(dht,dhtPin)
if humi is not None and temp is not None:
	while True:
		humi,temp = Adafruit_DHT.read_retry(dht,dhtPin)
		now = time.localtime()
		nowtime=("%04d/%02d/%02d %02d:%02d:%02d" %(now.tm_year,now.tm_mon,now.tm_mday,now.tm_hour,now.tm_min,now.tm_sec))
		#print('temp = {0:0.1f}*C humi={1:0.1f}%'.format(temp,humi))
		#온도 습도 시간 순으로 표시
		humi = (round(humi,2))
		temp = (round(temp,2))
		print(humi,temp)
		#print(humi,temp)
		#데이터 베이스에 온도 습도 시간 인설트문 실행.
		sql = """insert into temp5(temp,humi,date) values(%s,%s,%s) """
		val = (temp,humi,nowtime )
		print(val)
		curs.execute(sql,val)
		time.sleep(1)

		#sql문 실행하기
		#curs.execute(sql)
		#sql문 저장시키기
		conn.commit()

else:
	print("Failed to get reading. Try again!!")





