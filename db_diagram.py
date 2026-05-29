import urllib.parse
from eralchemy2 import render_er

# 1. We isolate the password and encode the '@' symbol to '%40' so eralchemy2 doesn't trip over it
safe_password = urllib.parse.quote_plus("pushpakviman@123")

# 2. Hardcode the connection string locally just for this visualization tool
local_db_url = f"postgresql+psycopg2://prabhat:{safe_password}@localhost:5432/cex_db"

print("Parsing database structure and drawing relations...")

# 3. Render the layout directly
render_er(local_db_url, 'exchange_schema.png')

print("Success! Diagram generated cleanly as exchange_schema.png")