import pandas as pd
import numpy as np
#import seaborn as  sns
#import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder


train_data = pd.read_csv("./country_new.csv")
train_data.drop('id', axis=1, inplace=True)
train_data.drop('departureIataCode', axis=1, inplace=True)
train_data.drop('destinationIataCode', axis=1, inplace=True)
train_data.drop('arrival', axis=1, inplace=True)
train_data.drop('arrivalTime', axis=1, inplace=True)
train_data.drop('departureTime', axis=1, inplace=True)
train_data.drop('duration', axis=1, inplace=True)
train_data.drop('carrierCode', axis=1, inplace=True)


# print( train_data.dtypes) #to check the data type

#id,price,departureIataCode,departureName,flightDate,destinationIataCode,
# destinationName,arrival,carrierCode,numberOfFlight,departureTime,arrivalTime,duration,totalStops

#we want to convert time objects to timestamp
def change_to_datetime(col):
    train_data[col]=pd.to_datetime(train_data[col])

for i in ['flightDate' ]:
    change_to_datetime(i)

train_data['flight_day']=train_data['flightDate'].dt.day
train_data['flight_month']=train_data['flightDate'].dt.month
train_data.drop('flightDate', axis=1, inplace=True)

def extract_time(df, col):
    df[col+'_hours']=df[col].dt.hour
    df[col+'_minutes']=df[col].dt.minute
    df.drop(col, axis=1, inplace=True)
    # print("hour ",  df[col+'_hour'])
    # print("min ", df[col+'_minute'])

# extract_time(train_data, 'arrivalTime')
#extract_time(train_data, 'departureTime')

def find_hour(x):
    pos= x.find('H')
    if(pos != -1 ):
        print("H found ",x, " in position: ", pos)
        ret= x[2:pos]
        if(ret[0]== 'T'):
            ret = ret[1:]
    else:
        ret= 0
    return ret

def find_minutes(x):
    pos= x.find('M')
    
    if(pos != -1 ):
        print("M found ",x, " in position: ", pos)
        ret = x[pos-2:pos]
        if(ret[0] == 'H' or ret[0]== 'T'):
            ret = ret[1:]
    else:
        ret = 0
    return ret

# train_data['duration_hours']=train_data['duration'].apply(find_hour)
# train_data['duration_minutes']=train_data['duration'].apply(find_minutes)
# train_data.drop('duration', axis=1, inplace=True)

features = [ 'price',  'flightDate',  'destinationName' ]

# print("hours ", train_data['duration_hours'])
# print("minutes ", train_data['duration_minutes'])

cat_col = [col for col in train_data.columns if train_data[col].dtype == 'O'] # object type data are considered categorical
print (cat_col)

cont_col = [col for col in train_data.columns if train_data[col].dtype != 'O'] # continues data
print (cont_col)
#[ 'price', 'flightDate', 'totalStops']

categorical_data = train_data.filter(cat_col, axis =1)

print("--------------------")
#Handle categorical  data with onehot encoding
# airline = pd.get_dummies(categorical_data['carrierCode'], drop_first=True)
departure = pd.get_dummies(categorical_data['departureName'], drop_first=True)
destination = pd.get_dummies(categorical_data['destinationName'], drop_first=True)

# categorical_data.drop('carrierCode', axis=1, inplace=True)
categorical_data.drop('departureName', axis=1, inplace=True)
categorical_data.drop('destinationName', axis=1, inplace=True)

print(">>>>>>>>>>>>> ", categorical_data)

final_train_data = pd.concat([categorical_data, departure, destination, train_data[cont_col]], axis=1)

#handle extreme values
final_train_data['price'] = np.where(final_train_data['price']>=3000, final_train_data['price'].median(), final_train_data['price'])

X=final_train_data.drop('price', axis=1)
y= final_train_data['price']

from sklearn import preprocessing
from sklearn import utils
lab_enc = preprocessing.LabelEncoder()
#y_encoded= lab_enc.fit_transform(y)
def toInt(x):
    return int(x)
y_encoded= y.apply(toInt)


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded,test_size=0.1)

from sklearn import metrics
from sklearn.ensemble import RandomForestRegressor
import pickle
def predict(ml_model, dump, X_test):
    model= ml_model.fit(X_train, y_train)
    print('Training score {}'.format(model.score(X_train,y_train)))
    predictions = model.predict(X_test)
    print('Predictions : {}'.format( predictions ))
    r2_score = metrics.r2_score(y_test, predictions)
    if dump == 1:
        file=open('./model.pkl', 'wb')
        pickle.dump(model, file)

predict(RandomForestRegressor(n_estimators = 200),1, X_test)


#id,price,departureIataCode,departureName,flightDate,destinationIataCode,destinationName,arrival,carrierCode,numberOfFlight,departureTime,arrivalTime,duration,totalStops

print( y_test )