import time
import os
import numpy as np
import pandas as pd
# Must install package matplotlib
import matplotlib.pyplot as plt
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import create_engine, MetaData, event, schema
from sqlalchemy import Table, Column, Date, Integer, Float, VARCHAR ,ForeignKey
# from sqlalchemy.orm import sessionmakere
from sqlalchemy_utils import database_exists,create_database


#  ******************************** part 1 AND 2 ********************************************
def read_given_file(f,use_sem_col):
    # reads CSV file into a pandas dataframe
    # return pd.read_csv(f,  sep=';',comment='#',skiprows=[1])    
    if use_sem_col:
      return pd.read_csv(f,  sep=';',comment='#',dtype='unicode')
    else:
      return pd.read_csv(f,  sep=',',comment='#',dtype='unicode')

try:
    '''**********************************************************************
    Main unit for Data sets
    '''
    # Create a new SQLite database
    csv_file = '//home//yuy4//weather_data_2020.csv'
    df = pd.read_csv(csv_file)
    print(list(df.columns))
    print(list(df.dtypes))
    print("Analyzed, found " +  str(df.shape[0]) + " rows; " + str(df.shape[1]) + " cols.")
    Sqlite_Server      = 'sqlite:///'
    my_path = '//home//yuy4//'
    DB_NAME_ = 'weatherdate_1.db'
    WEATHER_ = 'weather_data_2020'
    
    # Create an engine object
    Engine = create_engine(Sqlite_Server + my_path + DB_NAME_, echo=False)
    Sqlite_Conn = Engine.connect()
    if not Sqlite_Conn:
        print("DB connection is not OK!")
        exit()
    else:
        print("DB connection is OK.")
        
    # CREATE TABLE
    Engine.execute('CREATE TABLE IF NOT EXISTS "Place" ('
                   'code INT64 PRIMARY KEY NOT NULL,'
                   'name OBJECT NOT NULL,'
                   'latitude FLOAT64 NOT NULL,'
                   'longitude FLOAT64 NOT NULL);'
                  )

    Engine.execute('CREATE TABLE IF NOT EXISTS "Observation" ('
                   'place OBJECT NOT NULL,'
                   'date DATETIME PRIMARY KEY NOT NULL,'
                   'rain FLOAT64,'
                   'snow FLOAT64,'
                   'air temperature FLOAT64,'
                   'ground temperature FLOAT64);'
                  )

    Engine.execute('CREATE TABLE IF NOT EXISTS "Temperature" ('
                   'place OBJECT,'
                   'date DATETIME PRIMARY KEY NOT NULL,'
                   'lowest FLOAT64,'
                   'highest FLOAT64);'
                  )

    place_cols = ['place_code','place','latitude','longitude']
    Place = df[place_cols]
    Place.rename(columns={'place_code':'code','place':'name','latitude':'latitude','longitude':'longitude'}, inplace = True)
    
    date = pd.to_datetime(df[['year','month','day']])
    date = date.dt.date
    df.insert(df.shape[1],'date',date)
    Observation_cols = ['place','date','rain','snow','air_temperature','ground_temperature']
    Observation = df[Observation_cols]
    Observation.rename(columns={'air_temperature':'air temperature','ground_temperature':'ground temperature'}, inplace = True)
    Observation['rain'].replace(-1,0,inplace=True)
    Observation['snow'].replace(-1,0,inplace=True)
    
    Temperature_cols = ['place','date','lowest_temperature','highest_temperature']
    Temperature = df[Temperature_cols]
    Temperature.rename(columns={'lowest_temperature':'lowest','highest_temperature':'highest'}, inplace=True)
    
    Observation.fillna('NULL')
    Temperature.fillna('NULL')
    
    Place.to_sql('Place', Sqlite_Conn, if_exists='replace', index=False)
    Observation.to_sql('Observation', Sqlite_Conn, if_exists='replace', index=False)
    Temperature.to_sql('Temperature', Sqlite_Conn, if_exists='replace', index=False)

    print(Engine.execute("SELECT * FROM Place").fetchall())
    print(Engine.execute("SELECT * FROM Observation").fetchall())
    print(Engine.execute("SELECT * FROM Temperature").fetchall())

    #  ******************************** part 3 ********************************************
    # question(a)    
    sql_snowday = """
                  SELECT count(*) AS SnowDay, OV.place
                  FROM Observation AS OV
                  WHERE OV.snow > 0
                  GROUP BY place;
                  """
    test_snowday = pd.read_sql_query(sql_snowday,Sqlite_Conn)
    print(test_snowday)
    print('----------------------------------------------------------------')
    
    sql_mostsnow = """
                    with mostsnow AS
                    (SELECT MAX(SnowyDay) AS maxsnowday, OVP
                    FROM (
                    SELECT count(*) AS SnowyDay, OV.place AS OVP
                    FROM Observation AS OV
                    WHERE OV.snow > 0
                    GROUP BY place)),

                    snoweachmonth AS
                    (SELECT SUM(snow) AS sumsnow, strftime('%m',date) as month
                    FROM Observation,mostsnow
                    WHERE Observation.place = mostsnow.OVP
                    GROUP BY month)

                    SELECT goal.goalmonth,MAX(goal.snowgoal) AS sumsnow FROM 
                    (SELECT DISTINCT Observation.place,SEM.month AS goalmonth,SEM.sumsnow AS snowgoal FROM Observation,mostsnow,snoweachmonth AS SEM
                    WHERE Observation.place = (mostsnow.OVP) AND snow IS NOT NULL AND snow > 0
                    GROUP BY SEM.month) AS goal;
                   """
    test_mostsnow = pd.read_sql_query(sql_mostsnow,Sqlite_Conn)
    print(test_mostsnow)
    print('----------------------------------------------------------------')
    
    sql_leastsnow = """
                    with leastsnow AS
                    (SELECT MIN(SnowyDay) AS minsnowday, OVP
                    FROM (
                    SELECT COUNT(*) AS SnowyDay, OV.place AS OVP
                    FROM Observation AS OV
                    WHERE OV.snow > 0
                    GROUP BY place)),

                    mostsnowday AS
                    (SELECT COUNT(*) AS countsnowday, strftime('%m',date) as month
                    FROM Observation,leastsnow
                    WHERE Observation.place = leastsnow.OVP AND snow > 0 AND snow IS NOT NULL
                    GROUP BY month)

                    SELECT goal.goalmonth,MAX(goal.countsnowday) AS mostsnowday FROM
                    (SELECT DISTINCT Observation.place,MSD.month AS goalmonth,MSD.countsnowday AS countsnowday FROM Observation,leastsnow,mostsnowday AS MSD
                    WHERE Observation.place = (leastsnow.OVP) AND snow IS NOT NULL AND snow > 0
                    GROUP BY MSD.month) AS goal;
                    """
    test_leastsnow  = pd.read_sql_query(sql_leastsnow,Sqlite_Conn)
    print(test_leastsnow)
    print('----------------------------------------------------------------')
    
    # question(b)
    sql_tem_filter = """
                     SELECT place,date,lowest,highest FROM Temperature
                     WHERE lowest > 0 AND highest > 0
                     GROUP BY place;
                    """
    test_tem_filter = pd.read_sql_query(sql_tem_filter,Sqlite_Conn)
    print(test_tem_filter)
    
    correlation_1 = Temperature['lowest'].corr(Temperature['highest'])
    print(correlation_1)
    print('----------------------------------------------------------------')
    
    # question(c)
    sql_AvgTemcorrLati = """
                          SELECT DISTINCT place,date, latitude, (lowest+highest)/2 AS AvgTem
                          FROM Temperature,Place
                          WHERE lowest > 0 AND highest > 0 AND Temperature.place = Place.name
                          GROUP BY(place);
                         """
    AvgTemcorrLati = pd.read_sql_query(sql_AvgTemcorrLati,Sqlite_Conn)
    print(AvgTemcorrLati['latitude'].corr(AvgTemcorrLati['AvgTem']))
    plt.plot(AvgTemcorrLati['latitude'],AvgTemcorrLati['AvgTem'])
    plt.xlabel("latitude")
    plt.ylabel("Average Temperature");
    
    plt.show()
    
    # question(d)
    rain_Helsi = """
                  SELECT place, COUNT(*) AS rainyday, strftime('%m',date) as month
                  FROM Observation
                  WHERE Observation.place = 'Helsinki-Vantaa Airport' AND rain > 0 AND rain IS NOT NULL
                  GROUP BY month
                 """
    rain_Mustasaari = """
                  SELECT place, COUNT(*) AS rainyday, strftime('%m',date) as month
                  FROM Observation
                  WHERE Observation.place = 'Mustasaari' AND rain > 0 AND rain IS NOT NULL
                  GROUP BY month
                """
    rain_Pötsönvaara = """
                  SELECT place, COUNT(*) AS rainyday, strftime('%m',date) as month
                  FROM Observation
                  WHERE Observation.place = 'Pötsönvaara' AND rain > 0 AND rain IS NOT NULL
                  GROUP BY month
                 """
    rain_Utsjoki = """
                  SELECT place, COUNT(*) AS rainyday, strftime('%m',date) as month
                  FROM Observation
                  WHERE Observation.place = 'Utsjoki' AND rain > 0 AND rain IS NOT NULL
                  GROUP BY month
                 """
    
    test_rain_Helsi = pd.read_sql_query(rain_Helsi, Sqlite_Conn)
    test_rain_Mustasaari = pd.read_sql_query(rain_Mustasaari, Sqlite_Conn)
    test_rain_Pötsönvaara = pd.read_sql_query(rain_Pötsönvaara, Sqlite_Conn)
    test_rain_Utsjoki = pd.read_sql_query(rain_Utsjoki, Sqlite_Conn)
    
#     labels = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
#     
#     x = np.arange(len(labels))
#     width = 0.35  # the width of the bars
#     
#     fig, ax = plt.subplots()
#     rects1 = ax.bar(x - width/4, np.array(list(test_rain_Helsi['rainyday'])), width, label='Helsinki')
#     rects2 = ax.bar(x - width/2, np.array(list(test_rain_Mustasaari['rainyday'])), width, label='Mustasaari')
#     rects3 = ax.bar(x + width/4, np.array(list(test_rain_Pötsönvaara['rainyday'])), width, label='Pötsönvaara')
#     rects4 = ax.bar(x + width/2, np.array(list(test_rain_Utsjoki['rainyday'])), width, label='Utsjoki')
#     
#     # Add some text for labels, title and custom x-axis tick labels, etc.
#     ax.set_ylabel('Rainy Days')
#     ax.set_title('Rainy Days in all cities')
#     ax.set_xticks(x)
#     ax.set_xticklabels(labels)
#     ax.legend()
# 
#     ax.bar_label(rects1, padding=3)
#     ax.bar_label(rects2, padding=3)
#     ax.bar_label(rects3, padding=3)
#     ax.bar_label(rects4, padding=3)
#     
#     fig.tight_layout()
# 
#     plt.show()
    
    plt.figure(1)
    ax1 = plt.subplot(221)
    plt.bar(test_rain_Helsi['month'], test_rain_Helsi['rainyday'], color = 'r', width=0.8, bottom=None, align='center', data=None)

    ax2 = plt.subplot(222)
    plt.bar(test_rain_Mustasaari['month'], test_rain_Mustasaari['rainyday'], color = 'y', width=0.8, bottom=None, align='center', data=None)
    
    ax3 = plt.subplot(223)
    plt.bar(test_rain_Pötsönvaara['month'], test_rain_Pötsönvaara['rainyday'], color = 'g', width=0.8, bottom=None, align='center', data=None)
    
    ax4 = plt.subplot(224)
    plt.bar(test_rain_Helsi['month'], test_rain_Utsjoki['rainyday'], color = 'b', width=0.8, bottom=None, align='center', data=None)
    
    plt.show()
    
    # question(e)
    AvgTem_Helsinki = """
                SELECT place, strftime('%m',date) as month, (lowest+highest)/2 AS AvgTem
                FROM Temperature
                WHERE lowest > 0 AND highest > 0 AND place = 'Helsinki-Vantaa Airport'
                GROUP BY month;
                """
    AvgTem_Mustasaari = """
                SELECT place, strftime('%m',date) as month, (lowest+highest)/2 AS AvgTem
                FROM Temperature
                WHERE lowest > 0 AND highest > 0 AND place = 'Mustasaari'
                GROUP BY month;
                """
    AvgTem_Pötsönvaara = """
                SELECT place, strftime('%m',date) as month, (lowest+highest)/2 AS AvgTem
                FROM Temperature
                WHERE lowest > 0 AND highest > 0 AND place = 'Pötsönvaara'
                GROUP BY month;
                """
    AvgTem_Utsjoki = """
                SELECT place, strftime('%m',date) as month, (lowest+highest)/2 AS AvgTem
                FROM Temperature
                WHERE lowest > 0 AND highest > 0 AND place = 'Utsjoki'
                GROUP BY month;
                """
    
    test_AvgTem_Helsinki = pd.read_sql_query(AvgTem_Helsinki, Sqlite_Conn)
    test_AvgTem_Mustasaari = pd.read_sql_query(AvgTem_Mustasaari, Sqlite_Conn)
    test_AvgTem_Mustasaari = pd.read_sql_query(AvgTem_Pötsönvaara, Sqlite_Conn)
    test_AvgTem_Utsjoki = pd.read_sql_query(AvgTem_Utsjoki, Sqlite_Conn)
    
    plt.figure(1)
    bx1 = plt.subplot(221)
    plt.plot(test_AvgTem_Helsinki['month'], test_AvgTem_Helsinki['AvgTem'], color = 'r')

    bx2 = plt.subplot(222)
    plt.plot(test_AvgTem_Mustasaari['month'], test_AvgTem_Mustasaari['AvgTem'], color = 'y')
    
    bx3 = plt.subplot(223)
    plt.plot(test_AvgTem_Mustasaari['month'], test_AvgTem_Mustasaari['AvgTem'], color = 'g')
    
    bx4 = plt.subplot(224)
    plt.plot(test_AvgTem_Utsjoki['month'], test_AvgTem_Utsjoki['AvgTem'], color = 'b')

    plt.show()
    
except Exception as e:
        print ("FAILED due to:" + str(e))
# END







