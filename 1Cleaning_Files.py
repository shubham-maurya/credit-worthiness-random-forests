
# coding: utf-8

# In[2]:

#This file takes out only the necessary columns from each spreadsheet
import pandas as pd
inc=pd.read_csv('income.csv',header=0,low_memory=False)
inc=inc[['id','income_source','income_earned','frequency','months_per_year','customer_id','occupation_master_id','marital_status']]
assets=pd.read_csv('assets.csv',header=0,low_memory=False)
assets=assets[['id','name_of_owned_asset','number_of_owned_asset','owned_asset_details','customer_id']]
expenditure=pd.read_csv('expenditure.csv',header=0,low_memory=False)
expenditure=expenditure[['id','expenditure_source','annual_expenses','frequency','customer_id']]
family=pd.read_csv('family.csv',header=0,low_memory=False)
family=family[['id','gender','relationship','date_of_birth','education_status','customer_id','enrollment_id']]
customer=pd.read_csv('customer.csv',header=0,low_memory=False)
customer=customer[['id','gender','caste','religion','language','exserviceman','village_name','occupation1','occupation2','occupation3','occupation4','start_date_time']]
loan=pd.read_csv('loanDemandSchedule.csv',header=0,low_memory=False)
loan=loan[loan['repayment_date']!='\\N']
customer.to_csv('Customer.csv',index=False)
inc.to_csv('Income.csv',index=False)
assets.to_csv('Assets.csv',index=False)
expenditure.to_csv('Expenditure.csv',index=False)
loan.to_csv('Loan.csv',index=False)
family.to_csv('Family.csv',index=False)


# In[1]:




# In[ ]:



