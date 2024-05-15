from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

dotenv_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path)

# SQLALCHEMY_DATABASE_URL = 'sqlite:///./flask_app.db'
SQLALCHEMY_DATABASE_URL = ''

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Model(DeclarativeBase):
    pass



