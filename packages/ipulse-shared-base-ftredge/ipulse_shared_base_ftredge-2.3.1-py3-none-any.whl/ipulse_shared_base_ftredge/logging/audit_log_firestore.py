from pydantic import BaseModel
from datetime import datetime

class AuditLogFirestore(BaseModel):
    user_uid: str
    action: str
    collection_name: str
    document_name: str
    field_name: str
    old_value: str
    new_value: str
    timestamp: datetime