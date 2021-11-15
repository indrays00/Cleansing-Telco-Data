#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
df_load = pd.read_csv('https://storage.googleapis.com/dqlab-dataset/dqlab_telco.csv')


# In[4]:


# validation customerID
# valid customerID start with 45 and have long 11-12 char
df_load['valid_id'] = df_load['customerID'].astype(str).str.match(r'(45\d{9,10})')
df_load = (df_load[df_load['valid_id'] == True]).drop('valid_id', axis = 1)
print('Hasil jumlah ID Customer yang terfilter adalah', df_load['customerID'].count())


# In[5]:


#drop duplicate customerID
df_load = df_load.sort_values('UpdatedAt', ascending=False).drop_duplicates(['customerID'])
print("total rows after delete duplicates customerID", df_load.shape[0])


# In[6]:


#find missing value in data frame per columns
print(df_load.isna().sum())


# In[8]:


#drop a rows where churn column is null
df_load.dropna(subset=['Churn'], inplace=True)
print(df_load.isna().sum())


# In[14]:


# as a request fill tenure nan value with 11 and fill other missih with median
df_load['tenure'].fillna(11, inplace=True)
for nama_kolom in list(['MonthlyCharges', 'TotalCharges']):
    median = df_load[nama_kolom].median()
    df_load[nama_kolom].fillna(median, inplace=True)
    
print("missing value after fillna")
print(df_load.isna().sum())
df_load.dtypes


# In[18]:


#detect outlier with boxplot
import matplotlib.pyplot as plt
import seaborn as sns

for nama_kolom in list(['tenure', 'MonthlyCharges', 'TotalCharges']):
    plt.figure()
    sns.boxplot(x=df_load['tenure'])
    sns.boxplot(x=df_load['tenure'])
    judul = 'Boxplot column'+nama_kolom
    plt.title(judul)
    plt.savefig("%s.png" % judul)
plt.show()

print('\nPersebaran data sebelum ditangani Outlier: ')
print(df_load[['tenure','MonthlyCharges','TotalCharges']].describe())


# In[19]:


# find IQR
Q1 = (df_load[['tenure','MonthlyCharges','TotalCharges']]).quantile(0.25)
Q3 = (df_load[['tenure','MonthlyCharges','TotalCharges']]).quantile(0.75)

IQR = Q3 - Q1


# In[20]:


# get a minimum and max from tenure,MonthlyCharges,TotalCharges
maximum = Q3 + (1.5*IQR)
print('Nilai Maximum dari masing-masing Variable adalah: ')
print(maximum)
minimum = Q1 - (1.5*IQR)
print('\nNilai Minimum dari masing-masing Variable adalah: ')
print(minimum)


# In[21]:


#fill the outlier with maximum or minimum
more_than = (df_load > maximum)
lower_than = (df_load < minimum)

#masking
df_load = df_load.mask(more_than, maximum, axis=1)
df_load = df_load.mask(lower_than, minimum, axis=1)

print('\nPersebaran data setelah ditangani Outlier: ')
print(df_load[['tenure','MonthlyCharges','TotalCharges']].describe())


# In[24]:


#cheking unique value 
for col_name in list(['gender','SeniorCitizen','Partner','Dependents','PhoneService','MultipleLines','InternetService','OnlineSecurity','OnlineBackup','DeviceProtection','TechSupport','StreamingTV','StreamingMovies','Contract','PaperlessBilling','PaymentMethod','Churn']):
  print('\nUnique Values Count \033[1m' + 'Before Standardized \033[0mVariable',col_name)
  print(df_load[col_name].value_counts())


# In[26]:


# variable Standardized 
df_load = df_load.replace(['Wanita','Laki-Laki','Churn','Iya'],['Female','Male','Yes','Yes'])


# In[27]:


for col_name in list(['gender','SeniorCitizen','Partner','Dependents','PhoneService','MultipleLines','InternetService','OnlineSecurity','OnlineBackup','DeviceProtection','TechSupport','StreamingTV','StreamingMovies','Contract','PaperlessBilling','PaymentMethod','Churn']):
  print('\nUnique Values Count \033[1m' + 'After Standardized \033[0mVariable',col_name)
  print(df_load[col_name].value_counts())


# In[ ]:


# to csv
df_load.to_csv('dqlab_telco[cleared].csv', index=False)

