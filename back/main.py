from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from schemas import (
    ProductCreate, Product as ProductSchema,
    TransactionCreate, Transaction as TransactionSchema,
    TransactionDetailCreate, TransactionDetail as TransactionDetailSchema,
    TaxMasterCreate, TaxMaster as TaxMasterSchema,
)
from database import SessionLocal, engine
from models import Product, Transaction, TransactionDetail, TaxMaster
from crud import (create_product, get_products, get_product, get_product_by_code, update_product, delete_product,
                create_tax, get_taxes)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # すべてのオリジンを許可する場合
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Product.metadata.create_all(bind=engine)
Transaction.metadata.create_all(bind=engine)
TransactionDetail.metadata.create_all(bind=engine)
TaxMaster.metadata.create_all(bind=engine)

@app.post("/products/", response_model=ProductSchema)
async def create_product_endpoint(product: ProductCreate, db: Session = Depends(get_db)):
    existing_product = db.query(Product).filter(Product.code == product.code).first()
    if existing_product:
        raise HTTPException(status_code=400, detail="Product with this code already exists")
    return create_product(db=db, product=product)

@app.get("/products/", response_model=list[ProductSchema])
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_products(db, skip=skip, limit=limit)

@app.get("/products/{prd_id}", response_model=ProductSchema)
def read_product(prd_id: int, db: Session = Depends(get_db)):
    product = get_product(db, prd_id=prd_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.get("/products/code/{code}", response_model=ProductSchema)
def read_product_by_code(code: str, db: Session = Depends(get_db)):
    try:
        product = get_product_by_code(db, code=code)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/products/{prd_id}", response_model=ProductSchema)
def update_product_endpoint(prd_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    updated_product = update_product(db, prd_id=prd_id, product=product)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

@app.delete("/products/{prd_id}", response_model=ProductSchema)
def delete_product_endpoint(prd_id: int, db: Session = Depends(get_db)):
    if not delete_product(db, prd_id=prd_id):
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}

@app.post("/taxes/", response_model=TaxMasterSchema)
def create_tax_endpoint(entry: TaxMasterCreate, db: Session = Depends(get_db)):
    return create_tax(db=db, entry=entry)

@app.get("/taxes/", response_model=list[TaxMasterSchema])
def read_taxes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_taxes(db, skip=skip, limit=limit)

# 購入ボタン時用に利用
@app.post("/checkout")
def checkout(items: list[TransactionDetailCreate], db: Session = Depends(get_db)):
    try:
        transaction = TransactionCreate(
            datetime=datetime.now(),
            emp_cd="9999999999",  # 例として固定値を使用
            store_cd="30",       # 例として固定値を使用
            pos_no="90",         # 例として固定値を使用
            total_amt=sum(item.prd_price * item.quantity for item in items),
            ttl_amt_ex_tax=sum(item.prd_price * item.quantity for item in items)
        )
        new_transaction = create_transaction(db=db, transaction=transaction)
        for item in items:
            transaction_detail = TransactionDetailCreate(
                trd_id=new_transaction.trd_id,
                prd_id=item.prd_id,
                prd_code=item.prd_code,
                prd_name=item.prd_name,
                prd_price=item.prd_price,
                tax_cd=item.tax_cd
            )
            create_transaction_detail(db=db, transaction_detail=transaction_detail)
        return {"message": "Purchase successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Purchase failed")
