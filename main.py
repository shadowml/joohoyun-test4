# from fastapi import FastAPI
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel

import joblib
import pandas as pd
import numpy as np
from sklearn import linear_model
import requests
import pickle

app = FastAPI()

db = []

class City(BaseModel):
    name: str
    timezone: str

@app.post("/uploadfile")
def check(file: UploadFile = File(...)):
    if file.filename.endswith('.csv'):
        df = pd.read_csv(file.file)
        df_head = df.head(5)
        df_tail = df.tail(5)
        # cli.set("userId",str(df))
        head = df_head.to_json(orient='records')
        tail = df_tail.to_json(orient='records')
        head = eval(head)
        tail = eval(tail)
        # create_db_table()
        # insert_data(uuid=1,itemname=file.file.read())
        # final return
        return {
            "head":head,
            "tail":tail
        }


@app.get('/predict')
def predict_fun(propsize: int=1000):
    df = pd.read_csv("homeprices.csv")

    model = linear_model.LinearRegression()
    # model.fit(features, label-class)
    model.fit(df[['area']],df.price)

    predict1=model.predict([[propsize]])

    predict1_list=predict1.tolist()
    print(type(predict1_list))
    print(predict1_list)

    return {"info":predict1_list}


@app.get('/predict-chris')
def predict_fun(propsize: int=1000):
    df = pd.read_csv("homeprices.csv")

    model = linear_model.LinearRegression()
    # model.fit(features, label-class)
    model.fit(df[['area']],df.price)

    predict1=model.predict([[propsize]])

    predict1_list=predict1.tolist()
    print(type(predict1_list))
    print(predict1_list)

    return {"info":predict1_list}

@app.get('/predict-chris-2')
def predict_fun(propsize: int=1000):
    df = pd.read_csv("homeprices.csv")

    model = linear_model.LinearRegression()
    # model.fit(features, label-class)
    model.fit(df[['area']],df.price)

    predict1=model.predict([[propsize]])

    predict1_list=predict1.tolist()
    print(type(predict1_list))
    print(predict1_list)

    return {"info":predict1_list}

@app.get('/predict-model')
def predict_model(propsize: int=1000):
    with open('model_pickle','rb') as file:
        mp = pickle.load(file)
    predict1=mp.predict([[propsize]])

    predict1_list=predict1.tolist()
    print(type(predict1_list))
    print(predict1_list)

    return {"info model":predict1_list}

@app.get('/predict-model-tf')
def predict_model_tf(sample_url:str):
    with open('phishing.pkl','rb') as file:
        mp = pickle.load(file)

    predict_bad = ['17d515558faae741a3d0f9ced348e61a39eda6f62e153eb78e44e3ac3a0515b9','fazan-pacir.rs/temp/libraries/ipad','tubemoviez.exe','svision-online.de/mgfi/administrator/components/com_babackup/classes/fx29id1.txt']
    # predict_good = ['shop.calbears.com/?_s=google-ak19kv30-college-sp-campaign&adposition=&gclid=CjwKCAjw5p_8BRBUEiwAPpJO61FRX9tZH61coc4DG4khqrzunv06f5aStK0QrTmsQ_0kzsMeIVyx5RoCbuwQAvD_BwE&ks_id=6248_kw17915148&matchtype=e&pcrid=163221222456&target=kwd-1555141972&utm_campaign=NCAA+-+Brand+-+California+Bears%7C704709320&utm_medium=ppc&utm_source=g&utm_term=uc+berkeley+bookstore','youtube.com/watch?v=qI0TQJI3vdU','retailhellunderground.com/','restorevisioncenters.com/html/technology.html']
    predict_good=[sample_url]

    # result2 = mp.predict(predict_good)
    result2 = mp.predict(predict_good)
    predict1_list = result2.tolist()

    return {"info tensorflow": predict1_list}

    # predict1=mp.predict([[propsize]])

    # predict1_list=predict1.tolist()
    # print(type(predict1_list))
    # print(predict1_list)
    #
    # return {"info model":predict1_list}


@app.get('/')
def index():
    return {'key' : 'test2'}

@app.get('/cities')
def get_cities():
    results = []
    for city in db:
        r = requests.get(f'http://worldtimeapi.org/api/timezone/{city["timezone"]}')
        print(r.json())
        current_time = r.json()['datetime']
        results.append({'name' : city['name'], 'timezone': city['timezone'], 'current_time': current_time})
    return results

@app.get('/cities/{city_id}')
def get_city(city_id: int):
    city = db[city_id-1]
    r = requests.get(f'http://worldtimeapi.org/api/timezone/{city["timezone"]}')
    current_time = r.json()['datetime']
    return {'name' : city['name'], 'timezone': city['timezone'], 'current_time': current_time}

@app.post('/cities')
def create_city(city: City):
    db.append(city.dict())
    return db[-1]

@app.delete('/cities/{city_id}')
def delete_city(city_id: int):
    db.pop(city_id-1)
    return {}

@app.get("/get_csv")
async def get_csv():
    from fastapi.responses import StreamingResponse
    from io import StringIO
    import io
    datastuff =  {'colors':['blue','red'],'volume':[22,55]}
    df=pd.DataFrame(datastuff)
    response=StreamingResponse(io.StringIO(df.to_csv(index=False)), media_type="text/csv")
    response.headers["Content-Disposition"]="attachment; filename=export-999.csv"
    return response

# class City(BaseModel):
#     name: str
#     timezone: str

# {'abbreviation': 'EDT', 'client_ip': '68.231.197.86', 'datetime': '2020-10-22T20:17:37.809144-04:00', 'day_of_week': 4, 'day_of_year':
# 296, 'dst': True, 'dst_from': '2020-03-08T07:00:00+00:00', 'dst_offset': 3600, 'dst_until': '2020-11-01T06:00:00+00:00', 'raw_offset':
# -18000, 'timezone': 'America/New_York', 'unixtime': 1603412257, 'utc_datetime': '2020-10-23T00:17:37.809144+00:00', 'utc_offset': '-04:
# 00', 'week_number': 43}



# [
#   {
#     "name": "Miami",
#     "timezone": "America/New_York",
#     "current_time": "2020-10-22T20:22:21.069020-04:00"
#   }
# ]
