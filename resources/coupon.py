from models.coupon import CouponModel
from flask_restful import Resource, reqparse


class Coupon(Resource):
    def get(self, id):
        coupon = CouponModel.FindById(id)
        if coupon:
            return {'coupon': coupon.json()}, 200
        return {'message': 'Coupon not found!'}, 404


class CouponList(Resource):
    def get(self):
        coupons = CouponModel.FindAll()
        if coupons:
            return {'coupons': [coupon.json() for coupon in coupons]}, 200
        return {'message': 'Coupon not found!'}, 404
