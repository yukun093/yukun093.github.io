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


def main():
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

main()
Sqlite_Conn.close()
		
		

# # example code from assistant of Aalto course(CS-a1153) as follows:
# import sys
# import time,os,pandas as pd
# import matplotlib.pyplot as plt

# from sqlalchemy import create_engine,event,schema,Table,text
# from sqlalchemy.orm import sessionmaker


# def main():
	
    # DIALECT = 'sqlite:///'
    # DB_NAME = 'weather_db.db3'
    # DB_uri = DIALECT + DB_NAME
    # engine = create_engine(DB_uri)
	
    # global sqlite_conn
    # sqlite_conn  = engine.connect()
    # if not sqlite_conn:
        # print("DB connection is not OK!")
        # exit()
    # else:
        # print("DB connection is OK.")

    # ##################
    # # EXERCISE 1
    # ##################

    # engine.execute( 'CREATE TABLE IF NOT EXISTS "Place" ('
                    # 'code CHAR(6) PRIMARY KEY,'
                    # 'name VARCHAR(100),'
                    # 'latitude FLOAT,'
                    # 'longitude FLOAT);')


    # engine.execute( 'CREATE TABLE IF NOT EXISTS "Observation" ('
                    # 'place CHAR(6) REFERENCES Place(code),'
                    # 'date DATE,'
                    # 'rain FLOAT,'
                    # 'snow FLOAT,'
                    # 'air_temperature FLOAT,'
                    # 'ground_temperature FLOAT,'
                    # 'PRIMARY KEY(place, date));')

    # engine.execute( 'CREATE TABLE IF NOT EXISTS "Temperature" ('
                    # 'place CHAR(6) REFERENCES Place(code),'
                    # 'date DATE,'
                    # 'lowest FLOAT,'
                    # 'highest FLOAT,'
                    # 'PRIMARY KEY(place, date));')



    # try:
		
        # ##################
        # # EXERCISE 2
        # ##################
        
        # file_path = 'D:/Users/etnal/Aalto/Assist/DBAssist2021/Python/'
        # file_name = 'weather_data_2020.csv'
		
        # # Reading the file
        # df_weather = pd.read_csv(file_path+file_name,  sep=',',comment='#',dtype='unicode')
		
		
        # # Dates in format YYYY-MM-DD
        # df_weather['date'] = pd.to_datetime(df_weather[['year','month','day']],format='%Y%M%D').dt.date
		
        # # POPULATE PLACE
        # df_place = df_weather[['place_code', 'place', 'latitude', 'longitude']].drop_duplicates()
        # df_place.rename(columns={'place_code': 'code','place':'name'},inplace=True)

        # df_place.to_sql("Place", sqlite_conn, if_exists = 'replace')

        
        # # POPULATE OBSERVATION
        # df_obs = df_weather[['place_code', 'date', 'rain', 'snow', 'air_temperature', 'ground_temperature']].drop_duplicates()
        # df_obs.rename(columns={'place_code':'place'},inplace=True)

        # # Change types to float
        # df_obs['rain'] = df_obs['rain'].astype(float)
        # df_obs['snow'] = df_obs['snow'].astype(float)
        # df_obs['air_temperature'] = df_obs['air_temperature'].astype(float)
        # df_obs['ground_temperature'] = df_obs['ground_temperature'].astype(float)

        # # Change -1 to 0.0
        # df_obs.rain.replace(to_replace=[-1], value=[0], inplace=True)
        # df_obs.snow.replace(to_replace=[-1], value=[0], inplace=True)

        # df_obs.to_sql("Observation", sqlite_conn, if_exists = 'replace', index = False)
        
        # # POPULATE TEMPERATURE
        # df_temperature = df_weather[['place_code','date','lowest_temperature','highest_temperature']].drop_duplicates()
        # df_temperature.rename(columns={'place_code':'place','lowest_temperature':'lowest','highest_temperature':'highest'},inplace=True)

        # df_temperature['lowest'] = df_temperature['lowest'].astype(float)
        # df_temperature['highest'] = df_temperature['highest'].astype(float)


        # df_temperature.to_sql("Temperature", sqlite_conn, if_exists = 'replace')


        # ##############
        # # EXERCISE 3a)
        # ##############

        # print("\n\nEXERCISE 3b)\n")

        # query_snowy_days =  """
                            # SELECT code, name, COUNT(*) AS snowy_days 
                            # FROM Place JOIN Observation ON code = place 
                            # WHERE snow > 0.0 
                            # GROUP BY code;
                            # """
        # snowy_days= pd.read_sql_query(query_snowy_days, sqlite_conn)

        # # Inspection shows that Utsjoki (102035) is the place with most snow and least snow is Helsinki-Vantaa Airport (100968)
        # print("Number of snowy days:")
        # print(snowy_days)

        # query_most_snow = """
                    # SELECT strftime("%m", date) AS month, SUM(snow) AS total_snow 
                    # FROM Observation 
                    # WHERE place = "102035" 
                    # GROUP BY month 
                    # ORDER BY total_snow DESC;
                    # """
        
        # most_snow = pd.read_sql_query(query_most_snow, sqlite_conn)

        # # Inspection shows that the month with most snow is March (03)
        # print("Amount of snow per month in Utsjoki:")
        # print(most_snow)

        
        # query_least_snow =  """
                            # SELECT strftime("%m", date) AS month, COUNT(snow) AS snowy_days 
                            # FROM Observation 
                            # WHERE place = "100968" AND snow > 0.0 
                            # GROUP BY month 
                            # ORDER BY snowy_days DESC;
                            # """

        # least_snow = pd.read_sql_query(query_least_snow, sqlite_conn)
        
        # # Most snowy days on April(04)
        # print("Number of snowy days per month in Helsinki-Vantaa Airport:")
        # print(least_snow)


        # ##############
        # # EXERCISE 3b)
        # ##############

        # print("\n\nEXERCISE 3b)\n")

        # query_temp_notnull = """
                             # SELECT date, place, highest, lowest FROM Temperature WHERE highest IS NOT NULL AND lowest IS NOT NULL;
                             # """

        # temperatures = pd.read_sql_query(query_temp_notnull,sqlite_conn)

        # # Correlation between lowest and highest
        # temp_corr = temperatures['lowest'].corr(temperatures['highest'])
        # print("Correlation between lowest and highest by row: ", round(temp_corr,3)) # High positive correlation

        # # Correlate using group by and restructure the dataframe a bit
        # temp_corr2 = temperatures.groupby(['place']).corr().reset_index()
        # temp_corr2 = temp_corr2[temp_corr2['level_1'] == 'highest'][['place','lowest']].rename(columns={'lowest':'corr'})

        # print("Correlation between lowest and highest grouped by place: ")
        # print(temp_corr2) # Again very high positive correlation


        # ##############
        # # EXERCISE 3c)
        # ##############

        # print("\n\nEXERCISE 3c)\n")

        # #We decided to use air_temperature here
        # query_temp_obs =  """
                    # SELECT air_temperature, place, name, latitude 
                    # FROM Observation JOIN Place ON place = code
                    # WHERE air_temperature IS NOT NULL;
                    # """

        # temp_obs = pd.read_sql_query(query_temp_obs, sqlite_conn)
        
        # temp_lat_corr = temp_obs['air_temperature'].corr(temp_obs['latitude'].astype(float))
        # print("Correlation between air temp and latitude by row: ", temp_lat_corr) # slight negative correlation


        # query_temp_obs2 =   """
                            # SELECT AVG(air_temperature) AS air_temperature, place, name, latitude 
                            # FROM Observation JOIN Place ON place = code
                            # GROUP BY place;
                            # """
        # temp_obs2 = pd.read_sql_query(query_temp_obs2, sqlite_conn)
        # temp_lat_corr2 = temp_obs2['air_temperature'].corr(temp_obs2['latitude'].astype(float))
        
        # print("Correlation when grouped by place and taking avg: ", temp_lat_corr2) # high negative correlation

        # ##############
        # # EXERCISE 3d)
        # ##############
        
        # print("\n\nEXERCISE 3d)\n")
		
        # query_rainy_days = """
                            # SELECT strftime("%m", date) AS month, COUNT(rain) AS rain, code
                            # FROM Place LEFT JOIN (SELECT * FROM Observation
                            # WHERE rain > 0.0) ON place = code
                            # GROUP BY month,code;
                            # """

        # rainy_days = pd.read_sql_query(query_rainy_days, sqlite_conn)
        # # Pivot using month as index to include months with no rainy days
        # rainy_days = rainy_days.pivot(index = "month", columns = "code", values = "rain").fillna(0)

        # fig, axes = plt.subplots(nrows=2, ncols=2)

        # rainy_days['100968'].plot.bar(ax = axes[0,0], x = 'month', y = 'rain', title = 'Helsinki-Vantaa Airport')
        # rainy_days['101464'].plot.bar(ax = axes[0,1], x = 'month', y = 'rain', title = 'Mustasaari')
        # rainy_days['101649'].plot.bar(ax = axes[1,0], x = 'month', y = 'rain', title = 'Pöntsönvaara')
        # rainy_days['102035'].plot.bar(ax = axes[1,1], x = 'month', y = 'rain', title = 'Utsjoki')

        # plt.show()


        # ##############
        # # EXERCISE 3e)
        # ##############


        # #We will use the air temperature here.

        # query_temp_plot_df =    """
                                # SELECT air_temperature, place, date
                                # FROM Observation
                                # WHERE air_temperature IS NOT NULL;
                                # """

        # temp_plot_df = pd.read_sql_query(query_temp_plot_df, sqlite_conn)
        # temp_plot_df = temp_plot_df.pivot(index = "date", columns = "place", values = "air_temperature")
        # temp_plot_df.plot()

        # plt.show()

    # except Exception as e:
        # print ("FAILED due to:" + str(e))  


# main()
# sqlite_conn.close()




