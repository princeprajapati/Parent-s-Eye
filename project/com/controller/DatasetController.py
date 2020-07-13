import os
from datetime import date, datetime

from flask import request, redirect, render_template, url_for
from werkzeug.utils import secure_filename

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.DatasetDAO import DatasetDAO
from project.com.vo.DatasetVO import DatasetVO

UPLOAD_FOLDER = 'project/static/adminResources/dataset/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/admin/loadDataset', methods=['GET'])
def adminLoadDataset():
    try:
        if adminLoginSession() == 'admin':
            return render_template('admin/addDataset.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/insertDataset', methods=['POST'])
def adminInsertDataset():
    try:
        if adminLoginSession() == 'admin':
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
            datasetVO = DatasetVO()
            datasetDAO = DatasetDAO()

            file = request.files['file']

            datasetFileName = secure_filename(file.filename)

            datasetFilePath = os.path.join(app.config['UPLOAD_FOLDER'])

            datasetUploadDate = date.today()
            datasetUploadTime = datetime.now().strftime("%H:%M:%S")

            file.save(os.path.join(datasetFilePath, datasetFileName))

            datasetVO.datasetFileName = datasetFileName

            datasetVO.datasetFilePath = datasetFilePath.replace('project', '..')

            datasetVO.datasetUploadDate = datasetUploadDate

            datasetVO.datasetUploadTime = datasetUploadTime

            datasetDAO.insertDataset(datasetVO)

            return redirect(url_for('adminViewDataset'))

        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/viewDataset', methods=['GET'])
def adminViewDataset():
    try:
        if adminLoginSession() == 'admin':
            datasetDAO = DatasetDAO()
            datasetVOList = datasetDAO.viewDataset()
            print("______________", datasetVOList)

            return render_template('admin/viewDataset.html', datasetVOList=datasetVOList)
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/deleteDataset', methods=['GET'])
def adminDeleteDataset():
    try:
        if adminLoginSession() == 'admin':
            datasetVO = DatasetVO()

            datasetDAO = DatasetDAO()

            datasetFileId = request.args.get('datasetFileId')

            datasetVO.datasetFileId = datasetFileId

            datasetList = datasetDAO.deleteDataset(datasetVO)

            path = datasetList.datasetFilePath.replace("..", "project") + datasetList.datasetFileName

            os.remove(path)

            return redirect(url_for('adminViewDataset'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
