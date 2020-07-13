import random
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import request, render_template, redirect, url_for

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.LoginDAO import LoginDAO
from project.com.dao.RegisterDAO import RegisterDAO
from project.com.vo.LoginVO import LoginVO
from project.com.vo.RegisterVO import RegisterVO


@app.route('/user/loadRegister', methods=['GET'])
def LoadRegister():
    try:
        return render_template('user/register.html')
    except Exception as ex:
        print(ex)


@app.route('/user/insertRegister', methods=['POST'])
def userInsertRegister():
    try:
        loginUsername = request.form['loginUsername']

        loginPassword = ''.join((random.choice(string.ascii_letters + string.digits)) for x in range(8))
        print("password=", loginPassword)

        loginVO = LoginVO()
        loginDAO = LoginDAO()

        loginVO.loginUsername = loginUsername
        loginVO.loginPassword = loginPassword
        loginVO.loginRole = "user"
        loginVO.loginStatus = "active"

        sender = "parentseye2907@gmail.com"

        receiver = loginUsername

        msg = MIMEMultipart()

        msg['From'] = sender

        msg['To'] = receiver

        msg['Subject'] = "LOGIN PASSWORD"

        msg.attach(MIMEText(loginPassword, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)

        server.starttls()

        server.login(sender, "parents123eye123")

        text = msg.as_string()

        server.sendmail(sender, receiver, text)

        loginDAO.insertLogin(loginVO)

        registerFirstName = request.form['registerFirstName']
        registerLastName = request.form['registerLastName']
        registerAddress = request.form['registerAddress']
        registerContact = request.form['registerContact']

        registerVO = RegisterVO()
        registerDAO = RegisterDAO()

        registerVO.registerFirstName = registerFirstName
        registerVO.registerLastName = registerLastName
        registerVO.registerAddress = registerAddress
        registerVO.registerContact = registerContact
        registerVO.register_LoginId = loginVO.loginId

        registerDAO.insertRegister(registerVO)

        server.quit()

        return render_template("admin/login.html")
    except Exception as ex:
        print(ex)


@app.route('/admin/viewUser', methods=['GET'])
def adminViewRegister():
    try:
        if adminLoginSession() == "admin":
            registerDAO = RegisterDAO()
            registerVOList = registerDAO.viewRegister()
            print("_________", registerVOList)
            return render_template("admin/viewUser.html", registerVOList=registerVOList)

        else:
            return redirect(url_for("adminLogoutSession"))

    except Exception as ex:
        print(ex)

@app.route('/user/editRegister', methods=['GET'])
def userEditRegister():
    try:
        if adminLoginSession() == 'user':
            loginId = request.args.get('loginId')

            registerVO = RegisterVO()
            registerDAO = RegisterDAO()

            registerVO.register_LoginId = loginId
            registerVOList = registerDAO.editProfile(registerVO)
            print("registerVOList >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ", registerVOList)


            return render_template('user/editProfile.html', registerVOList=registerVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)

@app.route('/user/updateProfile', methods=['POST'])
def userUpdateRegister():
    try:
        if adminLoginSession() == 'user':
            registerVO = RegisterVO()
            registerDAO = RegisterDAO()

            loginId = request.form['loginId']
            loginUsername = request.form['loginUsername']

            registerId = request.form['registerId']
            registerFirstName = request.form['registerFirstName']
            registerLastName = request.form['registerLastName']
            registerAddress = request.form['registerAddress']
            registerContact = request.form['registerContact']

            loginVO = LoginVO()
            loginDAO = LoginDAO()
            loginVO.loginId = loginId
            loginList = loginDAO.viewLogin(loginVO)

            if loginList[0].loginUsername == loginUsername:
                pass
            else:
                loginPassword = ''.join((random.choice(string.ascii_letters + string.digits)) for x in range(8))

                sender = "parentseye2907@gmail.com"

                receiver = loginUsername

                msg = MIMEMultipart()

                msg['From'] = sender

                msg['To'] = receiver

                msg['Subject'] = "ACCOUNT PASSWORD"

                msg.attach(MIMEText(loginPassword, 'plain'))

                server = smtplib.SMTP('smtp.gmail.com', 587)

                server.starttls()

                server.login(sender, "parents123eye123")

                text = msg.as_string()

                server.sendmail(sender, receiver, text)

                server.quit()

                loginVO.loginUsername = loginUsername
                loginVO.loginPassword = loginPassword

                loginDAO.updateLogin(loginVO)

            registerVO.registerId = registerId
            registerVO.registerFirstName = registerFirstName
            registerVO.registerLastName = registerLastName
            registerVO.registerAddress = registerAddress
            registerVO.registerContact = registerContact

            registerDAO.updateRegister(registerVO)
            return redirect(url_for('userLoadDashboard'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
