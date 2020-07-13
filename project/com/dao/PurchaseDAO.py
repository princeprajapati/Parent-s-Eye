from project import db
from project.com.vo.LoginVO import LoginVO
from project.com.vo.PackageVO import PackageVO
from project.com.vo.PurchaseVO import PurchaseVO


class PurchaseDAO:
    def insertPurchase(self, purchaseVO):
        db.session.add(purchaseVO)
        db.session.commit()

    def userViewPurchase(self, purchaseVO):
        purchaseList = db.session.query(PurchaseVO, PackageVO) \
            .join(PackageVO, PurchaseVO.purchase_PackageId == PackageVO.packageId) \
            .filter(PurchaseVO.purchase_LoginId == purchaseVO.purchase_LoginId).all()
        return purchaseList

    def adminViewPurchase(self, purchaseVO):
        purchaseList = db.session.query(PurchaseVO, PackageVO, LoginVO) \
            .join(PackageVO, PurchaseVO.purchase_PackageId == PackageVO.packageId) \
            .join(LoginVO, purchaseVO.purchase_LoginId == LoginVO.loginId).all()
        return purchaseList

    def deletePurchase(self, purchaseVO):
        purchaseList = PurchaseVO.query.get(purchaseVO.purchaseId)
        db.session.delete(purchaseList)
        db.session.commit()
