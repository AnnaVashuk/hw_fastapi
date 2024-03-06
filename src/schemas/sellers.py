from pydantic import BaseModel, Field, field_validator
from pydantic_core import PydanticCustomError

from .books import ReturnedBook

__all__ = ["IncomingSeller", "ReturnedSeller", "ReturnedAllSellers", "ReturnedSellerBooks"]



class BaseSeller(BaseModel):
    first_name: str
    last_name: str
    email: str



class IncomingSeller(BaseSeller):
    first_name: str
    last_name: str
    email: str
    password: str

  

class ReturnedSeller(BaseSeller):
    id: int = 1



class ReturnedAllSellers(BaseModel):
    sellers: list[ReturnedSeller]



class ReturnedSellerBooks(BaseSeller):
    books: list[ReturnedBook]

