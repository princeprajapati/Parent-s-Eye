from project import db


class DatasetVO(db.Model):
    __tablename__ = 'datasetmaster'
    datasetFileId = db.Column('datasetFileId', db.Integer, primary_key=True, autoincrement=True)
    datasetFileName = db.Column('datasetFileName', db.String(500))
    datasetFilePath = db.Column('datasetFilePath', db.String(500))
    datasetUploadDate = db.Column('datasetUploadDate', db.String(50))
    datasetUploadTime = db.Column('datasetUploadTime', db.String(100))

    def as_dict(self):
        return {

            'datasetFileId': self.datasetFileId,
            'datasetFileName': self.datasetFileName,
            'datasetFilePath': self.datasetFilePath,
            'datasetUploadDate': self.datasetUploadDate,
            'datasetUploadTime': self.datasetUploadTime
        }


db.create_all()
