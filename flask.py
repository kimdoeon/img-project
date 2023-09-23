from flask import Flask, render_template, request, redirect, url_for
from flaskext.mysql import MySQL
from werkzeug.utils import secure_filename
 
import os
 
mysql = MySQL()
app = Flask(__name__)
 
# 데이터베이스 값 설정
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'image'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.secret_key = "ABCDEFG"
mysql.init_app(app)
 
@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('main.html')
 
@app.route('/fileUpload', methods = ['GET', 'POST'])
def file_upload():
    if request.method == 'POST':
        f = request.files['file']
        f.save('static/uploads/' + secure_filename(f.filename))
        files = os.listdir("static/uploads")
		
        conn = mysql.connect()
        cursor = conn.cursor()
        # 파일명과 파일경로를 데이터베이스에 저장함
        sql = "INSERT INTO images (image_name, image_dir) VALUES ('%s', '%s')" % (secure_filename(f.filename), '../static/uploads/'+secure_filename(f.filename))
        cursor.execute(sql)
        data = cursor.fetchall()
        
        if not data:
            conn.commit()
        
            return redirect(url_for("view"))
 
        else:
            conn.rollback()
            return 'upload failed'
    
 
@app.route('/view', methods = ['GET', 'POST'])
def view():
    conn = mysql.connect()  # DB와 연결
    cursor = conn.cursor()  # connection으로부터 cursor 생성 (데이터베이스의 Fetch 관리)
    sql = "SELECT image_name, image_dir FROM images"  # 실행할 SQL문
    cursor.execute(sql)  # 메소드로 전달해 명령문을 실행
    data = cursor.fetchall()  # 실행한 결과 데이터를 꺼냄

    data_list = []
    
    data_dic = {
        'name' : data[-1][0],
        'dir' : data[-1][1]
    }
    
    data_list.append(data_dic)  # 완성된 딕셔너리를 list에 넣음

    cursor.close()
    conn.close()
 
    return render_template('view.html', data_list=data_list)  # html을 렌더하며 DB에서 받아온 값들을 넘김
 
if __name__ == '__main__':
    app.run(port=5000)
 