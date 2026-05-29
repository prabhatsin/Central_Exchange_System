# #! -------------------------------------
# from pydantic import BaseModel
# # Pydantic is the most widely used data validation
# #Used ONLY for incoming API data
# #You just created a request validation schema
# class UserSignup(BaseModel):
#     user_name: str
#     password:str

# import asyncio
# async def async_func():
#     return "hello"

# result = asyncio.run(async_func())     # "hello"
# print(result)



from fastapi import FastAPI
import time

app = FastAPI()

@app.get("/slow")
def slow_sync():
    time.sleep(10)  # Blocks everything! 😢
    return {"message": "Done after 10 seconds"}

# Try this: Open two browser tabs to /slow
# Second request will wait 3 seconds AFTER first finishes
# Total time: 6 seconds for two requests
