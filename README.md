# credit-worthiness-random-forests
Contains the code used for feature selection, engineering and ultimately implementing and tuning a Random Forests model to predict credit worthiness of microfinance clients.

There are 5 .py scripts 
- 1Cleaning_Files
- 2Repayment_Data_Cust
- 3LoanGap
- 4MajorMod
- 5Model

They are in order of execution, according to the microfinance data. I have attempted to make it as general purpose as possible; to handle contingencies. 

The initial names of the .csv files containing the data must be named as mentioned in 1CleaningFiles, or else the code should be changed accordingly to adjust the file name (inc=pd.read_csv('FILENAME.csv',header=0,low_memory=False). Beyond this stage, the code requires no adjustment.

There are several design features of the model – for example, what condition to consider for a customer to be marked as ‘late’, what parameters (or combination of parameters) to incorporate to test the model. 
- 3LoanGap contains the decision rule I have used to flag defaulter
- 4MajorMod contains the significant parameters designed and taken into consideration

The 5Model script gives the results, ultimately.
- Significant Parameters for predicting defaulters
- Model Accuracy Score
- ROC Curve
