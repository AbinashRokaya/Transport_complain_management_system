from enum import Enum

class Category_Enum(str,Enum):
    Minor="Minor", 
    Moderate="Moderate", 
    Severe="Severe", 
    Emergency="Emergency"