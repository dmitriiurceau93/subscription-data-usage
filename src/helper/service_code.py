from src.models.utils import get_object_or_404
from src.models.service_codes import ServiceCode
from src.models.base import db

def apply_service_code(subscription):
    
    # Query Data Block Service Code Object
    block_code = get_object_or_404(ServiceCode, 1)

    block_code.subscriptions.append(subscription)
    db.session.commit()
    