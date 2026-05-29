
#! TODO asy Future Refactor

#? Later you can split:
#? routes/
#? services/
#? WITHOUT changing DB layer.



#! This script contains Signup/Login API routes 

from fastapi import FastAPI 
app=FastAPI()

@app.get("/")
def home():
    return {
        'message':"server is running fine for now"
    }

# This method uses body() method , recomended is Pydantic way 
from fastapi import Body
@app.post("/signup")
def signup(username:str=Body(), #Tells FastAPI: look for "username" inside the JSON body
           email:str=Body(),):  # Tells FastAPI: look for "email" inside the JSON body
    
    return {"username":username, 'email':email}

#! EmailStr use case 
##What it DoesSyntax Checking: 
##Ensures the email follows valid formats (e.g., checking for the @ symbol, proper placement of dots, and no illegal characters).
##Domain Validation: Checks if the email domain actually exists by querying DNS records.
##Automatic Normalization: Converts email addresses into a standardized format (e.g., converting parts of the email to lowercase) upon successful validation.



#! Note
# SQLAlchemy ORM ---DB table
# Pydantic -- Request validation 

