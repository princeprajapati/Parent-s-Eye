from project import db
from project.com.vo.ComplainVO import ComplainVO
from project.com.vo.LoginVO import LoginVO


class ComplainDAO:
    def userInsertComplain(self, complainVO):
        db.session.add(complainVO)
        db.session.commit()

    def userViewComplain(self, complainVO):
        complainList = ComplainVO.query.filter_by(complainFrom_LoginId=complainVO.complainFrom_LoginId).all()
        return complainList

    def adminViewComplain(self, complainVO):
        complainList = db.session.query(ComplainVO, LoginVO).join(LoginVO,
                                                                  ComplainVO.complainFrom_LoginId == LoginVO.loginId).filter(
            ComplainVO.complainStatus == complainVO.complainStatus).all()
        return complainList

    def adminInsertComplainReply(self, complainVO):
        db.session.merge(complainVO)
        db.session.commit()

    def userViewComplainReply(self, complainVO):
        complainList = ComplainVO.query.filter_by(complainId=complainVO.complainId)
        return complainList

    def userDeleteComplain(self, complainVO):
        complainList = ComplainVO.query.get(complainVO.complainId)

        db.session.delete(complainList)

        db.session.commit()

        return complainList

    def viewComplain(self):
        complainList = ComplainVO.query.all()
        return complainList
