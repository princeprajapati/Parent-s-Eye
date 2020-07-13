import os
from datetime import date, datetime

from flask import render_template, request, url_for, redirect
from werkzeug.utils import secure_filename

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession, session
from project.com.dao.ComplainDAO import ComplainDAO
from project.com.vo.ComplainVO import ComplainVO

UPLOAD_FOLDER1 = 'project/static/adminResources/complain/'
app.config['UPLOAD_FOLDER1'] = UPLOAD_FOLDER1

UPLOAD_FOLDER2 = 'project/static/adminResources/reply/'
app.config['UPLOAD_FOLDER2'] = UPLOAD_FOLDER2


@app.route('/user/loadComplain')
def userLoadComplain():
    try:
        if adminLoginSession() == 'user':
            return render_template("user/addComplain.html")
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/user/insertComplain', methods=['POST'])
def userInsertComplain():
    try:
        if adminLoginSession() == 'user':
            complainSubject = request.form['complainSubject']
            complainDescription = request.form['complainDescription']
            complainDate = date.today()
            complainTime = datetime.now().strftime("%H:%M:%S")
            complainStatus = 'Pending'
            complainFrom_LoginId = session['session_loginId']
            file = request.files['complainFile']

            complainFileName = secure_filename(file.filename)

            complainFilePath = os.path.join(app.config['UPLOAD_FOLDER1'])

            file.save(os.path.join(complainFilePath, complainFileName))

            complainVO = ComplainVO()
            complainDAO = ComplainDAO()

            complainVO.complainSubject = complainSubject
            complainVO.complainDescription = complainDescription
            complainVO.complainDate = complainDate
            complainVO.complainTime = complainTime
            complainVO.complainStatus = complainStatus
            complainVO.complainFrom_LoginId = complainFrom_LoginId
            complainVO.complainFileName = complainFileName
            complainVO.complainFilePath = complainFilePath.replace('project', '..')

            complainDAO.userInsertComplain(complainVO)

            return redirect(url_for('userViewComplain'))

        else:

            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/user/viewComplain', methods=['GET'])
def userViewComplain():
    try:
        if adminLoginSession() == 'user':
            complainDAO = ComplainDAO()
            complainVO = ComplainVO()
            complainFrom_LoginId = session['session_loginId']
            complainVO.complainFrom_LoginId = complainFrom_LoginId
            complainVOList = complainDAO.userViewComplain(complainVO)

            print("______________", complainVOList)

            return render_template("user/viewComplain.html", complainVOList=complainVOList)

        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/user/deleteComplain', methods=['GET'])
def userDeleteComplain():
    try:
        if adminLoginSession() == 'user':

            complainVO = ComplainVO()
            complainDAO = ComplainDAO()
            complainId = request.args.get('complainId')
            complainVO.complainId = complainId

            complainList = complainDAO.userDeleteComplain(complainVO)
            print(complainList)

            complainStatus = complainList.complainStatus
            complainFileName = complainList.complainFileName
            complainFilePath = complainList.complainFilePath.replace('..', 'project')
            complainPath = complainFilePath + complainFileName
            os.remove(complainPath)

            if complainStatus == "Replied":
                replyFileName = complainList.replyFileName
                replyFilePath = complainList.replyFilePath.replace('..', 'project')
                replyPath = replyFilePath + replyFileName
                os.remove(replyPath)

            return redirect(url_for('userViewComplain'))
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/user/viewComplainReply', methods=['GET'])
def userViewComplainReply():
    try:
        if adminLoginSession() == 'user':
            complainDAO = ComplainDAO()
            complainVO = ComplainVO()
            complainId = request.args.get('complainId')
            complainVO.complainId = complainId
            complainVOList = complainDAO.userViewComplainReply(complainVO)
            return render_template('user/viewComplainReply.html', complainVOList=complainVOList)

        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/viewComplain', methods=['GET'])
def adminViewComplain():
    try:
        if adminLoginSession() == 'admin':

            complainDAO = ComplainDAO()
            complainVO = ComplainVO()

            complainVO.complainStatus = "Pending"

            complainVOList = complainDAO.adminViewComplain(complainVO)
            print("______________", complainVOList)

            return render_template('admin/viewComplain.html', complainVOList=complainVOList)
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/loadComplainReply')
def adminLoadComplainReply():
    try:
        if adminLoginSession() == 'admin':
            complainId = request.args.get('complainId')
            return render_template('admin/addComplainReply.html', complainId=complainId)

        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/insertComplainReply', methods=['POST'])
def adminInsertComplainReply():
    try:
        if adminLoginSession() == 'admin':

            complainId = request.form['complainId']
            replySubject = request.form['replySubject']
            replyMessage = request.form['replyMessage']
            replyDate = date.today()
            replyTime = datetime.now().strftime("%H:%M:%S")
            complainStatus = 'Replied'
            complainTo_LoginId = session['session_loginId']

            file = request.files['replyFile']

            replyFileName = secure_filename(file.filename)

            replyFilePath = os.path.join(app.config['UPLOAD_FOLDER2'])

            file.save(os.path.join(replyFilePath, replyFileName))

            complainVO = ComplainVO()
            complainDAO = ComplainDAO()

            complainVO.complainId = complainId
            complainVO.complainTo_LoginId = complainTo_LoginId
            complainVO.replySubject = replySubject
            complainVO.replyMessage = replyMessage
            complainVO.replyDate = replyDate
            complainVO.replyTime = replyTime
            complainVO.complainStatus = complainStatus
            complainVO.replyFileName = replyFileName
            complainVO.replyFilePath = replyFilePath.replace('project', '..')

            complainDAO.adminInsertComplainReply(complainVO)

            return redirect(url_for('adminViewComplain'))

        else:
            return adminLogoutSession

    except Exception as ex:
        print(ex)
