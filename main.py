from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from backend.routes import router
app = FastAPI()   

app.include_router(router)
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ =='__main__':
    uvicorn.run(app,host='localhost',port=8000)



