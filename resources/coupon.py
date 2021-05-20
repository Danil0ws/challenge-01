from models.coupon import CouponModel
from flask_restful import Resource, reqparse

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

    def put(self, id):
        """Updates a coupon."""
        parser.add_argument('active',
                            type=bool,
                            required=True,
                            help='This field is required!')

        parser.add_argument('type',
                            type=str,
                            required=True,
                            help='This field is required!')

        parser.add_argument('code',
                            type=str,
                            required=True,
                            help='This field is required!')

        parser.add_argument('value',
                            type=int,
                            required=True,
                            help='This field is required!')

        data_payload = parser.parse_args()
        coupon = CouponModel.UpdateById(id, data_payload)
        if coupon:
            return {'message': 'Coupon successfully edited'}, 20
        return {'message': 'Coupon not edited!'}, 404

    def post(self):
        """Creates a new coupon."""
        parser.add_argument('active',
                            type=bool,
                            required=True,
                            help='This field is required!')

        parser.add_argument('type',
                            type=str,
                            required=True,
                            help='This field is required!')

        parser.add_argument('code',
                            type=str,
                            required=True,
                            help='This field is required!')

        parser.add_argument('value',
                            type=int,
                            required=True,
                            help='This field is required!')

        data_payload = parser.parse_args()
        coupon = CouponModel.InsertData(data_payload)
        if coupon:
            return {'message': 'Coupon successfully created'}, 201
        return {'message': 'Coupon not created!'}, 400
