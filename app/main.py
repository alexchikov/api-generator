from fastapi import FastAPI
from fastapi.responses import FileResponse
import os
import http


app = FastAPI()

@app.get('/')
def get_root():
    return {"message":"Hello"}

@app.get("/orders/{id}")
def get_order(id):
    dir_ls = os.listdir('../files/orders')
    for filename in dir_ls:
        print(dir_ls)
        if filename.split('_')[1] == str(id):
            return FileResponse(f'../files/orders/{filename}', 
                                filename=filename,
                                media_type="applicatino/octet-stream")
    return http.HTTPStatus.NOT_FOUND