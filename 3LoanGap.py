
# coding: utf-8

# In[ ]:

#This file has the decision criterion on what is 'late'
import pandas as pd
import numpy as np
import datetime
loan=pd.read_csv("NewLoan.csv",header=0,infer_datetime_format=True)


# In[ ]:




# In[ ]:

cust=pd.read_csv("Master.csv",header=0,infer_datetime_format=True)
idlist=cust['id']
for i in cust.index:
    if cust.loc[i,'tenure']=='1 Year' or cust.loc[i,'tenure']=='12 Months':
        cust.loc[i,'tenured']=12
    elif cust.loc[i,'tenure']=='2 Years' or cust.loc[i,'tenure']=='24 Months':
        cust.loc[i,'tenured']=24
    elif cust.loc[i,'tenure']=='50 Weeks':
        cust.loc[i,'tenured']=50
    else:
        cust.loc[i,'tenured']=62

cust=cust.drop('tenure',1)



# In[ ]:


for i in loan.index:
    if loan.loc[i,'tenure']=='1 Year' or loan.loc[i,'tenure']=='12 Months':
        loan.loc[i,'tenured']=12
    elif loan.loc[i,'tenure']=='2 Years' or loan.loc[i,'tenure']=='24 Months':
        loan.loc[i,'tenured']=24
    elif loan.loc[i,'tenure']=='50 Weeks':
        loan.loc[i,'tenured']=50
    else:
        loan.loc[i,'tenured']=62

loan=loan.drop('tenure',1)


# In[ ]:

count=0
latelist=list()
invalid=list()
for ids in idlist:
    temp=loan[loan['customer_id']==ids]
    j=loan[loan['customer_id']==ids].index[0]
    if len(temp)<5:
        invalid.append(ids)
    p=temp[temp['finalgap']>0]
    if temp.loc[j,'tenured']<20:
        if len(p)>1:
            latelist.append(ids)
    else:
        if len(p)>2:
            latelist.append(ids)
   
    


# In[28]:

for i in latelist:
    
    try:
        j=cust[cust['id']==i].index[0]
        cust.loc[j,'late']=1
    except:
        print('flag')

        
for i in cust.index:
    if cust.loc[i,'late']!=1:
        cust.loc[i,'late']=0
        


# In[29]:

loan.to_csv('NewLoan.csv',index=False)


# In[30]:

cust.to_csv('Master.csv',index=False)


# In[ ]:

len(latelist)/len(cust)*100


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# 

# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



