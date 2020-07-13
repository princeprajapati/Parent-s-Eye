from project import db
from project.com.vo.LoginVO import LoginVO
from project.com.vo.PackageVO import PackageVO


class PurchaseVO(db.Model):
    __tablename__ = 'purchasemaster'
    purchaseId = db.Column('purchaseId', db.Integer, primary_key=True, autoincrement=True)
    purchase_PackageId = db.Column('purchase_PackageId', db.Integer, db.ForeignKey(PackageVO.packageId))
    purchase_LoginId = db.Column('purchase_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId))
    purchaseDate = db.Column('purchaseDate', db.Date, nullable=False)
    purchaseTime = db.Column('purchaseTime', db.Time, nullable=False)

    def as_dict(self):
        return {
            'purchaseId': self.purchaseId,
            'purchase_PackageId': self.purchase_PackageId,
            'purchase_LoginId': self.purchase_LoginId,
            'purchaseDate': self.purchaseDate,
            'purchaseTime': self.purchaseTime
        }


db.create_all()
