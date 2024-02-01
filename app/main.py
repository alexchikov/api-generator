from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
import os
import http


app = FastAPI()

@app.get('/')
def get_root():
    return {"message":"Hello"}

@app.get("/orders/{id}")
def get_order(id):
    dir_ls = os.listdir('../files/orders')
    print(dir_ls)
    for filename in dir_ls:
        if filename.split('_')[1] == str(id):
            return FileResponse(f'../files/orders/{filename}', 
                                filename=filename,
                                media_type="applicatino/octet-stream")
    return JSONResponse({"message": "Not found"}, status_code=http.HTTPStatus.NOT_FOUND)

@app.get("/orders/")
def get_order_scheme():
    dir_ls = list(map(lambda x: int(x.split('_')[1]), os.listdir('../files/orders')))
    return {'orders_ids': sorted(dir_ls)}