"""Usage resource for handling any usage requests"""
from flask import jsonify
from webargs import fields
from webargs.flaskparser import use_kwargs
from flask_restful import Resource
from sqlalchemy import func
from datetime import datetime
from src.models.base import db

from src.models.subscriptions import Subscription
from src.models.usages import DataUsage
from src.models.service_codes import Plan
from src.models.cycles import BillingCycle

from src.models.utils import get_object_or_404
from src.schemas.subscriptions import SubscriptionSchema
from src.helper.usage import check_sub_limit

from src.config.constants import ACTIVE_SUBSCRIPTION_STATUS

class UsageAPI(Resource):
    """Resource/routes for Usage endpoints"""

    def get(self, sid):
        """External facing usage endpoint GET

        Gets data usage of subscription for current billing cycle

        Args:
            sid (int): id of subscription object

        Returns:
            json: 
                data_usage: data usage of a given subscription for current billing cycle - float
                notice: note for this subscription, especially for overlimit subscription

        """

        # Get Subscription 
        subscription = get_object_or_404(Subscription, sid)

        # Check Subscription status
        if subscription.status in ACTIVE_SUBSCRIPTION_STATUS:

            # Get current billing cycle
            cycle = BillingCycle.get_current_cycle()
            
            # if billing cycle is existing
            if cycle:
                # Get Data Usages Record in current billing cycle
                data_usages = db.session.query(func.sum(DataUsage.mb_used)).with_parent(subscription).\
                    filter(DataUsage.from_date <= cycle.end_date).\
                    filter(DataUsage.from_date >= cycle.start_date).\
                    scalar()
                
                # Check if subscription is over the alloted data usage
                # show the data usages in gigabytes

                result = {
                    "data_usage": "{} GB".format(float('%.2f' % (data_usages/1024))),
                }

                if not check_sub_limit(data_usages, subscription.plan):
                    result["notice"] = "The subscription is over its allocated space"
            else:
                result = {
                    "data_usage": "0 GB",
                    "notice": "This subscription doesn't have any usage data for current billing cycle"
                }
        else:
            result = {
                "data_usage": "0 GB",
                "notice": "This subscription can't have usage data"
            }

        return jsonify(result)
