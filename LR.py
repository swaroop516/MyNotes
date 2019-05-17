# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd

dataset=pd.read_csv('kc_house_data.csv',index_col='id')
#Y=dataset.loc[:,['date','price']]
#Y.date =  pd.to_datetime(Y.date, format='%Y%m%dT%H%M%S')

DatasetNoIdex=pd.read_csv('kc_house_data.csv')

Y=dataset.loc[:,['price']]
X=dataset.drop(["price","zipcode","lat","long"], axis = 1)

#X=X.drop(["date","zipcode","lat","long"],axis = 1)

X.date=pd.to_numeric(X.date.str[:4])
X['Years']=X['date']-X['yr_built']

X=X.drop(["date","yr_built"],axis = 1)

#Making this field as flag if it is renovated
X['yr_renovated']=[1 if i >0 else 0 for i in X['yr_renovated']]

X=X.drop(['sqft_living15','sqft_lot15'],axis = 1)

#X["sqft_above"]=X["sqft_above"]*100/X["sqft_living"]

#X["sqft_basement"]=X["sqft_basement"]*100/X["sqft_living"]

#Total Area of Plot
X["Total_sqft"]=X["sqft_living"]+X["sqft_lot"]

#%age of area lot is contributing
X["sqft_lot"]=X["sqft_lot"]*100/X["Total_sqft"]

#%age of area living is contributing
X["sqft_above"]=X["sqft_above"]*100/X["Total_sqft"]

#%age of area basement is contributing
X["sqft_basement"]=X["sqft_basement"]*100/X["Total_sqft"]

X=X.drop(["Total_sqft","sqft_living"],axis = 1)

#Z=X

#deleting records which has Year of built > Year of purchase
X.drop(X[X.Years < 0].index, inplace=True)


Y=Y.drop([1832100030, 3076500830, 9520900210, 1250200495, 2770601530,
            9126100346, 9126100765, 9310300160, 1257201420, 6058600220,
           5694500840, 6169901185])

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

X_train,X_test,y_train,y_test=train_test_split(X,Y,test_size=0.1,random_state=0)

sc_X=StandardScaler()
X_train=sc_X.fit_transform(X_train)
X_test=sc_X.transform(X_test)

from sklearn.linear_model import LinearRegression
regressor=LinearRegression()
regressor.fit(X_train,y_train)

Y_pred=regressor.predict(X_test)

regressor.coef_
regressor.intercept_ 
regressor._estimator_type
regressor.singular_


from sklearn.svm import SVR

regressorSV=SVR(kernel='linear')
regressorSV.fit(X_train,y_train)
SV_pred=regressorSV.predict(X_test)

regressorSV.coef_
regressorSV.intercept_

###Feature selection process

#How much each feature contributing to target irrespective of correlation
from sklearn.feature_selection import f_regression
f1=f_regression(X,Y)

f_s=f_regression(X_train,y_train)



#How much each feature contributing to target which is correlated with each other feature
from sklearn.feature_selection import mutual_info_regression

m1=mutual_info_regression(X,Y)

m_s=mutual_info_regression(X_train,y_train)


#
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
bestfeatures = SelectKBest(score_func=chi2, k=10)

fit = bestfeatures.fit(X,Y)

dfscores = pd.DataFrame(fit.scores_)
dfcolumns = pd.DataFrame(X.columns)
#concat two dataframes for better visualization 
featureScores = pd.concat([dfcolumns,dfscores],axis=1)
featureScores.columns = ['Specs','Score']  #naming the dataframe columns
print(featureScores.nlargest(10,'Score'))  #print 10 best features







#correlation matrix
import seaborn as sns


data=pd.concat([X,Y],axis=1)
corrmat = data.corr()
top_corr_features = corrmat.index
plt.figure(figsize=(20,20))
#plot heat map
g=sns.heatmap(data[top_corr_features].corr(),annot=True,cmap="RdYlGn")




#Sqft=dataset.loc[:,['price','sqft_living','sqft_lot','sqft_above','sqft_basement','sqft_living15','sqft_lot15','yr_renovated','yr_built']]

#Sqft=DatasetNoIdex.loc[:,['date','price','sqft_living','sqft_lot','sqft_living15','sqft_lot15','yr_renovated','yr_built']]
#Sqft['Year']=pd.to_numeric(Sqft.date.str[:4])



import seaborn as sns

sns.pairplot(data, x_vars=['bedrooms', 'bathrooms', 'sqft_lot', 'floors', 'waterfront', 'view','condition', 'grade', 'sqft_above', 'sqft_basement', 'yr_renovated','Years'], y_vars='price', size=7, aspect=0.7)

sns.pairplot(data, x_vars=['bedrooms', 'bathrooms', 'sqft_lot', 'floors', 'waterfront', 'view','condition', 'grade', 'sqft_above', 'sqft_basement', 'yr_renovated','Years'], y_vars='price', size=7, aspect=0.7,kind='reg')





import matplotlib.pyplot as plt



plt.plot_date(Y.date,Y.price)
plt.show()


Z=Y.groupby('date').count()
plt.plot_date(Z.index,Z.price)




pd.unique(X['zipcode'])
X['zipcode'].value_counts()

Area=dataset.loc[:,['zipcode','lat','long','price']]

plt.scatter(Area.zipcode,Area.price)
plt.ylabel('Price')
plt.xlabel('Zipcode')
plt.grid(True)
plt.show()


MeanPrice=Area.groupby('zipcode')['price'].mean()


#98103,98038,98115,98052
#
#
#test=Area[Area.zipcode.isin([98103,98038,98115,98052,98010,98024,98148,98039])]
#
#98103,98038,98115,98052
#98010,98024,98148,98039
#
#t_mean=test.groupby('zipcode').mean()
#
#MinLatLong=Area.groupby("zipcode", as_index=False)["lat","long"].min()
#MaxLatLong=Area.groupby("zipcode", as_index=False)["lat","long"].max()
#
#PinLatLong=MinLatLong.append(MaxLatLong)
#
#
#
#
