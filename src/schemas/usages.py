"""Usages schemas to assist with data usage serialization"""
from marshmallow import fields, Schema, validate

from src.schemas.subscriptions import SubscriptionSchema

class UsageSchema(Schema):
    """Schema class to handle serialization of data usage"""
    id = fields.Integer()
    mb_used = fields.Float()
    from_date = fields.DateTime()
    to_date = fields.DateTime()

    subscription_id = fields.String()
    subscription = fields.Nested(SubscriptionSchema, dump_only=True)
