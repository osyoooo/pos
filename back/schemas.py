from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ProductBase(BaseModel):
    code: str
    name: str
    price: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    prd_id: int
    class Config:
        from_attributes = True

class TransactionBase(BaseModel):
    datetime: datetime
    emp_cd: Optional[str] = None
    store_cd: Optional[str] = None
    pos_no: Optional[str] = None
    total_amt: int
    ttl_amt_ex_tax: int

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    trd_id: int
    class Config:
        from_attributes = True

class TransactionDetailBase(BaseModel):
    prd_id: int
    prd_code: Optional[str] = None
    prd_name: Optional[str] = None
    prd_price: int
    tax_cd: str

class TransactionDetailCreate(TransactionDetailBase):
    pass

class TransactionDetail(TransactionDetailBase):
    dtl_id: int
    trd_id: int
    class Config:
        from_attributes = True

class TaxMasterBase(BaseModel):
    code: str
    name: str
    percent: float

class TaxMasterCreate(TaxMasterBase):
    pass

class TaxMaster(TaxMasterBase):
    id: int
    class Config:
        from_attributes = True
