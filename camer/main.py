import os
import numpy as np
import time
import cv2
from flask import Flask, flash, redirect, render_template, request, session, abort, Response,Request
from flask_sqlalchemy import SQLAlchemy

cam0 = cv2.VideoCapture(0)
cam0.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cam0.set(cv2.CAP_PROP_FRAME_WIDTH, 640)

# #camera 2
cam1 = cv2.VideoCapture(1)
cam1.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cam1.set(cv2.CAP_PROP_FRAME_WIDTH, 640)

#
#camea 2
cam2 = cv2.VideoCapture(2)
cam2.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cam2.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#
# #camera 3
# cam3 = cv2.VideoCapture(3,cv2.CAP_DSHOW)
# cam3.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
# cam3.set(cv2.CAP_PROP_FRAME_WIDTH, 640)

# if cam0.isOpened:
# # if v1.isOpened and v0.isOpened:
#
#     while(True):
#       ret,frame1 = cam0.read()
#       # ret,frame2 = cam1.read()
#       # ret,frame3 = cam2.read()
#       # ret,frame4 = cam3.read()
#       cv2.imshow("Video One",frame1)
#       # cv2.imshow("Video Two",frame2)
#       # cv2.imshow("Video Three",frame3)
#       # cv2.imshow("Video Four",frame4)
#       if cv2.waitKey(1) &0XFF == ord("x"):
#        break
# else:
#     print("Could not open camera")

app = Flask(__name__)


db_path = os.path.join(os.path.dirname(__file__), 'apiDB.db')
db_uri = 'sqlite:///{}'.format(db_path)

app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

db = SQLAlchemy(app)

def checkUser(email,pword):
    pass


@app.route('/')
def index():
    if not session.get('logged_in'):
        return render_template('login.html', loggedIn=False)
    else:
        return render_template('cam1.html', loggedIn=True)


'''
Generates frames from cameras opened
'''

def gen1():

    while (cam0.isOpened()):
        # Capture frame-by-frame
        ret, img = cam0.read()
        if ret == True:
            img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
            frame = cv2.imencode('.jpg', img)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(0.1)
        else:
            print("no image")
            break

def gen2():
    # Read until video is completed
    while (cam1.isOpened()):
        # Capture frame-by-frame
        ret, img = cam1.read()
        if ret == True:
            img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
            frame = cv2.imencode('.jpg', img)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(0.1)
        else:
            break

def gen3():

    # Read until video is completed
    while (cam2.isOpened()):
        # Capture frame-by-frame
        ret, img = cam2.read()
        if ret == True:
            img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
            frame = cv2.imencode('.jpg', img)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(0.1)
        else:
            break

def genBlank():

    # Read until video is completed
    while (True):

        try:
            # Capture frame-by-frame
            ret = True
            img = cv2.imread("static/images/videocam.png")
            #img = cv2.resize(img, (0, 0), interpolation = cv2.INTER_AREA)
            frame = cv2.imencode('.png', img)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(0.1)
        except:
            break




'''
routes to get frames from cameras and provide to html images for streaming
'''
@app.route('/video_feed_1')
def video_feed_1():
    """Video streaming route. Put this in the src attribute of an img tag."""
    try:
        if cam0.isOpened() == False:
            print("Camera 1 Closed")
            return Response(genBlank(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
        else:
            return Response(gen1(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as e:
        print(str(e))


@app.route('/video_feed_2')
def video_feed_2():
    """Video streaming route. Put this in the src attribute of an img tag."""
    try:
        if cam1.isOpened() == False:
            print("Camera  2 Closed")
            return Response(genBlank(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
        else:
            return Response(gen2(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as e:
        print(str(e))

@app.route('/video_feed_3')
def video_feed_3():


    """Video streaming route. Put this in the src attribute of an img tag."""

    try:
        if cam2.isOpened() == False:
            print("Camera 3  Closed")
            return Response(genBlank(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
        else:
            return Response(gen3(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as e:
        print(str(e))


@app.route('/login',methods=['POST'])
def login():
    username = request.form.get('login')
    password = request.form.get('password')

    print("username: "+username + " password: "+password)
    if username == 'admin' and password == 'password':
        session['logged_in'] = True
    else:
        error = 'Invalid username or password. Please try again!'
        return render_template('login.html', error=error)

    return index()

@app.route('/logout')
def logout():
    session.pop('user', None)
    session['logged_in'] = False
    return redirect('/')

@app.route('/about')
def about():
    if not session.get('logged_in'):
        return render_template('login.html', loggedIn=False)
    else:
        return render_template('about.html')

if __name__ == "__main__":



    app.run(host='0.0.0.0',debug=True)