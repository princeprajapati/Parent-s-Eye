from project import db
from project.com.vo.LoginVO import LoginVO
from project.com.vo.VideoVO import VideoVO


class VideoDAO:
    def insertVideo(self, videoVO):
        db.session.add(videoVO)
        db.session.commit()

    def viewVideo(self, videoVO):
        videoList = VideoVO.query.filter_by(video_LoginId=videoVO.video_LoginId).all()

        return videoList

    def deleteVideo(self, videoVO):
        videoList = VideoVO.query.get(videoVO.videoId)

        db.session.delete(videoList)

        db.session.commit()

        return videoList

    def adminViewVideo(self):
        videoList = db.session.query(VideoVO, LoginVO) \
            .join(LoginVO, VideoVO.video_LoginId == LoginVO.loginId).all()

        return videoList
