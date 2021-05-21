from models.coupon import CouponModel
from flask_restful import Resource, reqparse, request
from flask_expects_json import expects_json

parser = reqparse.RequestParser()


class Coupon(Resource):
    """Operations related to coupons."""

    def get(self, id=None):
        """Returns details of a coupon."""
        if id:
            coupon = CouponModel.FindById(id)
            if coupon:
                return {'coupon': coupon.json()}, 200
            return {'message': 'Coupon not found!'}, 404
        else:
            coupons = CouponModel.FindAll()
            if coupons:
                return {'coupons': [coupon.json() for coupon in coupons]}, 200
            return {'message': 'Coupon not found!'}, 404

    def delete(self, id):
        """Deletes coupon."""
        coupon = CouponModel.DeleteById(id)
        if coupon:
            return {'message': 'Coupon successfully delete'}, 200
        return {'message': 'Coupon not found!'}, 400

    @expects_json({
        'type': 'object',
        'properties': {
            'active': {'type': 'string'},
            'type': {'type': 'string'},
            'code': {'type': 'integer'},
            'quantity': {'type': 'integer'},
            'value': {'type': 'integer'}
        }
    })
    def put(self, id):
        """Updates a coupon."""
        data_payload = request.get_json()
        couponReturn = CouponModel.UpdateById(id, data_payload)
        return couponReturn

    @expects_json({
        'type': 'object',
        'properties': {
            'active': {'type': 'string'},
            'type': {'type': 'string'},
            'code': {'type': 'integer'},
            'quantity': {'type': 'integer'},
            'value': {'type': 'integer'}
        },
        'required': ['active', 'type', 'code', 'quantity', 'value']
    })
    def post(self):
        """Creates a new coupon."""
        data_payload = request.get_json()
        couponReturn = CouponModel.InsertData(data_payload)
        return couponReturn
