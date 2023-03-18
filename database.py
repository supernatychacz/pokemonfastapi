from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URI = "postgresql://testdb_xz97_user:UsJlYSEKzM00sFoKdHkzEgWw51nJuR2x@dpg-cfpqqs82i3mo4bsq46vg-a.oregon-postgres.render.com/testdb_xz97"

engine = create_engine(SQLALCHEMY_DATABASE_URI)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()
