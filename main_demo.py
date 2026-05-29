from fastapi import FastAPI
from fastapi import Depends
app=FastAPI()

# USERS={}

from pydantic import BaseModel

class UserSignup(BaseModel):
    username:str
    password:str

class UserSignin(BaseModel):
    username:str
    password:str
#? ------------------------------------------------------
# ! InMemory storage part 

# @app.post("/signup")
# def signup(user:UserSignup):
#     USERS[user.username]={'password':user.password}
#     print(USERS)
#     return {"message":"User created suceesfully"}
#?---------------------------------------------------------
# user: UserSignup , is a type hint.
# It tells FastAPI:
#"Incoming request body should be converted into a UserSignup object.

@app.get("/")
def home():
    return {
        'message':"Welcomne to  the Landing Page"
    }


from database import get_db
from models import User
@app.post("/signup")
def signup(user:UserSignup,db=Depends(get_db)):
    # You are deciding Which Pydantic field maps to which ORM field
    db_user=User(
        username=user.username,
        password=user.password
    )
 
    existing_user=db.query(User).filter(User.username==user.username).first()
    print("The type of exist_user is,ing",type(existing_user))
    if existing_user is None:
        db.add(db_user)
        db.commit()
        return {"message":" A New User created suceesfully"}
    else:
        return{"message":"user Already exist"}



#? Note
#? filter(User.username==user.username) This line is equivalent to 
#? SQL WHERE expression object , its not the pythonic way of comparsion
# ? 'user' is the object instance of original request body , 
# ? but 'User' is the class of users table so User.username is It is: 
# a special SQLAlchemy column descriptor object
# representing:
# "username column in users table"

# So This
# .filter(User.username == user.username)

# conceptually becomes:

# WHERE username = 'prabhat'
'''
    SELECT * FROM users
    WHERE username = ?
    LIMIT 1;
'''

#! What exactly is Depends and why its used ?? 
'''

1- Depends is a utility provided by FastAPI.
It tells FastAPI:
"This parameter should be provided by another function."

2-This Line -->db = Depends(get_db) means:
"FastAPI, before executing signup(),
run get_db() and put its result into db."

'''
# user: UserSignup ,,--> Comes from HTTP request body
# db = Depends(get_db) --> Comes from FastAPI dependency system

#? I m creating this route to just test the users using the route/users
from models import User
@app.get("/users")
def users(db=Depends(get_db)):
    users=db.query(User).all()
    usernames=[]
    for user in users:
         usernames.append(user.username)
         print(user.username)
    return (usernames)

# ---------------------------------------------------------

@app.post("/signin")
def signin(user:UserSignin,db=Depends(get_db)):
    db_user=db.query(User).filter(user.username==User.username).first()
    #User not found
    if db_user is None:
        return {
            "message": "User does not exist"
        }

    # Password check
    if db_user.password != user.password:
        return {
            "message": "Incorrect password"
        }

    # Success
    return {
        "message": "Signin successful"
    }

#?-------------
'''
Where:

User.username
→ database column
user.username
→ incoming request body value
Very important distinction.
'''
