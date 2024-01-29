from fastapi import FastAPI, HTTPException
from tortoise.contrib.fastapi import register_tortoise
from contextlib import asynccontextmanager
from Database import start_db_client,shutdown_db_client
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.exceptions import DoesNotExist
from passlib.context import CryptContext
from app.models import User_s,createUser
from dotenv import load_dotenv    
import os


load_dotenv()

database_url=os.getenv("DATABSEURL")




   

User_Pydantic=pydantic_model_creator(User_s)




asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    await start_db_client()

    yield
    # Clean up the ML models and release the resources
    await shutdown_db_client()







crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI(lifespan=lifespan)



@app.get("/")
async def read_root():
    return{"hello":"world"}




@app.post("/adduser/")
async def adduser(name:str,password:str):
    try:
            hpassword = crypt_context.hash(password)
            user = await User_s.create(name=name,password=hpassword)

            return {"message":"User created","user_id":user.id}
    


    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    


@app.put("/updateuser/{user_id}")
async def updateuser(user_id:int, updatename:createUser):
    user= await  User_s.get(id=user_id)

    if user is None:
         raise HTTPException (status_code=404,detail="User Not Found")
    
    else:
        user.name =updatename.name
        user.password=updatename.password
        await user.save()

        return {"message":"Data Has Been Updated"}




@app.get("/getusers/")
async def getuser():
    try:
        users= await User_s.all()
        for user in users:
                data=[{
                    "id":user.id,
                "name": user.name,
                "password":  user.password
                }]
        return data
    except Exception as s:
        raise HTTPException(status_code=500,detail=str(s))
    


@app.get("/getusers/{user_id}")
async def getuserby_id(user_id:int):

    try:
        user=await User_s.get(id=user_id)
        return {"name":user.name,
                "password":user.password}
    except DoesNotExist:
        err={
            "message":f"User with id no {user_id} does not Exist"
        }
        raise HTTPException(status_code=404, detail=err )
    except Exception as e:
        raise HTTPException (status_code=500,detail=str(e))


@app.delete("/deleteuser/{user_id}")
async def deleteuser(user_id:int):

    try : 
        user=await User_s.get(id=user_id)
        await user.delete()
        return{
            "message":"User Deleted Sucessfully"
        }
    except DoesNotExist:
        err={
            "message":f"User with id no {user_id} does not Exist"
        }
        raise HTTPException(status_code=404,detail=err)
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))




            





register_tortoise(
      app,
      db_url=database_url,
    modules={'models': ['app.models']},
        
    generate_schemas=True,
    add_exception_handlers=True,


)

