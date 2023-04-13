import mysql.connector
import requests
import json
import datetime
import pandas as pd
from sklearn import linear_model
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn import preprocessing
from IPython.display import display

def machine_learn(stnID, dateordinal):
    #Connect to MySQLServer with proper db
    mydb = mysql.connector.connect(
    host="",
    user="",
    password="",
    database="DBikeDynamicV2"
    )

    #getting info from db into dicts
    sql = """
    SELECT ID, AvailableBike, DateTime FROM Dynamic;
    """

    mycursor = mydb.cursor()
    mycursor.execute(sql)
    data = mycursor.fetchall()

    mycursor.close()
    mydb.close() 

    #idlis is the ID, for reference
    idlis = [item[0] for item in data]

    #nb is the number of bikes available
    nb = [item[1] for item in data]

    #dt is the day and time
    dt = [item[2] for item in data]

    #converting lists to dataframe
    dfdata = {'ID': idlis, 'numbike': nb, 'date': dt}
    df = pd.DataFrame(dfdata)

    #converting date to date ordinals
    df['date_ordinal'] = pd.to_datetime(df['date']).apply(lambda date: date.toordinal())

    #combining independent variables and setting depedent variable
    independent = df[['ID', 'date_ordinal']]
    dependent = df['numbike']

    #train test split
    X_train, X_test, y_train, y_test = train_test_split(
        independent, dependent, test_size=0.3, random_state=101)

    #linear regression model
    regr = linear_model.LinearRegression()
    regr.fit(X_train, y_train)

    predictedavail = regr.predict(X_test)
    y_test = np.array(list(y_test))

    #comaprison between actual and comparison
    #sdf = pd.DataFrame({'Actual': y_test.flatten(), 'Predicted': predictedavail.flatten()})
    #display(sdf)


    #predicts with data passed in function call
    finaldfdata = {'ID': [stnID], 'date_ordinal': [dateordinal]}
    finaldf = pd.DataFrame(finaldfdata)
    return regr.predict(finaldf)




