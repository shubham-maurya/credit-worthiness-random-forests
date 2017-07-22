
# coding: utf-8

# In[1]:

#Creating a Master Table with various features
import pandas as pd
import numpy as np
cust=pd.read_csv("customer.csv",header=0,infer_datetime_format=True)
family=pd.read_csv("family.csv",header=0,infer_datetime_format=True)
loan=pd.read_csv("Loan.csv",header=0,infer_datetime_format=True)
expend=pd.read_csv("expenditure.csv",header=0,infer_datetime_format=True)
inc=pd.read_csv("income.csv",header=0,infer_datetime_format=True)
assets=pd.read_csv("assets.csv",header=0,infer_datetime_format=True)


# In[2]:

family['edu_code']=-1
i=0
for i in family.index:
    if family.loc[i,'education_status']=='1st - 5th':
        family.loc[i,'edu_code']=1
    elif family.loc[i,'education_status']=='Cannot read/write':
        family.loc[i,'edu_code']=0
    elif family.loc[i,'education_status']=='6th - 8th':
        family.loc[i,'edu_code']=1
    elif family.loc[i,'education_status']=='9th- 10th':
        family.loc[i,'edu_code']=1
    elif family.loc[i,'education_status']=='11th - 12th':
        family.loc[i,'edu_code']=2
    elif family.loc[i,'education_status']=='Graduate':
        family.loc[i,'edu_code']=2
    elif family.loc[i,'education_status']=='Post Graduate':
        family.loc[i,'edu_code']=2
    else:
        family.loc[i,'edu_code']=0
    


# In[4]:

i=0

agro=['Agriculture','Dairy','Goat rearing']
labour=['Labour','Migrant Labour']
fixed=['Driver','House-wife','Salaried - Govt','Salaried - Others','Working Abroad']
entre=['Shop Owner','Business - Others','Small Industry','Performing Arts']

for i in cust.index:
    if cust.loc[i,'occupation1'] in agro:
        cust.loc[i,'occ']=1
       
    elif cust.loc[i,'occupation1'] in labour:
        cust.loc[i,'occ']=2
       
    elif cust.loc[i,'occupation1'] in fixed:
        cust.loc[i,'occ']=3
    
    elif cust.loc[i,'occupation1'] in entre:
        cust.loc[i,'occ']=4
       

            


# In[5]:

cust['self_edu']=-1
i=0
edudict={}
for i in family.index:
    if family.loc[i,'relationship']=='Self':
        edudict[family.loc[i,'customer_id']]=family.loc[i,'edu_code']
        
i=0
for i in cust.index:
    if cust.loc[i,'id'] in edudict:
        cust.loc[i,'self_edu']=edudict[cust.loc[i,'id']]


# In[6]:

jeweldict={}
for i in assets.index:
    if assets.loc[i,'name_of_owned_asset'] == 'Jewellery':
        jeweldict[assets.loc[i,'customer_id']]=assets.loc[i,'number_of_owned_asset']

for i in cust.index:
    j=cust.loc[i,'id']
    if j in jeweldict.keys():
        cust.loc[i,'jewel']=jeweldict[j]
    else:
        cust.loc[i,'jewel']=0


# In[7]:

landdict={}
for i in assets.index:
    if assets.loc[i,'name_of_owned_asset'] == 'Land area':
        landdict[assets.loc[i,'customer_id']]=assets.loc[i,'number_of_owned_asset']

for i in cust.index:
    j=cust.loc[i,'id']
    if j in landdict.keys():
        cust.loc[i,'land']=landdict[j]
    else:
        cust.loc[i,'land']=0


# In[8]:

family['date_of_birth']=pd.to_datetime(family['date_of_birth'])
i=0
agedict={}
for i in family.index:
    if family.loc[i,'relationship']=='Self':
        agedict[family.loc[i,'customer_id']]=2016-family.loc[i,'date_of_birth'].year
        
i=0

for i in cust.index:
    if cust.loc[i,'id'] in agedict:
        cust.loc[i,'age']=agedict[cust.loc[i,'id']]


# In[10]:

amtdict={}
idlist=cust['id']
for i in idlist:
    temp=loan[loan['customer_id']==i]
    j=loan[loan['customer_id']==i].index[0]
    amtdict[i]=temp.loc[j,'loan_amount']
    
for i in cust.index:
    if cust.loc[i,'id'] in amtdict:
        cust.loc[i,'loan_amt']=amtdict[cust.loc[i,'id']]


# In[11]:

i=0

famsize={}
for i in idlist:
    temp=family[family['customer_id']==i]
    famsize[i]=len(temp)


for i in cust.index:
    if cust.loc[i,'id'] in famsize:
         cust.loc[i,'fam_size']= famsize[cust.loc[i,'id']]
       
                    
            


# In[15]:

i=0
idlist=cust['id']
fedudict={}
for i in idlist:
    temp=family[family['customer_id']==i]
    a=temp.edu_code
    try:
        fedudict[i]=max(a)
    except:
        fedudict[i]=2
    
for i in fedudict:
    j=cust[cust['id']==i].index[0]
    cust.loc[j,'family_edu']=fedudict[i]
    
        


# In[16]:


explist=list()
for i in expend.index:
    if expend.loc[i,'frequency']=='Annually':
        explist.append(expend.loc[i,'annual_expenses'])
    elif expend.loc[i,'frequency']=='Half yearly':
        explist.append(2*(expend.loc[i,'annual_expenses']))
    elif expend.loc[i,'frequency']=='Monthly':
        explist.append(12*expend.loc[i,'annual_expenses'])
    elif expend.loc[i,'frequency']=='Fortnightly':
        explist.append(24*expend.loc[i,'annual_expenses'])
    elif expend.loc[i,'frequency']=='Quarterly':
        explist.append(4*expend.loc[i,'annual_expenses'])
    elif expend.loc[i,'frequency']=='Weekly':
        explist.append(52*expend.loc[i,'annual_expenses'])
    elif expend.loc[i,'frequency']=='Daily':
        explist.append(350*expend.loc[i,'annual_expenses'])
    else:
        explist.append(0)
    
expend['total']=explist
idlist=list(set(expend['customer_id']))
expdict={}
for i in idlist:
    temp=expend[expend['customer_id']==i]
    j=expend[expend['customer_id']==i].index[0]
    expdict[i]=sum(temp['total'])
    
for i in cust.index:
    if cust.loc[i,'id'] in expdict:
        cust.loc[i,'expenses']=expdict[cust.loc[i,'id']]


# In[17]:

inclist=list()
for i in inc.index:
    if expend.loc[i,'frequency']=='Annually':
        inclist.append(inc.loc[i,'income_earned'])
    elif expend.loc[i,'frequency']=='Half yearly':
        inclist.append(inc.loc[i,'income_earned']*inc.loc[i,'months_per_year']/6)
    elif expend.loc[i,'frequency']=='Monthly':
        inclist.append(inc.loc[i,'months_per_year']*inc.loc[i,'income_earned'])
    elif expend.loc[i,'frequency']=='Quarterly':
        inclist.append(inc.loc[i,'months_per_year']*inc.loc[i,'income_earned']/3)
    elif expend.loc[i,'frequency']=='Weekly':
        inclist.append(inc.loc[i,'months_per_year']*inc.loc[i,'income_earned']*4)
    elif expend.loc[i,'frequency']=='Daily':
        inclist.append(inc.loc[i,'months_per_year']*inc.loc[i,'income_earned']*30)
    else:
        inclist.append(0)
    
inc['total']=inclist
idlist=list(set(inc['customer_id']))
incdict={}
for i in idlist:
    temp=inc[inc['customer_id']==i]
    j=inc[inc['customer_id']==i].index[0]
    incdict[i]=sum(temp['total'])
    
for i in cust.index:
    if cust.loc[i,'id'] in incdict:
        cust.loc[i,'incdict']=incdict[cust.loc[i,'id']]


# In[18]:

rich=['Computer','Refrigerator','Washing Machine']
richlist=list()
i=0
for i in assets.index:
    if assets.loc[i,'owned_asset_details'] in rich:
        richlist.append(assets.loc[i,'customer_id'])
        
richlist=list(set(richlist))


for i in cust.index:
    j=cust.loc[i,'id']
    if j in richlist:
        cust.loc[i,'rich']=1
    else:
        cust.loc[i,'rich']=0
        


# In[19]:

for i in cust.index:
    if cust.loc[i,'occupation1']!='0' and cust.loc[i,'occupation2']!='0'and cust.loc[i,'occupation3']!='0' and cust.loc[i,'occupation4']!='0':
        cust.loc[i,'no_of_jobs']=4
    elif cust.loc[i,'occupation1']!='0' and cust.loc[i,'occupation2']!='0' and cust.loc[i,'occupation3']!='0':
        cust.loc[i,'no_of_jobs']=3
    elif cust.loc[i,'occupation1']!='0' and cust.loc[i,'occupation2']!='0':
        cust.loc[i,'no_of_jobs']=2
    else:
        cust.loc[i,'no_of_jobs']=1


# In[28]:

edulist=list()
for i in expend.index:
    if expend.loc[i,'expenditure_source'] == 'Education - Fees':
        edulist.append(expend.loc[i,'customer_id'])
        
inslist=list()
for i in expend.index:
    if expend.loc[i,'expenditure_source'] == 'Insurance':
        inslist.append(expend.loc[i,'customer_id'])
        
cust['edu']=0

for i in edulist:
    j=cust[cust['id']==i].index[0]
    cust.loc[j,'edu']=1
    
    
cust['insurance']=0

for i in inslist:
    j=cust[cust['id']==i].index[0]
    cust.loc[j,'insurance']=1
    

for i in cust.index:
    if cust.loc[i,'edu']==1 and cust.loc[i,'insurance']==1:
        cust.loc[i,'edu-ins']=1
    else:
        cust.loc[i,'edu-ins']=0


# In[21]:

for i in cust.index:
    if cust.loc[i,'loan_amt']>22000:
        cust.loc[i,'bucket']=3
    elif cust.loc[i,'loan_amt']>=19000:
        cust.loc[i,'bucket']=2
    else:
        cust.loc[i,'bucket']=1


# In[ ]:




# In[22]:

maincust=pd.DataFrame()

idl=cust['id']

for i in idl:
    temp=loan[loan['customer_id']==i]
    prodlist=list(set(temp['product_id']))
    j=0
    for prod in prodlist:
        
        temp2=temp[temp['product_id']==prod]
        temp2['customer_id']=temp2['customer_id']*10 + j
        maincust=maincust.append(temp2)
        j+=1
 
   


# In[33]:

idlist=list(set(maincust['customer_id']))
oldlist=list()
for i in cust['id']:
    oldlist.append(i)

    
for i in idlist:
    k=int(i/10)
    if k in oldlist:
        try:
            j=cust[cust['id']==k].index[0]
            cust=cust.append(cust.loc[j,],ignore_index=True)
            cust.loc[len(cust)-1,'id']=i
        except:
            print(i,k)
    

        
  


# In[39]:

cust=cust.ix[len(oldlist):]    


# In[44]:

for i in cust.index:
    j=cust.loc[i,'id']
    temp=maincust[maincust['customer_id']==j]
    temp=temp.reset_index()
    if temp.loc[0,'group_code']!='\\N':
        cust.loc[i,'group']=1
    else:
        cust.loc[i,'group']=0
        
    


# In[25]:

for i in cust.index:
    j=cust.loc[i,'id']%10
    if j==0:
        cust.loc[i,'loan_no']=1
    elif j==1:
        cust.loc[i,'loan_no']=2
    elif j==2:
        cust.loc[i,'loan_no']=3
    elif j==3:
        cust.loc[i,'loan_no']=4
    else:
        cust.loc[i,'loan_no']=5


# In[29]:

idlist=cust['id']
weekdict={}
for i in idlist:
    temp=loan[loan['customer_id']==i]
    j=loan[loan['customer_id']==i].index[0]
    if loan.loc[j,'frequency']=='EWI':
        weekdict[i]=1
    else:
        weekdict[i]=0
    
for i in cust.index:
    if cust.loc[i,'id'] in weekdict:
        cust.loc[i,'weekly']=weekdict[cust.loc[i,'id']]
        
        
lendict={}
for i in idlist:
    temp=loan[loan['customer_id']==i]
    j=loan[loan['customer_id']==i].index[0]
    lendict[i]=temp.loc[j,'tenure']
    
for i in cust.index:
    if cust.loc[i,'id'] in lendict:
        cust.loc[i,'tenure']=lendict[cust.loc[i,'id']]

    
        


# In[45]:

cust.to_csv('Master.csv',index=False)
maincust.to_csv('NewLoan.csv',index=False)


# In[37]:

cust.head()


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




# In[ ]:




# In[ ]:




# In[ ]:



