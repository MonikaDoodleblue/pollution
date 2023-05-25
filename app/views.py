from django.http import JsonResponse
import mysql.connector
import matplotlib
from django.http import HttpResponse
import matplotlib.pyplot as plt
import io
import json
import requests
from django.shortcuts import render, redirect
import numpy as np
import pandas as pd
import joblib


model = joblib.load(
    'C:/Users/Monika/OneDrive/Documents/airpollution/pollution/app/RF.pkl')


def home(request):
    return render(request, "home.html")

def chart(request):
    return render(request, "chart.html")

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        cnx = mysql.connector.connect(user='newuser', password='monikamysql03',
                                      host='localhost', database='pollution')
        cursor = cnx.cursor()

        query = "INSERT INTO usertable (username, password, email) VALUES (%s, %s, %s)"
        values = (username, password, email)
        cursor.execute(query, values)
        cnx.commit()

        return redirect('register')
    else:
        return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        cnx = mysql.connector.connect(user='newuser', password='monikamysql03',
                                      host='localhost', database='pollution')
        cursor = cnx.cursor()

        query = "SELECT password FROM usertable WHERE username = %s"
        values = (username,)
        cursor.execute(query, values)
        result = cursor.fetchone()

        if result and result[0] == password:
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    else:
        return render(request, 'login.html')


def predict(request):
    if request.method == 'POST':
        return render(request, 'index.html')
    else:
        return render(request, 'index.html')


def predict(request):
    if request.method == "POST":

        df = pd.read_csv(
            'C:/Users/Monika/OneDrive/Documents/airpollution/pollution/city_day.csv')

        AQI = request.POST.get('AQI', None)
        City = request.POST.get('City', None)

        if AQI is not None:

            df_filtered = df[(df['AQI'] == float(AQI)) &
                             (df['City'] == str(City))]

            aqi = df_filtered['AQI'].values[1]
            pm10 = df_filtered['PM10'].values[0]
            no = df_filtered['NO'].values[0]
            no2 = df_filtered['NO2'].values[0]
            nox = df_filtered['NOx'].values[0]
            nh3 = df_filtered['NH3'].values[0]
            co = df_filtered['CO'].values[0]
            so2 = df_filtered['SO2'].values[0]
            o3 = df_filtered['O3'].values[0]
            benzene = df_filtered['Benzene'].values[0]
            toluene = df_filtered['Toluene'].values[0]
            xylene = df_filtered['Xylene'].values[0]
            aqi_bucket = df_filtered['AQI_Bucket'].values[0]

            output_dict = {
                'AQI': aqi,
                'PM10': pm10,
                'NO': no,
                'NO2': no2,
                'NOx': nox,
                'NH3': nh3,
                'CO': co,
                'SO2': so2,
                'O3': o3,
                'Benzene': benzene,
                'Toluene': toluene,
                'Xylene': xylene,
                'AQI_Bucket': aqi_bucket,
            }

            return render(request, 'index.html', {'prediction_text': output_dict})

    return render(request, 'index.html')


def news(request):
    url = "http://api.mediastack.com/v1/news"
    params = {
        "access_key": "9c605c0c66e13ee34dfce48d04d682f2",
        "keywords": "pollution",
        "countries": "in,us",
    }
    response = requests.get(url, params=params)
    news_data = response.json()
    return render(request, "news.html", {"news_data": news_data})


matplotlib.use('Agg')


# def chart(request):
#     df = pd.read_csv(
#         'C:/Users/Monika/OneDrive/Documents/airpollution/pollution/city_day.csv')

#     fig, ax = plt.subplots()

#     ax.plot(df['Date'], df['AQI'])

#     ax.set_xlabel('Date')
#     ax.set_ylabel('AQI')
#     ax.set_title('Air Pollution Data')

#     buffer = io.BytesIO()
#     plt.savefig(buffer, format='png')
#     buffer.seek(0)

#     return HttpResponse(buffer, content_type='image/png')


# def chart(request):
#     df = pd.read_csv(
#         'C:/Users/Monika/OneDrive/Documents/airpollution/pollution/city_day.csv')

#     # Create chart data as a dictionary
#     chart_data = {
#         'labels': list(df['Date']),
#         'data': list(df['AQI'])
#     }

#     # Return chart data as JSON response
#     return JsonResponse(chart_data)