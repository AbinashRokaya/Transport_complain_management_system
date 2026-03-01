from enum import Enum

class Status_Enum(str,Enum):
    Pending="Pending",
    In_Progress="In Progress",
    Resolved="Resolved"