from project import db
from project.com.vo.LoginVO import LoginVO


class VideoVO(db.Model):
    __tablename__ = 'videomaster'
    videoId = db.Column('videoId', db.Integer, primary_key=True, autoincrement=True)
    videoOutputFileName = db.Column('videoOutputFileName', db.String(500))
    videoOutputFilePath = db.Column('videoOutputFilePath', db.String(500))
    videoUploadDate = db.Column('videoUploadDate', db.String(50))
    videoUploadTime = db.Column('videoUploadTime', db.String(100))
    video_LoginId = db.Column('video_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId))

    def as_dict(self):
        return {

            'videoId': self.videoId,
            'videoOutputFileName': self.videoOutputFileName,
            'videoOutputFilePath': self.videoOutputFilePath,
            'videoUploadDate': self.videoUploadDate,
            'videoUploadTime': self.videoUploadTime,
            'video_LoginId': self.video_LoginId
        }


db.create_all()
