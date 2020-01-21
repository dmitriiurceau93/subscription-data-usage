from datetime import datetime
from src.models.base import db
from src.models.subscriptions import Subscription
from src.models.cycles import BillingCycle
from src.models.usages import DataUsage
from sqlalchemy import func

from src.helper.service_code import apply_service_code
from src.helper.usage import check_sub_limit

def check_subscriptions():
    # Get Subscription 
    subscriptions = Subscription.get_subscriptions()
    
    # Get current billing cycle
    cycle = BillingCycle.get_current_cycle(date=datetime(2019,9,2))
    
    # if billing cycle is existing
    if cycle:
        for s in subscriptions:
            # Get Data Usages Record in current billing cycle
            data_usages = db.session.query(func.sum(DataUsage.mb_used)).with_parent(s).\
                filter(DataUsage.from_date <= cycle.end_date).\
                filter(DataUsage.from_date >= cycle.start_date).\
                scalar()
            
            # Check if subscription is over the alloted data usage

            if data_usages and \
                not check_sub_limit(data_usages, s.plan) \
                and not s.plan.is_unlimited:

                # Apply block service code
                apply_service_code(s)

    return
    