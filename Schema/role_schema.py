from pydantic import BaseModel

from typing import Literal
from enum import Enum

class Role_Schema(str,Enum):
    User="user"
    Admin="admin"
    SuperAdmin="superAdmin"


Permission_ROLE = {
Role_Schema.User: {"view"},
Role_Schema.Admin: {"view", "edit","write","delete","search"},
Role_Schema.SuperAdmin: {"view", "edit","write","delete"}  
}

Action=Literal["view","edit","write","delete","role_assign","me"]