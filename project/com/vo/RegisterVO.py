from project import db
from project.com.vo.LoginVO import LoginVO


class RegisterVO(db.Model):
    __tablename__ = 'registermaster'
    registerId = db.Column('registerId', db.Integer, primary_key=True, autoincrement=True)
    registerFirstName = db.Column('registerFirstName', db.String(500), nullable=False)
    registerLastName = db.Column('registerLastName', db.String(500), nullable=False)
    registerAddress = db.Column('registerAddress', db.String(500), nullable=False)
    registerContact = db.Column('registerContact', db.String(100), nullable=False)
    register_LoginId = db.Column('register_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId))

    def as_dict(self):
        return {

            'registerId': self.registerId,
            'registerFirstName': self.registerFirstName,
            'registerLastName': self.registerLastName,
            'registerAddress': self.registerAddress,
            'registerContact': self.registerContact,
            'register_LoginId': self.register_LoginId
        }


db.create_all()
