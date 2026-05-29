
from sqlalchemy.engine import URL 
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv


# Put this inside the.env file 

#? URL creation 

load_dotenv()
# url=os.getenv("DATABASE_URL")
db_url = URL.create(
    drivername="postgresql",
    username="prabhat",
    password="pushpakviman@123",  # Write your raw password here naturally! No %40 needed.
    host="localhost",
    port=5432,
    database="cex_db"
)

#? engine creation

engine=create_engine(db_url,echo=True)
### whats this echo=True
# ---> Prints every SQL statement SQLAlchemy generates to stdout
# ---> Very useful for debugging — you see exactly what queries run

#? 
from sqlalchemy.orm import sessionmaker

SessionLocal = sessionmaker(bind=engine)

# db=SessionLocal()
# one global session shared across all requests
# is not the correct FastAPI architecture.
# Instead what we want is A function that CREATES a fresh session per request



def get_db():
    db=SessionLocal()
    try:
        yield db 
    finally:
        db.close()

'''
WHY yield INSTEAD OF return?
This is the most important conceptual point.
If you used:  return db
then:  function ends immediately
No automatic cleanup lifecycle.
But yield creates:
setup → temporary usage → cleanup
pattern.
This is perfect for DB sessions.
'''
#  declarative base class
class Base(DeclarativeBase):
    pass
