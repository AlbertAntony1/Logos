from flask import Flask, render_template, request, jsonify, redirect, session
import sqlite3, requests, random
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "https://logos-messaging-platform.onrender.com/callback"
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
mail = Mail(app)

session['userId']= ''
session['userName'] = ''
session['userProfilePicture'] = ''


# Database Handling
def createTable():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages(
              userId TEXT,
              userName TEXT,
              userProfilePicture TEXT,
              messageId INTEGER PRIMARY KEY,
              message TEXT,
              date TEXT)''')
    conn.commit()
    conn.close()
def insertData(userId, userName, userProfilePicture, messageId, message, date):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''INSERT INTO messages (userId, userName, userProfilePicture , messageId, message, date) VALUES (?, ?, ?, ?, ?, ?)''', (userId, userName, userProfilePicture,  messageId, message, date))
    conn.commit()
    conn.close()
def getData():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM messages ORDER BY messageId ASC''')
    row = c.fetchall()
    conn.close()
    return row


# Database and Routes Handling 
@app.route('/messageSend', methods=[ 'POST'])
def messageSend():
    messageDetails = request.json
    insertData(session['userId'], session['userName'], session['userProfilePicture'], messageDetails['messageId'], messageDetails['message'], messageDetails['date'])
    return jsonify({'result' : 'Message Successfully Sended'})
@app.route('/messageReceive', methods=['POST'])
def messageReceive():
    dataList = []
    for data in getData():
        dataList.insert(0, {
            'userId': data[0], 
            'userName': data[1], 
            'userProfilePicture': data[2],
            'messageId': data[3], 
            'message': data[4], 
            'date': data[5]
        })
    return dataList

# Login
@app.route('/login/google')
def googleLogin ():
    google_auth_url = "https://accounts.google.com/o/oauth2/auth"
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile"
    }
    request_url = requests.Request('GET', google_auth_url, params=params).prepare().url
    return {'data': request_url}
@app.route('/callback')
def callback():
    code = request.args.get("code")
    token_url = "https://oauth2.googleapis.com/token"
    data={
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        "grant_type": "authorization_code"
    }

    token_response = requests.post(token_url, data=data).json()
    access_token = token_response.get('access_token')
    users_data = requests.get("https://www.googleapis.com/oauth2/v1/userinfo", params={'access_token': access_token}).json()
    session['userId'] = users_data['email']
    session['userName'] = users_data['name']
    session['userProfilePicture'] = users_data['picture']
    return redirect('/chat')
@app.route('/login/otp', methods=['POST'])
def emailVerification():
    otp = str(random.randint(100000, 999999))
    session['otp'] = otp
    email = request.json.get('data')
    session['email'] = email
    msg = Message(
        subject="Your OTP Code",
        sender=app.config['MAIL_USERNAME'],
        recipients=[email]
    )
    
    msg.body = f"Your OTP is: {otp}"
    mail.send(msg)
    return {'data': 'OTP Successfully Send'}
@app.route('/login/otp/validate', methods=['POST'])
def otpVerification():
    if (session['otp'] == str(request.json.get('otp'))):
        session['userId'] = session['email']
        session['userName'] = request.json.get('name')
        session['userProfilePicture'] = 'https://www.shutterstock.com/search/funny-profile-picture?image_type=vector'
        return {'data' : True}
    else:
        return {'data': False}
@app.route('/userProfilePictureChange', methods=['POST'])
def userProfilePictureChange():
    file = request.files['file']
    session['userProfilePicture'] = f"./static/Resources/Images/Uploads/{str(random.randint(100000, 999999))}{file.filename}"
    file.save(session['userProfilePicture'])
    return 'success'

@app.route('/userIdChange', methods=['POST'])
def userIdChange():
    session['userId'] = request.json.get('data')
    return 'success'
@app.route('/userNameChange', methods=['POST'])
def userNameChange():
    session['userName'] = request.json.get('data')
    return 'success'

# Routes
@app.route('/')
@app.route('/home')
def launchPage():
    return render_template('index.html')

@app.route('/chat')
def homePage():
    if session['userId'] == '':
        return redirect('/login')
    else:
        createTable()
        return render_template('chat.html')
@app.route('/login')
def loginPage():
    return render_template('login.html')
@app.route('/profile')
def ProfilePage():
    if session['userId'] == '':
        return redirect('/login')
    else:
        return render_template('profile.html', username=session['userName'], userId=session['userId'], picture=session['userProfilePicture'])
@app.route('/about')
def aboutPage():
    return render_template('about.html')
@app.route('/contact')
def contactPage():
    return render_template('contact.html')
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# App Run
if __name__ == "__main__":
    app.run(debug=True)