from flask import Flask,render_template,session,flash,redirect,request,send_from_directory,url_for,jsonify
import mysql.connector, os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from datetime import datetime
import datetime

app=Flask(__name__)
app.config['SECRET_KEY']='attendance system'


db = mysql.connector.connect(host="localhost", user="root", passwd="", database="dermatology")
cur=db.cursor()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/admin', methods=['POST','GET'])
def admin():
    if request.method=='POST':
        useremail = request.form['userEmail'] 
        password = request.form['userPassword']

       
        if useremail=="admin@gmail.com" and password=="admin":
            flash("Welcome Admin","success")
            return render_template('admindash.html')
        else:
            flash("Invalid data entered","danger")
            return render_template('admin.html')
    return render_template('admin.html')


@app.route('/signin', methods=['POST','GET'])
def signin():
    if request.method=='POST':
        useremail = request.form['userEmail'] 
        password = request.form['userPassword']

        sql="select * from users where user_Email='"+useremail+"' and Password='"+password+"'"
        cur.execute(sql)
        data=cur.fetchall()
        db.commit()

        if data==[]:
            flash("Invalid data entered","danger")
            return render_template('signin.html')
        else:
           
            session['useremail']=useremail
            session['username']=data[0][1]
            flash("welcome ","success")
            return render_template('upload.html')
    return render_template('signin.html')

@app.route('/contact',methods=["POST","GET"])
def contact():
    if request.method=='POST':
        username=request.form['userName']
        useremail = request.form['userEmail']       
        password = request.form['userPassword']
        mobile = request.form['userPhone']
        address = request.form['userAddr']

        sql="select * from users where user_Email='%s' "%(useremail)
        cur.execute(sql)
        data=cur.fetchall()
        db.commit()
        if data==[]:
            sql = "insert into users(user_Name,user_Email,Password,user_Phone,user_Addr) values(%s,%s,%s,%s,%s)"
            val=(username,useremail,password,mobile,address)
            cur.execute(sql,val)
            db.commit()
            flash("User registered Successfully","success")
            return render_template("contact.html")
        else:
            flash("Details already Exists","warning")
            return render_template("contact.html")
        
    return render_template('contact.html')

@app.route('/userdash')
def userdash():
    return render_template('admindash.html')

import pickle 
@app.route("/upload", methods=["POST","GET"])
def upload():
    print('a')
    if request.method=='POST':
        myfile=request.files['file']
        age=float(request.form['age'])
        gender=float(request.form['gender'])
        days=float(request.form['day'])
        bmi=float(request.form['bmi'])
        smoking=float(request.form['smoking'])
        infection=float(request.form['infection'])
        fn=myfile.filename
        mypath=os.path.join('static/disease/', fn)
        myfile.save(mypath)
        print(mypath)
        lee=[age,gender,days,bmi,smoking,infection]
        filename = (r'models/LinearDiscriminantAnalysis.sav')
        model = pickle.load(open(filename, 'rb'))
        result =model.predict([lee])
        result=result[0]
        if result==0:
            msg1 = 'High'
        elif result==1:
            msg1= 'Low'
        else:
            msg1= 'Medium'
        accepted_formated=['jpg','png','jpeg','jfif','JPG']
        if fn.split('.')[-1] not in accepted_formated:
            flash("Image formats only Accepted","Danger")
            return render_template("upload.html")
        new_model = load_model(r"models/mobilenet.h5")
        test_image = image.load_img(mypath, target_size=(256, 256))
        test_image = image.img_to_array(test_image)
        test_image = test_image/255
        test_image = np.expand_dims(test_image, axis=0)
        result = new_model.predict(test_image)
        print(np.argmax(result))
        classes=['Actinic Keratosis', 'Basal Cell Carcinoma', 'Dermatofibroma', 'Melanoma', 'Nevus', 'Pigmented Benign Keratosis', 'Seborrheic Keratosis', 'Squamous Cell Carcinoma', 'Vascular Lesion']
        prediction=classes[np.argmax(result)]
        print(prediction)
        if prediction=="Actinic Keratosi":
            msg="Actinic Keratosis: This condition is primarily caused by long-term exposure to ultraviolet (UV) light, either from the sun or artificial sources like tanning beds. It's considered a precancerous condition because it can sometimes develop into squamous cell carcinoma."
            remedy="Treatment often includes cryotherapy (freezing the lesion), topical creams (like 5-fluorouracil, imiquimod), chemical peels, or laser therapy. The choice of treatment depends on the number and extent of skin lesions."
        elif prediction=="Basal Cell Carcinoma":
            msg="Basal Cell Carcinoma (BCC): The primary cause of BCC is long-term exposure to UV radiation from the sun or tanning beds. People with fair skin, light hair and eye color, and those with a history of sunburns or excessive sun exposure are at higher risk." 
            remedy="Common treatments include surgical excision, Mohs surgery (a precise surgical technique to remove the cancer), cryotherapy, radiation therapy, and topical or oral medications for less invasive types."
        elif prediction=="Dermatofibroma":
            msg="Dermatofibroma: These benign skin growths can be caused by an injury or insect bite, leading to an overgrowth of fibrous tissue. The exact cause isn't always clear."
            remedy="Often, no treatment is necessary unless the lesion is bothersome. Options include surgical removal or cryotherapy if it's painful or growing."
        elif prediction=="Melanoma":
            msg="Melanoma: The most serious type of skin cancer, melanoma, is largely caused by intense, intermittent UV exposure that leads to sunburns, especially in people with fair skin. Genetic factors and family history also play a role."
            remedy="Treatment is dependent on the stage of the cancer and can include surgical removal, immunotherapy, targeted therapy, chemotherapy, and radiation therapy. Early detection and treatment are crucial."
        elif prediction=="Nevus":
            msg="Nevus (Moles): Moles are usually benign and are caused by a high concentration of melanocytes, the cells that produce pigment in the skin. They can be influenced by genetic factors and sun exposure."
            remedy="If a mole is normal and not bothersome, no treatment is needed. If it's suspicious, changing, or cosmetically undesirable, surgical removal is the standard treatment."
        elif prediction=="Pigmented Benign Keratosis":
            msg="Pigmented Benign Keratosis: These are usually benign growths that are often part of the aging process. Sun exposure can play a role in their development."
            remedy="These are usually harmless and don't need treatment unless for cosmetic reasons. Options include cryotherapy, laser therapy, or surgical removal."
        elif prediction=="Seborrheic Keratosis":
            msg="Seborrheic Keratosis: These growths are common in older adults and may be related to aging, genetic factors, and possibly sun exposure. They're typically benign."
            remedy="Treatment is typically not necessary unless the lesions are irritating or for cosmetic reasons. Removal options include cryotherapy, curettage (scraping off the lesion), or laser therapy."
        elif prediction=="Squamous Cell Carcinoma":
            msg="Squamous Cell Carcinoma (SCC): Like BCC, SCC is mainly caused by cumulative exposure to UV radiation, leading to damage in the DNA of skin cells. People with fair skin, a history of sunburns, or immunosuppression are at increased risk."
            remedy="Treatment often involves surgical removal, Mohs surgery, cryotherapy, radiation therapy, or topical chemotherapy, depending on the lesion's size, depth, and location."
        else:
            msg="Vascular Lesion: This can refer to a range of conditions like hemangiomas or spider veins. Causes can vary widely, from genetic factors to hormonal changes, sun damage, or skin injuries."
            remedy="reatment depends on the type of lesion. Options may include laser therapy, sclerotherapy (injection that causes the vessel to collapse), or surgical removal in some cases."


        now = datetime.datetime.now()
        date = now.strftime('%Y-%m-%d')
        timeStamp = now.strftime('%H:%M:%S')
        sql="insert into disease_info(pname,email,age,gender,smoking,days,infection,bmi,image,disease,severity,causes,remedies,date,time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val=(session['username'],session['useremail'],age,gender,smoking,days,infection,bmi,mypath,prediction,msg1,msg,remedy,date,timeStamp)
        cur.execute(sql,val)
        db.commit()
        sql="select * from doctor"
        cur.execute(sql)
        data=cur.fetchall()
        db.commit()
        
        return render_template("result.html",image_name=fn, text=prediction,msg=msg , msg1=msg1,data=data)
    return render_template('upload.html')

@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("static/disease", filename)

@app.route('/expertdash')
def expertdash():
    
    sql="select * from users where user_Email='"+session['useremail']+"' "
    cur.execute(sql)
    data=cur.fetchall()
    return render_template('expertdash.html', data=data)

@app.route('/doctor_info',methods=['GET','POST'])
def doctor_info():
    
    sql="select * from appointment where pemail='"+session['useremail']+"'"
    cur.execute(sql)
    data=cur.fetchall()
    db.commit()
    
    return render_template('doctor_info.html', data=data)

@app.route('/expertchat/<email>',  methods=['POST', 'GET'])
def expertchat(email=""):
    useremail = session['useremail']   
    if request.method=="POST":
        email=request.form['email']
        messages = request.form['messages']
        now = datetime.datetime.now()
        date = now.strftime('%Y-%m-%d')
        timeStamp = now.strftime('%H:%M:%S')
        
        receiver=""
        sql = "INSERT INTO chatting (sender_email,receiver_email,chat_date,chat_time,msg,patient_email,patient_name,doctor_email) VALUES (%s,%s,%s,%s, %s, %s,%s,%s)"
        val = (useremail,email,date,timeStamp,messages,useremail,session['username'],email)
        data = cur.execute(sql, val)
        print(data)
        db.commit()
        
       
    # Fetch messages from the database
    
    sql_select = "SELECT * FROM chatting where patient_email='"+session['useremail']+"' ORDER BY chat_date, chat_time"
    cur.execute(sql_select)
    alldata = cur.fetchall()
    print(alldata)
    return render_template('expertchat.html',expert_email=email,farmer_email=useremail, alldata=alldata)

@app.route('/patient_request',methods=['GET','POST'])
def patient_request():
    
    print(session['useremail'])
    sql="select DISTINCT patient_email, patient_name from chatting where doctor_email='"+session['useremail']+"' "
    cur.execute(sql)
    data=cur.fetchall()
    db.commit()
    
    return render_template('patient_request.html', data=data)
    

@app.route('/patientchat/<email>/<name>',  methods=['POST', 'GET'])
def patientchat(email="",name=""):
    useremail = session['useremail']
    print(useremail) 
    print(email)  
    print(name)  
    if request.method=="POST":
        email=request.form['email']
        print(email)  
        name=request.form['username']
        print(name)  
        messages = request.form['messages']
        now = datetime.datetime.now()
        date = now.strftime('%Y-%m-%d')
        timeStamp = now.strftime('%H:%M:%S')
        
        sql = "INSERT INTO chatting (sender_email,receiver_email,chat_date,chat_time,msg,patient_email,patient_name,doctor_email) VALUES (%s,%s,%s,%s, %s, %s,%s,%s)"
        val = (useremail,email,date,timeStamp,messages,email,name,useremail)
        data = cur.execute(sql, val)
        print(data)
        db.commit()
        
    # Fetch messages from the database
    
    sql_select = "SELECT * FROM chatting where doctor_email='"+session['useremail']+"' and patient_email='"+email+"' ORDER BY chat_date, chat_time"
    cur.execute(sql_select)
    alldata = cur.fetchall()
    print(alldata[0][2])
    return render_template('patientchat.html',doctor_email=useremail,patient_email=email,patient_name=name, alldata=alldata)

@app.route('/patient')
def patient():
    
    sql="select * from users"
    cur.execute(sql)
    data=cur.fetchall()
    return render_template('patient.html',data=data)

@app.route('/doctor',methods=["POST","GET"])
def doctor():
    if request.method=='POST':
        username=request.form['userName']
        useremail = request.form['userEmail']       
        password = request.form['userPassword']
        mobile = request.form['userPhone']
        address = request.form['addr']
        exp = request.form['exp']
        age = request.form['age']
        gender = request.form['gender']
        hname = request.form['hname']
        
        sql="select * from doctor where Email='%s' "%(useremail)
        cur.execute(sql)
        data=cur.fetchall()
        db.commit()
        if data==[]:
            sql = "insert into doctor(Name,Email,Password,age,gender,hospital_name,address,exp_type,mobile) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val=(username,useremail,password,age,gender,hname,address,exp,mobile)
            cur.execute(sql,val)
            db.commit()
            flash("User registered Successfully","success")
            return render_template("doctor.html")
        else:
            flash("Details already Exists","warning")
            return render_template("doctor.html")
        
    return render_template('doctor.html')


@app.route('/doctorin', methods=['POST','GET'])
def sigdoctorinnin():
    if request.method=='POST':
        useremail = request.form['userEmail'] 
        password = request.form['userPassword']

        
        sql="select * from doctor where Email='"+useremail+"' and Password='"+password+"'"
        cur.execute(sql)
        data=cur.fetchall()
        db.commit()
        if data==[]:
            flash("Invalid data entered","danger")
            return render_template('doctorin.html')
        else:
            session['useremail']=useremail
            session['username']=data[0][1]
            flash("welcome ","success")
            return redirect(url_for('patient_request'))
          
    return render_template('doctorin.html')

@app.route('/appointment/<name>/<email>/<hname>/<addr>')
def appointment(name="",email="",hname="",addr=""):
    now = datetime.datetime.now()
    date = now.strftime('%Y-%m-%d')
    timeStamp = now.strftime('%H:%M:%S')
    
    sql="SELECT * FROM disease_info where email='"+session['useremail']+"' ORDER BY id DESC LIMIT 1";
    cur.execute(sql)
    data=cur.fetchall()
    db.commit()
    sq="insert into appointment(pname,pemail,age,gender,bmi,infection,smoking,days,image,disease,severity,date,time,hname,address,dname,demail) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val=(data[0][1],data[0][2],data[0][3],data[0][4],data[0][8],data[0][7],data[0][5],data[0][6],data[0][9],data[0][10],data[0][11],date, timeStamp,hname,addr,name,email)
    cur.execute(sq,val)
    db.commit()
    
    flash("Appointment Booked successfully","success")
    return render_template('upload.html')

@app.route('/view_appointments')
def view_appointments():
    
    sql="select * from appointment where demail='"+session['useremail']+"'"
    cur.execute(sql)
    data=cur.fetchall()
    return render_template('view_appointments.html',data=data)

@app.route('/appointment_status', methods=['POST','GET'])
def appointment_status(id=0):
    if request.method=='POST':
        id=request.form['id']
        date=request.form['date']
        
        sql="update appointment set status='Accepted', accepted_date='"+date+"' where id='"+id+"'"
        cur.execute(sql)
        db.commit()
        flash("appointment accepted","success")
        return redirect(url_for('view_appointments'))
    return redirect(url_for('view_appointments'))

@app.route('/feedback', methods=['POST','GET'])
def feedback():
    if request.method=='POST':
        id=request.form['id']
        msg=request.form['msg']
        
        sql="update appointment set status='Accepted', feedback='"+msg+"' where id='"+id+"'"
        cur.execute(sql)
        db.commit()
        flash("feedback submitted","success")
        return redirect(url_for('doctor_info'))
     
    return redirect(url_for('doctor_info'))



# Dummy translation function for demonstration
def translate(text, target_language):
    # Implement actual translation logic or integration with a translation service here
    return "Translated Text"

@app.route('/translate/<causes>/<remedy>' , methods=['GET'])
def translate_text(causes="",remedy=""):
    data = request.json
    translated_data = translate(data['text'], data['target_language'])
    return jsonify(translated_data)

@app.route('/history')
def history():

    sql="select * from disease_info where email='"+session['useremail']+"'"
    cur.execute(sql)
    data = cur.fetchall()
    print(data)
    print(type(data))
    return render_template('history.html', data=data)

# @app.route('/history')
# def history():

#     sql="select * from disease_info where email='"+session['useremail']+"'"
#     # cur.execute(sql, (session['useremail'],))
#     cur.execute(sql)
#     data = cur.fetchall()
#     print(data)
#     print(type(data))

#     # Check for language preference in session
#     if 'language' in session and session['language'] == 'telugu':
#         translator = Translator()
#         data = [(translator.translate(text, src='en', dest='te').text if isinstance(text, str) else text) for row in data for text in row]
#         print(data)
#     return render_template('history.html', data=data)

@app.route('/set_language', methods=['POST'])
def set_language():
    session['language'] = request.form['language']
    return redirect(url_for('history'))

@app.route('/doct_info')
def doct_info():

    sql="select * from doctor"
    cur.execute(sql)
    data = cur.fetchall()
    print(data)
    print(type(data))
    return render_template('doct_info.html', data=data)
if __name__=='__main__':
    app.run(debug=True)