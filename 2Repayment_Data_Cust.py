
# coding: utf-8

# In[ ]:

#This file ensures only those customers are used whose repayment data is available
import pandas as pd
import numpy as np
import datetime
loan=pd.read_csv("Loan.csv",header=0,infer_datetime_format=True)
idlist=loan['customer_id'].tolist()
idlist.sort()
loanid=set(idlist)
assets=pd.read_csv("Assets.csv",header=0,infer_datetime_format=True)
newassets=pd.DataFrame()

for ida in loanid:
    newassets=newassets.append(assets[assets['customer_id']==ida])
newassets.to_csv("Assets.csv",index=False)

idlist=newassets['customer_id'].tolist()
idlist.sort()
idlist=set(idlist)

cust=pd.read_csv("Customer.csv",header=0,infer_datetime_format=True)
newcust=pd.DataFrame()

for ida in idlist:
    newcust=newcust.append(cust[cust['id']==ida])
newcust.to_csv("Customer.csv",index=False)

expend=pd.read_csv("Expenditure.csv",header=0,infer_datetime_format=True)
newexpend=pd.DataFrame()

for ida in idlist:
    newexpend=newexpend.append(expend[expend['customer_id']==ida])
newexpend.to_csv("Expenditure.csv",index=False)

family=pd.read_csv("Family.csv",header=0,infer_datetime_format=True)
newfamily=pd.DataFrame()

for ida in idlist:
    newfamily=newfamily.append(family[family['customer_id']==ida])
newfamily.to_csv("Family.csv",index=False)

inc=pd.read_csv("Income.csv",header=0,infer_datetime_format=True)
newinc=pd.DataFrame()

for ida in idlist:
    newinc=newinc.append(inc[inc['customer_id']==ida])
newinc.to_csv("Income.csv",index=False)


# In[ ]:

loan['disbursement_date']=pd.to_datetime(loan['disbursement_date'],format="%d-%m-%Y")
loan['schedule_date']=pd.to_datetime(loan['schedule_date'],format="%d-%m-%Y")
loan['repayment_date']=pd.to_datetime(loan['repayment_date'],format="%d-%m-%Y %H:%M")


i=0
loan['finalgap']=0
for i in loan.index:
        loan.loc[i,'finalgap']=(loan.loc[i,'repayment_date']-loan.loc[i,'schedule_date']).days


# In[ ]:


loan.to_csv("Loan.csv",index=False)


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



