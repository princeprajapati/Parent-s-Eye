from datetime import datetime, date

from flask import request, render_template, redirect, url_for, session

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.PackageDAO import PackageDAO
from project.com.dao.PurchaseDAO import PurchaseDAO
from project.com.vo.PurchaseVO import PurchaseVO


@app.route('/user/viewPackage', methods=['GET'])
def userViewPackage():
    try:
        if adminLoginSession() == 'user':
            packageDAO = PackageDAO()
            packageVOList = packageDAO.viewPackage()
            return render_template('user/viewPackage.html', packageVOList=packageVOList)
        else:
            return redirect(url_for('adminLogoutSession'))
    except Exception as ex:
        print(ex)


@app.route('/admin/viewPurchase', methods=['GET'])
def adminViewPurchase():
    try:
        if adminLoginSession() == 'admin':
            purchaseDAO = PurchaseDAO()
            purchaseVO = PurchaseVO()

            purchaseVOList = purchaseDAO.adminViewPurchase(purchaseVO)

            return render_template('admin/viewPurchase.html', purchaseVOList=purchaseVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/insertPurchase', methods=['GET'])
def userInsertPurchase():
    try:
        if adminLoginSession() == 'user':
            purchase_LoginId = session.get('session_loginId')
            purchase_PackageId = request.args.get('packageId')

            purchaseDate = date.today()
            print(purchaseDate)

            purchaseTime = datetime.now().strftime("%H:%M:%S")
            print(purchaseTime)

            purchaseVO = PurchaseVO()
            purchaseDAO = PurchaseDAO()

            purchaseVO.purchaseDate = purchaseDate
            purchaseVO.purchaseTime = purchaseTime
            purchaseVO.purchase_LoginId = purchase_LoginId
            purchaseVO.purchase_PackageId = purchase_PackageId

            purchaseDAO.insertPurchase(purchaseVO)

            return redirect(url_for('userViewPurchase'))
        else:
            return redirect(url_for('adminLogoutSession'))
    except Exception as ex:
        print(ex)


@app.route('/user/viewPurchase', methods=['GET'])
def userViewPurchase():
    try:
        if adminLoginSession() == 'user':
            purchaseDAO = PurchaseDAO()
            purchaseVO = PurchaseVO()

            purchase_LoginId = session.get('session_loginId')

            purchaseVO.purchase_LoginId = purchase_LoginId

            purchaseVOList = purchaseDAO.userViewPurchase(purchaseVO)

            return render_template('user/viewPurchase.html', purchaseVOList=purchaseVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/deletePurchase', methods=['GET'])
def userDeletePurchase():
    try:
        if adminLoginSession() == 'user':
            purchaseDAO = PurchaseDAO()
            purchaseVO = PurchaseVO()

            purchaseId = request.args.get('purchaseId')
            purchaseVO.purchaseId = purchaseId

            purchaseDAO.deletePurchase(purchaseVO)

            return redirect(url_for('userViewPurchase'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
