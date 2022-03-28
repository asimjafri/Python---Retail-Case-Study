#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[4]:


cust = pd.read_csv("Customer.csv")
cust


# In[5]:


prod = pd.read_csv("prod_cat_info.csv")
prod


# In[6]:


trans = pd.read_csv("Transactions.csv")
trans


# In[7]:


# 1.Merge the datasets Customers, Product Hierarchy and Transactions as Customer_Final. Ensure to keep all customers who have done transactions with us and select the join type accordingly.
merge = trans.merge(prod, left_on=['prod_cat_code', 'prod_subcat_code'], right_on=['prod_cat_code', 'prod_sub_cat_code'], how ='left')
merge


# In[8]:


merge.rename(columns={'cust_id':'customer_Id'}, inplace=True)
customer_final = merge.merge(cust, on='customer_Id', how='left')
customer_final


# In[9]:


# 2.Prepare a summary report for the merged data set.
# a. Get the column names and their corresponding data types
customer_final.dtypes


# In[10]:


# b. Top 10 observations
customer_final.head(10)


# In[11]:


# b. Bottom 10 observations
customer_final.tail(10)


# In[12]:


# c. “Five-number summary” for continuous variables (min, Q1, median, Q3 and max)
customer_final.describe()


# In[13]:


# d. Frequency tables for all the categorical variables
customer_final.loc[:,customer_final.dtypes=="object"].describe()


# In[14]:


# 3. Generate histograms for all continuous variables and frequency bars for categorical variables.
flt = customer_final.loc[:, (customer_final.dtypes=='int64') | (customer_final.dtypes=='float64')]
flt.columns


# In[15]:


continuous = customer_final.loc[:,['prod_subcat_code','prod_cat_code', 'Qty', 'Rate', 'Tax', 'total_amt']]
continuous.columns


# In[16]:


for col in continuous.columns:
    continuous[col].plot(kind='hist')
    plt.title(col)
    plt.show()


# In[17]:


categorical = customer_final.loc[:, (customer_final.dtypes=='object')]
categorical.columns


# In[18]:


categorical.Store_type.value_counts().plot.bar()


# In[19]:


categorical.Gender.value_counts().plot.bar()


# In[20]:


categorical.prod_cat.value_counts().plot.bar()


# In[21]:


categorical.prod_subcat.value_counts().plot.bar()


# In[22]:


# 4. Calculate the following information using the merged dataset :
# a. Time period of the available transaction data
customer_final.sort_values(by="tran_date")
print("The time period of transaction data is from "+customer_final["tran_date"].min()+" to "+customer_final["tran_date"].max())


# In[23]:


# b. Count of transactions where the total amount of transaction was negative
len(customer_final[customer_final.total_amt<0].total_amt)


# In[24]:


# 5. Analyze which product categories are more popular among females vs male customers.
customer_final.groupby(['prod_cat', 'Gender'])['transaction_id'].count().reset_index()


# In[25]:


# 6. Which City code has the maximum customers and what was the percentage of customers from that city?
code = customer_final.groupby('city_code')['customer_Id'].count().sort_values(ascending=False).reset_index()
code['percentage'] = (code['customer_Id'] / code['customer_Id'].sum()) * 100
code.head(1)


# In[26]:


# 7. Which store type sells the maximum products by value and by quantity?
store = customer_final.groupby("Store_type")["Qty","Rate"].sum().sort_values(by="Qty",ascending=False).reset_index()
store.head(1)


# In[27]:


# 8. What was the total amount earned from the "Electronics" and "Clothing" categories from Flagship Stores?
x = customer_final.groupby(['Store_type', 'prod_cat'])['total_amt'].sum().reset_index()
y = x[(x.Store_type == 'Flagship store')&((x.prod_cat == 'Electronics')|(x.prod_cat == 'Clothing'))]
y.reset_index()


# In[28]:


# 9. What was the total amount earned from "Male" customers under the "Electronics" category?
z = customer_final.groupby(['Gender','prod_cat'])['total_amt'].sum().reset_index()
amt = z[(z.Gender == 'M') & (z.prod_cat == 'Electronics')]
amt.reset_index()


# In[29]:


# 10. How many customers have more than 10 unique transactions, after removing all transactions which have any negative amounts?
p = customer_final[customer_final.total_amt>0].groupby('customer_Id')['transaction_id'].count().reset_index()
unique = p[p.transaction_id>10]
unique.customer_Id.count()


# In[31]:


# 11. For all customers aged between 25 - 35, find out:
# a. What was the total amount spent for “Electronics” and “Books” product categories?
import datetime
customer_final['Age'] = (datetime.datetime.now().year - pd.DatetimeIndex(customer_final['DOB']).year)
customer_final[((customer_final.prod_cat == 'Electronics')|(customer_final.prod_cat == 'Books')) & ((customer_final.Age >= 25) & (customer_final.Age <=35))].groupby('prod_cat')['total_amt'].sum().reset_index()


# In[38]:


#  b. What was the total amount spent by these customers between 1st Jan, 2014 to 1st Mar, 2014?
customer_final[((pd.to_datetime(customer_final.tran_date) >= '2014-01-01')&(pd.to_datetime(customer_final.tran_date) <= '2014-03-01')) & ((customer_final.Age >= 25) & (customer_final.Age <=35))].total_amt.sum()

