from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import mysql.connector
from dotenv import load_dotenv
import os

# 環境変数を読み込む
load_dotenv()

# 環境変数から接続情報を取得
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_SSL_CA = os.getenv('DB_SSL_CA')

# 接続文字列を生成
DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}?ssl_ca={DB_SSL_CA}"

engine = create_engine(
    DATABASE_URL,
    echo=True  # SQLログを表示したい場合はTrueに設定
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
