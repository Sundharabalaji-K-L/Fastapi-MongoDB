from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers.cars import router as cars_router
from routers.users import router as users_router
from motor import motor_asyncio
from config import BaseConfig
from fastapi.middleware.cors import CORSMiddleware


settings = BaseConfig()


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.client = motor_asyncio.AsyncIOMotorClient(settings.DB_URL)
    app.db = app.client[settings.DB_NAME]

    try:
        app.client.admin.command('ping')
        print("Pinged your deployment. You have successfully connected to mongoDB!")
        print("Mogo address: ", settings.DB_URL)

    except Exception as e:
        print(e)

    yield

    app.client.close()
    

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(cars_router, prefix="/cars", tags=["cars"])
app.include_router(users_router, prefix="/auth", tags=["auth"])
@app.get('/')
async def get_root():
    return {'message': 'Root working!'}
