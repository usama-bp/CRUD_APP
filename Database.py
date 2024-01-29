
from tortoise import Tortoise, fields,run_async
from dotenv import load_dotenv
import os
# from dotenv import load_dotenv    

load_dotenv()

database_url=os.getenv("DATABASE_URL")


async def start_db_client():

    # database_url=load_dotenv("DATABSE_URL")    
    await Tortoise.init(
        # db_url='sqlite://db.sqlite3',
         db_url=database_url,
        modules={'models': ['app.models']}
    )
    await Tortoise.generate_schemas()

async def shutdown_db_client():
     await Tortoise.close_connections()
    






