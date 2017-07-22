
# coding: utf-8

# In[ ]:

#This file contains the Random Forests Implementation for the data
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import preprocessing
from sklearn.metrics import roc_curve, auc


# In[ ]:


cust=pd.read_csv('Master.csv',header=0)



# In[ ]:

for i in cust.index:
    if cust.loc[i,'gender']=='MALE':
        cust.loc[i,'sex']=0
    else:
        cust.loc[i,'sex']=1

cust=cust.drop('gender',1)

cust.rename(columns={'tenured':'tenure'}, inplace=True)
for i in cust.index:
    if cust.loc[i,'caste']=='OBC':
        cust.loc[i,'caste1']=0
    elif cust.loc[i,'caste']=='SC' or cust.loc[i,'caste']=='ST':
        cust.loc[i,'caste1']=1
    else:
        cust.loc[i,'caste1']=2

cust=cust.drop('caste',1)
cust.rename(columns={'caste1':'caste'}, inplace=True)


for i in cust.index:
    if cust.loc[i,'religion']=='Hindu':
        cust.loc[i,'rel']=0
    elif cust.loc[i,'religion']=='Christian':
        cust.loc[i,'rel']=1
    else:
        cust.loc[i,'rel']=2

cust=cust.drop('religion',1)
cust.rename(columns={'rel':'religion'}, inplace=True)







# In[ ]:




# In[ ]:

df=cust[['sex','religion','occ','self_edu','jewel','land','age','fam_size','family_edu','expenses','rich','no_of_jobs','edu-ins','bucket','group','tenure','loan_no','late']]


# In[ ]:

df = df.apply(lambda x:x.fillna(x.value_counts().index[0]))


# In[ ]:

df['is_train'] = np.random.uniform(0, 1, len(df)) <= .66
train, validate = df[df['is_train']==True], df[df['is_train']==False]


# In[ ]:

#Raw implementation of Random Forests. First Value is area under ROC Curve, second is efficiency score
from sklearn import cross_validation
rf = RandomForestClassifier()
rf.fit(train.drop('late',axis=1),train['late'])

disbursed = rf.predict_proba(validate.drop('late',axis=1))
fpr, tpr, _ = roc_curve(validate['late'], disbursed[:,1])
roc_auc = auc(fpr, tpr)
print (roc_auc)


scores = cross_validation.cross_val_score(rf, df.drop('late',1), df.late, cv=5)

scores
print(sum(scores)/5)



# In[ ]:

#Now, detailed implementation of Random Forests begins


# In[ ]:

import sklearn
from sklearn.cross_validation import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from scipy.stats import pointbiserialr, spearmanr
get_ipython().magic('matplotlib inline')
import math
columns = df.columns.values

param=[]
correlation=[]
abs_corr=[]

for c in columns:
    #Check if binary or continuous
    if len(df[c].unique())<=4:
        corr = spearmanr(df['late'],df[c])[0]
    else:
        corr = pointbiserialr(df['late'],df[c])[0]
    param.append(c)
    correlation.append(corr)
    abs_corr.append(abs(corr))

#Create dataframe for visualization
param_df=pd.DataFrame({'correlation':correlation,'parameter':param, 'abs_corr':abs_corr})

#Sort by absolute correlation
param_df=param_df.sort_values(by=['abs_corr'], ascending=False)

#Set parameter name as index
param_df=param_df.set_index('parameter')


param_df
i=0
for i in param_df.index:
        
    try:
        r=param_df.loc[i,'correlation']
        param_df.loc[i,'t']=r*math.sqrt(4770/(1-(math.pow(r,2))))
    except:
        print('lol')
        
param_df
    



# In[ ]:

scoresCV = []
scores = []
import matplotlib.pyplot as plt
for i in range(1,len(param_df)):
    new_df=df[param_df.index[0:i+1].values]
    X = new_df.ix[:,1::]
    y = new_df.ix[:,0]
    clf = DecisionTreeClassifier()
    scoreCV = sklearn.cross_validation.cross_val_score(clf, X, y, cv= 5)
    scores.append(np.mean(scoreCV))
    
plt.figure(figsize=(20,8))
plt.plot(range(1,len(scores)+1),scores, '.-')
plt.axis("tight")
plt.title('Feature Selection', fontsize=14)
plt.xlabel('# Features', fontsize=12)
plt.ylabel('Score', fontsize=12)
plt.grid();


# In[ ]:

best_features=param_df.index[1:4+1].values
print('Best features:\t',best_features)


# In[ ]:

df[best_features].hist(figsize=(20,15))


# In[ ]:

X = df[best_features]
y = df['late']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=44)


# In[ ]:




# In[ ]:

plt.figure(figsize=(25,15))

#N Estimators
plt.subplot(3,3,1)
feature_param = range(1,21)
scores=[]
for feature in feature_param:
    clf = RandomForestClassifier(n_estimators=feature)
    clf.fit(X_train,y_train)
    scoreCV = clf.score(X_test,y_test)
    scores.append(scoreCV)
plt.plot(scores, '.-')
plt.axis('tight')
# plt.xlabel('parameter')
# plt.ylabel('score')
plt.title('N Estimators')
plt.grid();

#Criterion
plt.subplot(3,3,2)
feature_param = ['gini','entropy']
scores=[]
for feature in feature_param:
    clf = RandomForestClassifier(criterion=feature)
    clf.fit(X_train,y_train)
    scoreCV = clf.score(X_test,y_test)
    scores.append(scoreCV)
plt.plot(scores, '.-')
# plt.xlabel('parameter')
# plt.ylabel('score')
plt.title('Criterion')
plt.xticks(range(len(feature_param)), feature_param)
plt.grid();

#Max Features
plt.subplot(3,3,3)
feature_param = ['auto','sqrt','log2',None]
scores=[]
for feature in feature_param:
    clf = RandomForestClassifier(max_features=feature)
    clf.fit(X_train,y_train)
    scoreCV = clf.score(X_test,y_test)
    scores.append(scoreCV)
plt.plot(scores, '.-')
plt.axis('tight')
# plt.xlabel('parameter')
# plt.ylabel('score')
plt.title('Max Features')
plt.xticks(range(len(feature_param)), feature_param)
plt.grid();

#Max Depth
plt.subplot(3,3,4)
feature_param = range(1,21)
scores=[]
for feature in feature_param:
    clf = RandomForestClassifier(max_depth=feature)
    clf.fit(X_train,y_train)
    scoreCV = clf.score(X_test,y_test)
    scores.append(scoreCV)
plt.plot(feature_param, scores, '.-')
plt.axis('tight')
# plt.xlabel('parameter')
# plt.ylabel('score')
plt.title('Max Depth')
plt.grid();

#Min Samples Split
plt.subplot(3,3,5)
feature_param = range(1,21)
scores=[]
for feature in feature_param:
    clf = RandomForestClassifier(min_samples_split =feature)
    clf.fit(X_train,y_train)
    scoreCV = clf.score(X_test,y_test)
    scores.append(scoreCV)
plt.plot(feature_param, scores, '.-')
plt.axis('tight')
# plt.xlabel('parameter')
# plt.ylabel('score')
plt.title('Min Samples Split')
plt.grid();

#Min Weight Fraction Leaf
plt.subplot(3,3,6)
feature_param = np.linspace(0,0.5,10)
scores=[]
for feature in feature_param:
    clf = RandomForestClassifier(min_weight_fraction_leaf =feature)
    clf.fit(X_train,y_train)
    scoreCV = clf.score(X_test,y_test)
    scores.append(scoreCV)
plt.plot(feature_param, scores, '.-')
plt.axis('tight')
# plt.xlabel('parameter')
# plt.ylabel('score')
plt.title('Min Weight Fraction Leaf')
plt.grid();

#Max Leaf Nodes
plt.subplot(3,3,7)
feature_param = range(2,21)
scores=[]
for feature in feature_param:
    clf = RandomForestClassifier(max_leaf_nodes=feature)
    clf.fit(X_train,y_train)
    scoreCV = clf.score(X_test,y_test)
    scores.append(scoreCV)
plt.plot(feature_param, scores, '.-')
plt.axis('tight')
# plt.xlabel('parameter')
# plt.ylabel('score')
plt.title('Max Leaf Nodes')
plt.grid();


# In[ ]:

df['is_train'] = np.random.uniform(0, 1, len(df)) <= .66
train, validate = df[df['is_train']==True], df[df['is_train']==False]
from sklearn import cross_validation
rf = RandomForestClassifier(n_estimators=15,criterion='gini',max_features='log2',max_depth=15,max_leaf_nodes=5,min_samples_split=6)
rf.fit(X_train,y_train)

disbursed = rf.predict_proba(X_test)
fpr, tpr, _ = roc_curve(y_test, disbursed[:,1])
roc_auc = auc(fpr, tpr)
print (roc_auc)


scores = cross_validation.cross_val_score(rf, df.drop('late',1), df.late, cv=5)

scores
final=sum(scores)/5




# In[ ]:

#Final score of the model! Average value of 5 fold cross validation
final


# In[ ]:




# In[ ]:




# In[ ]:




# 

# In[ ]:

import seaborn as sns
import matplotlib.pyplot as plt
sns.set_style('whitegrid')
get_ipython().magic('matplotlib inline')
# .... continue with plot Age column

# peaks for survived/not survived passengers by their age
# average survived passengers by age
fig, axis1 = plt.subplots(1,1,figsize=(18,4))
average_age = df[['loan_no', "late"]].groupby(['loan_no'],as_index=False).mean()

sns.barplot(x='loan_no', y='late', data=average_age)
plt.axhline(y=.3105, xmin=0, xmax=1, linewidth=1.5, color = 'black')



# In[ ]:



