from fastapi import FastAPI

app = FastAPI()

BALANCES = {

}

ORDERBOOKS = {
    "SOL": {},
    "BTC": {}
}

# ----This Section of code does the validation part 
from pydantic import BaseModel
class UserSignup(BaseModel):
    username:str
    password:str


# user
# This is the actual object instance created from incoming request data.

# user is now an OBJECT.
# Specifically:
# instance of UserSignup

@app.post("/signup")
def signup(user:UserSignup):
    pass

'''
What FastAPI Does Internally
Suppose request body is:
{
   "username": "prabhat",
   "password": "123"
}
FastAPI internally does roughly:
user = UserSignup(
    username="prabhat",
    password="123"
)
'''

@app.post("/signin")
def signin():
    pass


"""
    body = {
        type:           "market" | "limit",
        price:          number | null,
        qty:            number,
        market_id:      string,
        side:           "buy" | "sell"
    }

    @returns {
        orderId: string,
        filledQty: number,
        averagePrice
    }
"""

# 50.01

# 500001
@app.post("/order")
def create_order():
    pass


"""
    returns the status of an order (partially filled, success, cancellled)
    ALSO RETURNS THE INDIVIDUAL FILLS OF THIS ORDER
"""
@app.get("/order/{orderId}")
def get_order(orderId: str):
    pass


@app.delete("/order/{orderId}")
def delete_order(orderId: str):
    pass


@app.get("/depth/{symbol}")
def get_depth(symbol: str):
    pass


@app.get("/orders")
def get_orders():
    pass


@app.get("/fills")
def get_fills():
    pass


@app.get("/balance/usd")
def get_usd_balance():
    pass


"""
    Returns the balance of all stocks
"""
@app.get("/balance")
def get_balance():
    pass
