from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DECIMAL
from database import Base
import datetime

class Product(Base):
    __tablename__ = "商品マスタ"
    prd_id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(13), nullable=False, unique=True)
    name = Column(String(50), nullable=False)
    price = Column(Integer, nullable=False)

class Transaction(Base):
    __tablename__ = "取引"
    trd_id = Column(Integer, primary_key=True)
    datetime = Column(DateTime, default=datetime.datetime.utcnow)
    emp_cd = Column(String(10), nullable=True)
    store_cd = Column(String(5), nullable=True)
    pos_no = Column(String(3), nullable=True)
    total_amt = Column(Integer)
    ttl_amt_ex_tax = Column(Integer)

class TransactionDetail(Base):
    __tablename__ = "取引明細"
    dtl_id = Column(Integer, primary_key=True)
    trd_id = Column(Integer, ForeignKey("取引.trd_id"))
    prd_id = Column(Integer, ForeignKey("商品マスタ.prd_id"))
    prd_code = Column(String(13), nullable=True)
    prd_name = Column(String(50), nullable=True)
    prd_price = Column(Integer)
    tax_cd = Column(String(2))

class TaxMaster(Base):
    __tablename__ = "税マスタ"
    id = Column(Integer, primary_key=True)
    code = Column(String(2), unique=True)
    name = Column(String(20), nullable=False)
    percent = Column(DECIMAL(5, 2), nullable=False)
