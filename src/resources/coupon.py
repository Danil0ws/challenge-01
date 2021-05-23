from models.coupon import CouponModel
from flask_restful import Resource, request
from flask_expects_json import expects_json


class Coupon(Resource):
    """Operations related to Coupons."""

    def get(self, id=None):
        """Returns details of a(all) coupon(s)."""
        codeParams = request.args.get('code')
        if id:
            couponReturn = CouponModel.FindById(id)
            return couponReturn
        elif codeParams is not None:
            couponReturn = CouponModel.FindByCode(codeParams)
            return couponReturn
        else:
            couponReturn = CouponModel.FindAll()
            return couponReturn

    @expects_json({
        'type': 'object',
        'properties': {
            'active': {'type': 'integer'},
            'type': {'type': 'string'},
            'code': {'type': 'string'},
            'quantity': {'type': 'integer'},
            'value': {'type': 'number'}
        },
        'required': ['active', 'type', 'code', 'quantity', 'value']
    })
    def post(self):
        """Add a new coupon to the database."""
        data_payload = request.get_json()
        couponReturn = CouponModel.InsertData(data_payload)
        return couponReturn

    @expects_json({
        'type': 'object',
        'properties': {
            'active': {'type': 'integer'},
            'type': {'type': 'string'},
            'code': {'type': 'string'},
            'quantity': {'type': 'integer'},
            'value': {'type': 'number'}
        }
    })
    def put(self, id):
        """Update an existing coupon."""
        data_payload = request.get_json()
        couponReturn = CouponModel.UpdateById(id, data_payload)
        return couponReturn

    def delete(self, id):
        """Deletes a coupon."""
        couponReturn = CouponModel.DeleteById(id)
        return couponReturn
