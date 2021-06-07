from fastapi import FastAPI

# from enum import Enum

# class ModelName(str, Enum) :
#     alexnet = "alexnet"
#     resnet = "resnet"
#     lenet = "lenet"

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

# @app.get("/models/{model_name}")
# async def get_model(model_name: ModelName):
#     if model_name == ModelName.alexnet:
#         return {"model_name" : model_name, "message" : "Deep Learning FTW!"}
#     if model_name.value == "lenet":
#         return {"model_name" : model_name, "message" : "LeCNN all the images"}
#     return {"model_name" : model_name, "message" : "LeCNN all the images"}

# @app.get("/users/me")
# async def read_user_me():
#     return {"user_id": "the current user"}

