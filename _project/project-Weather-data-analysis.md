---
title: "SQL-for-weather-data-analysis"
excerpt: "Using pandas and sqlalchemy to analyse the weather data from Finnish Meteorological Institute<br/><img src='/images/Finnish-Meteorological-Institute-open-data.png'>"
permalink: /project/project-Weather-data-analysis/
Finnish-Meteorological-Institute-link: 'https://en.ilmatieteenlaitos.fi/open-data'
filelink: 'https://drive.google.com/file/d/14iq1ielpMPG-QXGdmt9NBdnWBmQ8HTI5/view?usp=sharing'
collection: project
---

------

It is one project that uses pandas to read data from [csv file](https://drive.google.com/file/d/14iq1ielpMPG-QXGdmt9NBdnWBmQ8HTI5/view?usp=sharing), and sqlalchemy to create database and address the data, which is picked from Finnish Meteorological Institute, and the cover page is also downloaded from the [institute's page](https://en.ilmatieteenlaitos.fi/open-data) as well. If you wish to download more data, it could also download data from this page, since they already has made its data sets freely available for public use. First, one database engine should be created, for example as sqlite_conn. Then using `engine.connect()` to prompt the script to connect with the database.

## Field Creation

Using engine.execute() to create several tables if there are not tables that are mentioned beforehand, For Example the table "Place".

```sql
engine.execute( 'CREATE TABLE IF NOT EXISTS "Place" ('
                'code CHAR(6) PRIMARY KEY,'
                'name VARCHAR(100),'
                'latitude FLOAT,'
                'longitude FLOAT);')
```

## Data Cleaning

Using pandas to read the ".csv" file, then pick up the needed area to set the specific format with pd.to_datatime, such as "YYYY-MM-DD". If it is necessary, some fields should be replaced as well. Then, the selected field mentioned above should be written into the generated table "Place". Familiar with deal with field below 'Place', fields of 'Observation' and 'Temperature' should be handled as well. Here, the most important part is to adjust field name according to individual requirements.

## SQL Operation

If sqlqueries need to combine with database engine, first the query should be created. Then, using pd.read_sql_query to connect query with engine to pick up the data needed, for example, as follows:

```sql
query_snowy_days =  """
                    SELECT code, name, COUNT(*) AS snowy_days 
                    FROM Place JOIN Observation ON code = place 
                    WHERE snow > 0.0 
                    GROUP BY code;
                    """
snowy_days= pd.read_sql_query(query_snowy_days, sqlite_conn)
```

Basically, with the help of `.fillna()`, the null value could be replaced by 0.0. It is better to express data with figures with the help of `rainy_days['100968'].plot.bar(ax = axes[0,0], x = 'month', y = 'rain', title = 'Helsinki-Vantaa Airport')`.

Finally, after reading sqlquery, using .close() to close the engine.

