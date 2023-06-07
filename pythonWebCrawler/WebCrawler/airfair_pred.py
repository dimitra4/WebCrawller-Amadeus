import pandas as pd
import numpy as np
import pickle
from dbQueries import findUniqueCarrierCodeForDest, findUniqueTotalStopsForDest
from datetime import datetime as dt
from sklearn.preprocessing import LabelBinarizer



train_data = pd.read_csv("./country_new.csv")
train_data.drop('id', axis=1, inplace=True)
train_data.drop('departureIataCode', axis=1, inplace=True)
train_data.drop('destinationIataCode', axis=1, inplace=True)
train_data.drop('departureIataCodeValidation', axis=1, inplace=True)
train_data.drop('destinationRegion', axis=1, inplace=True)
train_data.drop('arrival', axis=1, inplace=True)
train_data.drop('arrivalTime', axis=1, inplace=True)
train_data.drop('duration', axis=1, inplace=True)
train_data.drop('dateInserted', axis=1, inplace=True)
train_data.drop('timeInserted', axis=1, inplace=True)
train_data.drop('countOfOffers', axis=1, inplace=True)
train_data.drop('numberOfFlight', axis=1, inplace=True)
train_data.drop('departureName', axis=1, inplace=True)


#we want to convert time objects to timestamp
def change_to_datetime(col):
    train_data[col]=pd.to_datetime(train_data[col])

for i in ['flightDate', 'departureTime' ]:
    change_to_datetime(i)

train_data['flight_day']=train_data['flightDate'].dt.day
train_data['flight_month']=train_data['flightDate'].dt.month
train_data.drop('flightDate', axis=1, inplace=True)

def extract_time(df, col):
    df[col+'_hours']=df[col].dt.hour
    df[col+'_minutes']=df[col].dt.minute
    df.drop(col, axis=1, inplace=True)

extract_time(train_data, 'departureTime')

def find_hour(x):
    pos= x.find('H')
    if(pos != -1 ):
        # print("H found ",x, " in position: ", pos)
        ret= x[2:pos]
        if(ret[0]== 'T'):
            ret = ret[1:]
    else:
        ret= 0
    return ret

def find_minutes(x):
    pos= x.find('M')
    
    if(pos != -1 ):
        # print("M found ",x, " in position: ", pos)
        ret = x[pos-2:pos]
        if(ret[0] == 'H' or ret[0]== 'T'):
            ret = ret[1:]
    else:
        ret = 0
    return ret



cat_col = [col for col in train_data.columns if train_data[col].dtype == 'O'] # object type data are considered categorical
cont_col = [col for col in train_data.columns if train_data[col].dtype != 'O'] # continues data


categorical_data = train_data.filter(cat_col, axis =1)


#Handle categorical  data with onehot encoding
enc1 = LabelBinarizer()
enc1.fit(categorical_data['carrierCode'])
transformed = enc1.transform(categorical_data['carrierCode'])
airline = pd.DataFrame(transformed, columns=enc1.classes_)


enc2 = LabelBinarizer()
enc2.fit(categorical_data['destinationName'])
transformed2 = enc2.transform(categorical_data['destinationName'])
destination = pd.DataFrame(transformed2, columns=enc2.classes_)

enc_dict={"airlines":enc1, "destinations":enc2 }
file=open('./encoders.pkl', 'wb')
pickle.dump(enc_dict, file)
file.close()



categorical_data.drop('carrierCode', axis=1, inplace=True)
categorical_data.drop('destinationName', axis=1, inplace=True)


final_train_data = pd.concat([ airline, destination, train_data[cont_col]], axis=1)

#handle extreme values
final_train_data['price'] = np.where(final_train_data['price']>=3000, final_train_data['price'].median(), final_train_data['price'])

X=final_train_data.drop('price', axis=1)
y= final_train_data['price']

"airlines1hot, departure1hot, destination1hot, totalStops, flight_day, flight_month, departureTime_hours, departureTime_minutes"
print("final_train_data:: ", X)

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

def predict(ml_model, dump, X_test):
    model= ml_model.fit(X_train, y_train)
    print('Training score {}'.format(model.score(X_train,y_train)))
    predictions = model.predict(X_test)
    print('Predictions : {}'.format( predictions ))
    r2_score = metrics.r2_score(y_test, predictions)
    if dump == 1:
        file=open('./model.pkl', 'wb+')
        pickle.dump(model, file)
        file.close()

predict(RandomForestRegressor(n_estimators = 100),1, X_test)



def predictPrice(sday, smonth, destination, stops):
   
    dep_hours = ["9:00:00", "12:00:00", "18:00:00", "22:00:00", "2:00:00"]

    test_airlines = []
    test_flightDays=[]
    test_flightMonth=[]
    test_destinationName=[]
    test_stops=[]
    test_hours=[]
    test_minutes=[]

    encoders={}
    enc_file = open("./encoders.pkl", 'rb')
    encoders = pickle.load(enc_file)
    enc1=  encoders["airlines"]
    enc2 = encoders["destinations"]
    enc_file.close()

    airlines = findUniqueCarrierCodeForDest(destination)
    stops_lst= [0] 
    if(stops == 1): stops_lst.append(1) 
    for line in airlines:   
        if line not in enc1.classes_ : continue #there might be unknown values to the encoder
        for hour in dep_hours:
            for stops in stops_lst:
                fhour= dt.strptime(hour, '%X')
                test_airlines.append(line) 
                test_flightDays.append(sday)
                test_flightMonth.append(smonth)
                test_destinationName.append(destination)
                test_stops.append(stops)
                test_hours.append(fhour.hour)
                test_minutes.append(fhour.minute)   
            
    
    test_airlines_df = pd.DataFrame(data=test_airlines)
    transformed_airlines = enc1.transform(test_airlines_df)
    test_airlines = pd.DataFrame(transformed_airlines, columns=enc1.classes_)
    
    test_destinationName_df = pd.DataFrame(data=test_destinationName)
    transformed_destinationName = enc2.transform(test_destinationName_df)
    test_destinationName = pd.DataFrame(transformed_destinationName, columns=enc2.classes_)
    
    dt_cont= pd.DataFrame(list(zip(test_stops, test_flightDays, test_flightMonth, test_hours, test_minutes)), columns=["totalStops", "flight_day", "flight_month", "departureTime_hours", "departureTime_minutes"] )
    test_set= pd.concat([ test_airlines, test_destinationName, dt_cont], axis=1)
    
    model_file = open("./model.pkl", 'rb')
    loaded_model = pickle.load(model_file)
    predictions = loaded_model.predict(test_set)
    print('Predictions : {}'.format( predictions ))
    avg = sum(predictions)/len(predictions)
    print("Average: ", avg)

    model_file.close()
    
    return avg
                                    

   