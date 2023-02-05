#!/usr/bin/env python
# coding: utf-8

# In[2]:


#import the necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[3]:


#import the csv files which are exported from https://www.gunviolencearchive.org/reports
mass_shootings = pd.read_csv("Gun_violence_mass_shootings.csv")
accidental_deaths = pd.read_csv("Gun_violence_accidental_deaths.csv")
officer_involved_shootings = pd.read_csv("Gun_violence_officers_involved.csv")


# In[13]:


#convert into dataframes and cheack contents 
df_ms = pd.DataFrame(data = mass_shootings)
df_ms.head()


# In[6]:


df_ad = pd.DataFrame(data = accidental_deaths)
df_ad.head()


# In[7]:


df_o = pd.DataFrame(data = officer_involved_shootings)
df_o.head()


# In[14]:


# dropping address and Operations columns
df_ms.drop(['Operations','Address'],axis = 1,inplace = True)
df_ms.head()


# In[15]:


df_ad.drop(['Operations','Address'],axis = 1,inplace = True)
df_ad.head()


# In[16]:


df_o.drop(['Operations','Address'],axis = 1,inplace = True)
df_o.head()


# In[17]:


df_ms = df_ms.rename(columns={"Incident ID":"Incident_ID", "Incident Date":"Incident_Date", "State":"State", "City Or County":"CityorCounty", "# Killed":"Num_Killed", "# Injured":"Num_Injured"})
df_ms.head()


# In[18]:


df_ad = df_ad.rename(columns={"Incident ID":"Incident_ID", "Incident Date":"Incident_Date", "State":"State", "City Or County":"CityorCounty", "# Killed":"Num_Killed", "# Injured":"Num_Injured"})
df_ad.head()


# In[19]:


df_o = df_o.rename(columns={"Incident ID":"Incident_ID", "Incident Date":"Incident_Date", "State":"State", "City Or County":"CityorCounty", "# Killed":"Num_Killed", "# Injured":"Num_Injured"})
df_o.head()


# In[20]:


from sqlalchemy import create_engine

import pymysql


# In[21]:



tableName = 'mass_shootings'
sqlEngine       = create_engine('mysql+pymysql://root:SQL_1294#@localhost:3306/msds_530_db', pool_recycle=3600)

dbConnection    = sqlEngine.connect()

 

try:

    frame           = df_ms.to_sql(tableName, dbConnection, if_exists='fail');

except ValueError as vx:

    print(vx)

except Exception as ex:   

    print(ex)

else:

    print("Table %s created successfully."%tableName);   

finally:

    dbConnection.close()


# In[23]:


tableName = 'accidental_deaths_updated'
sqlEngine       = create_engine('mysql+pymysql://root:SQL_1294#@localhost:3306/msds_530_db', pool_recycle=3600)

dbConnection    = sqlEngine.connect()

 

try:

    frame           = df_ad.to_sql(tableName, dbConnection, if_exists='append');

except ValueError as vx:

    print(vx)

except Exception as ex:   

    print(ex)

else:

    print("Table %s created successfully."%tableName);   

finally:

    dbConnection.close()


# In[24]:


tableName = 'officer_involved_shootings'
sqlEngine       = create_engine('mysql+pymysql://root:SQL_1294#@localhost:3306/msds_530_db', pool_recycle=3600)

dbConnection    = sqlEngine.connect()

 

try:

    frame           = df_o.to_sql(tableName, dbConnection, if_exists='append');

except ValueError as vx:

    print(vx)

except Exception as ex:   

    print(ex)

else:

    print("Table %s created successfully."%tableName);   

finally:

    dbConnection.close()


# In[27]:


#check the proper creation of the table in SQL by querying  
sqlEngine       = create_engine('mysql+pymysql://root:SQL_1294#@localhost:3306/msds_530_db', pool_recycle=3600)

dbConnection    = sqlEngine.connect()
check=pd.read_sql_query('select * from accidental_deaths_updated', con=dbConnection)
dbConnection.close()


# In[28]:


check.head()


# In[31]:


#check for duplicates considering Incident_ID as primary key
duplicates = pd.merge(df_ms,df_ad, on="Incident_ID")
len(duplicates['Incident_ID'])


# In[32]:


duplicates = pd.merge(df_ms,df_o, on="Incident_ID")
len(duplicates['Incident_ID'])


# In[33]:


duplicates = pd.merge(df_o,df_ad, on="Incident_ID")
len(duplicates['Incident_ID'])


# In[34]:


count_states = df_ms.drop(["Incident_ID","Num_Injured", "CityorCounty", "Incident_Date"], axis=1)
ms_count=count_states.groupby(['State']).sum().sort_values(['Num_Killed'],ascending = False)
ms_count


# In[35]:


ms_count.head()


# In[36]:


count_states_ad = df_ad.drop(["Incident_ID","Num_Injured", "CityorCounty", "Incident_Date"], axis=1)
ad_count=count_states_ad.groupby(['State']).sum().sort_values(['Num_Killed'],ascending = False)
ad_count.head()


# In[38]:


count_states_o = df_o.drop(["Incident_ID","Num_Injured", "CityorCounty", "Incident_Date"], axis=1)
o_count=count_states_o.groupby(['State']).sum().sort_values(['Num_Killed'],ascending = False)
o_count.head()


# In[39]:


#extract year from the date
df_ad['year'] = pd.DatetimeIndex(df_ad['Incident_Date']).year
df_ad.head()


# In[40]:


df_ad['month'] = pd.DatetimeIndex(df_ad['Incident_Date']).month
df_ad.head()


# In[66]:


df_test = df_ad.drop(["Incident_ID","Num_Injured", "CityorCounty", "Incident_Date","month","State"],axis = 1)
df_test.head()


# In[67]:


df_temp=df_test.groupby(['year']).sum().sort_values(['Num_Killed'],ascending = False)
df_temp.head()


# In[71]:


df_temp['year'] = df_temp.index


# In[72]:


sns.barplot(x = 'year',
            y = 'Num_Killed',
            data = df_temp)
 
# Show the plot
plt.show()


# In[77]:


ms_count['state']=ms_count.index
#ms_count=ms_count.drop(['state'],axis=1)
ms_count.reset_index(drop = True,inplace = True)
ms_count.head()


# In[79]:


tableName = 'mass_shootings_by_state'
sqlEngine       = create_engine('mysql+pymysql://root:SQL_1294#@localhost:3306/msds_530_db', pool_recycle=3600)

dbConnection    = sqlEngine.connect()

try:

    frame           = ms_count.to_sql(tableName, dbConnection, if_exists='append');

except ValueError as vx:

    print(vx)

except Exception as ex:   

    print(ex)

else:

    print("Table %s created successfully."%tableName);   

finally:

    dbConnection.close()


# In[81]:


ad_count['state']=ad_count.index
ad_count.reset_index(drop = True,inplace = True)
ad_count.head()


# In[82]:


tableName = 'accidental_deaths_by_state'
sqlEngine       = create_engine('mysql+pymysql://root:SQL_1294#@localhost:3306/msds_530_db', pool_recycle=3600)

dbConnection    = sqlEngine.connect()

try:

    frame           = ad_count.to_sql(tableName, dbConnection, if_exists='append');

except ValueError as vx:

    print(vx)

except Exception as ex:   

    print(ex)

else:

    print("Table %s created successfully."%tableName);   

finally:

    dbConnection.close()


# In[83]:


o_count['state']=o_count.index
o_count.reset_index(drop = True,inplace = True)
o_count.head()


# In[84]:


tableName = 'officer_involved_deaths_by_state'
sqlEngine       = create_engine('mysql+pymysql://root:SQL_1294#@localhost:3306/msds_530_db', pool_recycle=3600)

dbConnection    = sqlEngine.connect()

try:

    frame           = o_count.to_sql(tableName, dbConnection, if_exists='append');

except ValueError as vx:

    print(vx)

except Exception as ex:   

    print(ex)

else:

    print("Table %s created successfully."%tableName);   

finally:

    dbConnection.close()


# In[94]:


df_test_1 = df_ad.drop(["Incident_ID","Num_Injured", "CityorCounty", "Incident_Date","State"],axis = 1)
df_test_1.head()
df_temp_1=df_test_1.groupby(['year','month']).sum().sort_values(['Num_Killed'],ascending = False)
df_temp_1.head()


# In[87]:


df_ad.head()


# In[96]:


type(df_temp_1.index)


# In[98]:


#parsing year and month and adding in DataFrames
df_ms['year'] = pd.DatetimeIndex(df_ms['Incident_Date']).year
df_ms['month'] = pd.DatetimeIndex(df_ms['Incident_Date']).month
df_ms.head()


# In[99]:


#parsing year and month and adding in DataFrames
df_o['year'] = pd.DatetimeIndex(df_o['Incident_Date']).year
df_o['month'] = pd.DatetimeIndex(df_o['Incident_Date']).month
df_o.head()


# In[102]:


#create tables with year and month sparced
tableName = 'accidental_deaths_timed'
sqlEngine       = create_engine('mysql+pymysql://root:SQL_1294#@localhost:3306/msds_530_db', pool_recycle=3600)

dbConnection    = sqlEngine.connect()

try:

    frame           = df_ad.to_sql(tableName, dbConnection, if_exists='append');

except ValueError as vx:

    print(vx)

except Exception as ex:   

    print(ex)

else:

    print("Table %s created successfully."%tableName);   

finally:

    dbConnection.close()


# In[101]:


#create tables with year and month sparced
tableName = 'mass_shooting_timed'
sqlEngine       = create_engine('mysql+pymysql://root:SQL_1294#@localhost:3306/msds_530_db', pool_recycle=3600)

dbConnection    = sqlEngine.connect()

try:

    frame           = df_ms.to_sql(tableName, dbConnection, if_exists='append');

except ValueError as vx:

    print(vx)

except Exception as ex:   

    print(ex)

else:

    print("Table %s created successfully."%tableName);   

finally:

    dbConnection.close()


# In[103]:


#create tables with year and month sparced
tableName = 'officer_involved_shooting_timed'
sqlEngine       = create_engine('mysql+pymysql://root:SQL_1294#@localhost:3306/msds_530_db', pool_recycle=3600)

dbConnection    = sqlEngine.connect()

try:

    frame           = df_o.to_sql(tableName, dbConnection, if_exists='append');

except ValueError as vx:

    print(vx)

except Exception as ex:   

    print(ex)

else:

    print("Table %s created successfully."%tableName);   

finally:

    dbConnection.close()


# In[105]:


#check table names finally
sqlEngine       = create_engine('mysql+pymysql://root:SQL_1294#@localhost:3306/msds_530_db', pool_recycle=3600)

dbConnection    = sqlEngine.connect()

print(sqlEngine.table_names())

dbConnection.close()


# In[ ]:




