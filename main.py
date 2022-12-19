
from flask import Flask,request
import json
from flask_cors import CORS
from flask_restful import Resource, reqparse, Api
import yfinance as yf
from datetime import date
import pandas as pd
import requests
import yfinance as yf
from fbprophet import Prophet
import numpy as np

app = Flask(__name__)
CORS(app)
Api(app)

START = "2022-01-01"
TODAY = date.today().strftime("%Y-%m-%d")
DAYS1 = "2022-12-01"
DAYS2 = "2022-12-05"

@app.route('/',methods=['POST'])
def connect():
    args = request.json

    name = args['name']
    print(args)

    datas = {'Page':'Connect','Message':f'Gain Access now {name}'}
    data_json = json.dumps(datas)
    return data_json;


@app.route('/stockData',methods=['POST'])
def dataStock():
    args = request.json

    # print(args) 
    
    #get passing value
    stockname = args['stock']
    startDate = args['startDate']
    lastDate = args['lastDate']

    print("stock " + stockname)

    data = yf.download(stockname , startDate, lastDate)
    data.reset_index(inplace=True)

    result = pd.DataFrame.to_json(data) #result for data stock

    print("result")
    print(result)

    return result;

@app.route('/lstm',methods=['POST'])
def lstm():
    return ""
    

@app.route('/fbprophet',methods=['POST'])
def fbpro():
    args = request.json

    print(args) 
    
    #get passing value
    stockname = args['stock']
    startDate = args['startDate']
    lastDate = args['lastDate']
    period = int(args['period'])

    #period = years * 365
    #period = 7

    data = yf.download(stockname , startDate, lastDate)
    data.reset_index(inplace=True)

    result = pd.DataFrame.to_json(data) #result for data stock

    # Forecasting
    df_train = data[{'Date','Close'}]
    df_train = df_train.rename(columns={"Date": "ds", "Close":"y"})

    #prediction using prophet
    m = Prophet()
    m.fit(df_train)
    future = m.make_future_dataframe(periods=period)
    forecast = m.predict(future)

    # print("actual")
    # print(df_train['y'])

    # print("predict")
    # print(forecast['yhat'])

    df_actual = pd.DataFrame(df_train)
    df_predict = pd.DataFrame(forecast[{'ds','yhat'}])

    df_join = df_predict.join(df_actual.set_index('ds'), on='ds')

    print("actual")
    print(df_actual)

    print("predict")
    print(df_predict)

    print("join")
    print(df_join)

    #forecastResult = pd.DataFrame.to_json(forecast)
    forecastResult = pd.DataFrame.to_json(df_join)

    print("forecast")
    #print(forecastResult)

    #return result;
    return forecastResult


@app.route('/stocknews',methods=['GET'])
def stocknews():

    api = 'https://api.polygon.io/v2/reference/news?limit=100&apiKey=X9nrIiYxl0zQAWHFfi6ZImIuLXoXT3VJ'

    data = requests.get(api).json()

    print(data)

    return data

@app.route('/getStocks',methods=['POST'])
def getStocks():
    
    args = request.json

    # print(args) 
    
    #get passing value
    stockname = args['stock']
    startDate = args['startDate']
    lastDate = args['lastDate']

    # countStock = len(stockname)

    # print(f'countStock {countStock}')

    # for st in stockname:
    #     print(st)
    #     result = getStock(st,startDate,lastDate)
    #     dataStock.update(result)
    
    data = yf.download(stockname , startDate, lastDate)
    data.reset_index(inplace=True)

    stockData = pd.DataFrame.to_json(data) #result for data stock
    print(stockData)

    return stockData

def getStock(name,startDate,lastDate):
    #print(name)

    data = yf.download(name , startDate, lastDate)
    data.reset_index(inplace=True)

    stockData = pd.DataFrame.to_json(data) #result for data stock
    print(stockData)
    
    return stockData

@app.route('/getPredict',methods=['POST'])
def getPredict():

    # CREATE ONE FUNCTION THAT CALLED MULTIPLE PREDICITON FUNCTION

    # getPredict() --- called multiple -- fbpro()

    args = request.json

    # print(args) 
    
    #get passing value
    stockname = args['stock']
    startDate = args['startDate']
    lastDate = args['lastDate']
    period = int(args['period'])

    print(stockname)

    for x in stockname:
        print(f'stock {x}')

        name = x
        # call fbpro function / or create new like fbpro

    return ""



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)