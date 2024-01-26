from tortoise import Tortoise,run_async
from Database import start_db_client





async def main():
    await start_db_client()
    await Tortoise.generate_schemas()

if __name__=='__main___':
    run_async(main())