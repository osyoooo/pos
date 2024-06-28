from sqlalchemy.orm import Session
from models import Product, Transaction, TransactionDetail, TaxMaster
from schemas import ProductCreate, TransactionCreate, TransactionDetailCreate, TaxMasterCreate
from datetime import datetime
from sqlalchemy import func

# 商品を作成
def create_product(db: Session, product: ProductCreate):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# 商品一覧を取得
def get_products(db: Session, skip: int, limit: int):
    return db.query(Product).offset(skip).limit(limit).all()

# 商品IDで商品を検索
def get_product(db: Session, prd_id: int):
    return db.query(Product).filter(Product.prd_id == prd_id).first()

# 商品コードで商品を検索
def get_product_by_code(db: Session, code: str):
    return db.query(Product).filter(Product.code == code).first()

# 商品情報を更新
def update_product(db: Session, prd_id: int, product: ProductCreate):
    db_product = db.query(Product).filter(Product.prd_id == prd_id).first()
    if db_product:
        db_product.code = product.code
        db_product.name = product.name
        db_product.price = product.price
        db.commit()
        db.refresh(db_product)
    return db_product

# 商品を削除
def delete_product(db: Session, prd_id: int):
    db_product = db.query(Product).filter(Product.prd_id == prd_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product

# 税率情報を作成
def create_tax(db: Session, entry: TaxMasterCreate):
    db_entry = TaxMaster(**entry.dict())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

# 税率情報一覧を取得
def get_taxes(db: Session, skip: int, limit: int):
    return db.query(TaxMaster).offset(skip).limit(limit).all()

# 売上明細を生成
def generate_sales_report(db: Session, start_date: str, end_date: str):
    start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
    end_datetime = datetime.strptime(end_date, "%Y-%m-%d")
    total_sales = db.query(func.sum(Transaction.total_amt)).filter(
        Transaction.datetime >= start_datetime,
        Transaction.datetime <= end_datetime
    ).scalar() or 0  # 結果がNoneの場合は0を返す
    return {"total_sales": total_sales}
