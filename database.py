from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URI = "postgresql://root:aNXZbeeiU52r5oRXCdN1N56qavu3dqHv@dpg-cfgkdrpa6gdma8h2oobg-a.frankfurt-postgres.render.com/testdb2_7cq3"

engine = create_engine(SQLALCHEMY_DATABASE_URI)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()
