# from database import engine, Base
# # import models

# # Base.metadata.drop_all(bind=engine)

# # Base.metadata.create_all(bind=engine)


# #! Issuee with this scripty is it will delete all the tables and then recreate all 
# # Later on learn to remove a particuylar tabole/column or anything  u want to 
# # Not just simply deleteing everything 
# #! TODO:
# # Later you'll learn Alembic for proper schema evolution.

# #? This part of code helps in looking at the table names anede columns in users table 

# from sqlalchemy import inspect
# inspector = inspect(engine)
# print(inspector.get_table_names())
# columns = inspector.get_columns("users")
# for column in columns:
#     print(column["name"])


USERS = {
    1: {
        "username": "prabhat",
        "password": "abc123"
    },
    2: {
        "username": "rahul",
        "password": "rahul@123"
    },
    3: {
        "username": "amit",
        "password": "amit@456"
    }
}
userid=[key for key in USERS]
print(userid) 
