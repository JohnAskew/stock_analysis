import os, sys

try:

    from get_future_dates import calc_future_date

except Exception as e:

    print("tools_predict_closing unable to access module get_future_dates routine calc_future_date. Aborting")
    print(e)
    sys.exit(0)
try:

    import time

except:

    os.system('pip install time')

    import time

try:

    import math

except:

    os.system('pip install math')

    import math

try:

    import csv

except:

    os.system("pip3 install csv")

    import csv

try:

    import requests

except:

    os.system('pip install requests')

    import requests

try:

    import matplotlib as mpl

except:

    os.system('pip3 install matplotlib')

    import matplotlib as mpl

try:

    import matplotlib.pyplot as plt

except:

    os.system("pip3 install matplotlib")

    import matplotlib.pyplot as plt

from  matplotlib import style

try:

    import pandas as pd

except:

    os.system('pip3 install pandas')

    import pandas as pd

try:

    import numpy as np

except:

    os.system("pip3 install numpy")

    import numpy as np

try:

    from sklearn.svm import SVR

except:

    os.system('pip install sklearn.svm')

    from sklearn.svm import SVR

try:

    from sklearn.model_selection import train_test_split

except:

    os.system('pip install sklearn.model_selection')

    from sklearn.model_selection import train_test_split

try:

    from sklearn.svm import SVR

except:

    os.system('pip install sklearn.svm')

    from sklearn.svm import SVR

try:

    from sklearn.linear_model import LinearRegression

except:

    os.system('pip import sklearn.linear_model')

    from sklearn.linear_model import LinearRegression

try:

    from sklearn.preprocessing import MinMaxScaler

except:

    os.system('pip install sklearn.preprocessing')

    from sklearn.preprocessing import MinMaxScaler

try:

    import scipy

except:

    os.system('pip install scipy')

    import scipy

try:

    import tensorflow

except:

    os.system('pip install tensorflow')

    import tensorflow

try:

    from keras.models  import Sequential 

except:

    os.system('pip install keras')

    from keras.models  import Sequential 

from keras.layers import Dense, LSTM 




style.use('fivethirtyeight')

plt.rcParams['axes.formatter.useoffset'] = False

pd.plotting.register_matplotlib_converters()

######################################
# Functions
######################################
#------------------------------------#
def predict_prices(dates, prices, x):
#------------------------------------#
    print("tools_predict_closing: predict_prices ENTRY")
    #svr_lin = SVR(kernel = 'linear', C=1e3)
    svr_rbf = SVR(kernel = 'rbf', C=1e3, gamma = 0.1)
    svr_poly = SVR(kernel = 'poly', C = 1e3, degree = 2)

    #print("tools_predict_closing: predict_prices starting to svr_lin.fit data")
    #svr_lin.fit(dates, prices)
    
    print("tools_predict_closing: predict_prices starting to svr_poly.fit data")
    svr_poly.fit(dates, prices)
    poly_predict = svr_poly.predict(x)[0]

    print("tools_predict_closing: predict_prices starting to rbf_poly.fit data")
    svr_rbf.fit(dates, prices)
    rbf_predict = svr_rbf.predict(x)[0]

    plt.scatter(dates, prices, color='black', label = 'Data')
    plt.scatter( dates, svr_poly.predict(dates), color = 'green', label = 'Poly Model', alpha = 0.1)
    plt.scatter( dates, svr_rbf.predict(dates), color = 'red', label = 'RBF Model')
    plt.plot(x, poly_predict, '*', color = 'green', label = 'Poly Predict')
    plt.plot( x, rbf_predict, '*', color = 'blue', label = 'RBF Predicted')

    plt.xlabel('Date')
    plt.ylabel('Prices')
    plt.title("Support Vector Regression")
    plt.legend()
    plt.show

    print("Poly answer for predicting record", str(x), "is:",svr_poly.predict(x)[0])
    print("RBF answer for predicting record", str(x), "is:", rbf_predict )#svr_rbf.predict(x)[0])
    return  poly_predict, rbf_predict #svr_rbf.predict(x)[0]

#------------------------------------#
def build_model(x_train):
#------------------------------------#

    model = Sequential()

    model.add(LSTM(50, return_sequences = True, input_shape = (x_train.shape[1],1)))

    model.add(LSTM(50, return_sequences = False))

    model.add(Dense(25))

    model.add(Dense(1))

    #
    ## Compile the model
    #
    model.compile(optimizer = 'adam', loss = 'mean_squared_error')

    return model
#------------------------------------#
def build_train_data(dataset, training_data_len, scaled_data):
#------------------------------------#

    #
    ## Create training dataset
    #
    train_data = scaled_data[0:training_data_len, :]

    print("#-------------------#")
    print("tools_predict_closing: Creating 'train_data' with scaled_data for first", len(train_data), "records.")
    print("#-------------------#")
    print("")
    #
    ## Split the data into x_train and y_train
    #
    x_train = []

    y_train = []


    print("#-------------------#")
    print("tools_predict_closing: Preparing x_train to use all 'train_data' except last", train_2_test_days, "records.")
    print("#-------------------#")
    print("")

    for i in range(train_2_test_days,len(train_data)):

        x_train.append(train_data[i-train_2_test_days:i,0])

        y_train.append(train_data[i,0])

    print("#-------------------#")
    print("tools_predict_closing: x_train created with", len(x_train), "records.")
    print("tools_predict_closing: y_train created with", len(y_train), "records.")
    print("#-------------------#")
    print("")

    #
    ## Convert tht x_train and y_train to numpy arrays
    #
    x_train, y_train = np.array(x_train), np.array(y_train)
    #
    ## Reshape the data
    #
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    
    return  train_data, x_train, y_train

#------------------------------------#
def get_svr_rbf_predictions(df):
#------------------------------------#

    ##################################
    # Do the Close prediction first
    ##################################
    ## value for num prediction days
    forecast_out = 7
    
    df_close  = df[['Close']]

    df_close['Prediction'] = df_close[['Close']].shift(-forecast_out)
    
    #
    ## Create the independent dataset. Convert to numpy array
    #

    X_adjc = np.array(df_close.drop(['Prediction'],1))

    #
    ## Remove the last forecast_out number of rows
    #
    X_adjc = X_adjc[:-forecast_out]

    #
    ## Create the dependent dataset y. Convert df to array
    #
    y_adjc = np.array(df_close['Prediction'])

    y_adjc = y_adjc[:-forecast_out]

    #
    ## Split the data
    print("len(X_adjc",len(X_adjc))

    print("len(y_adjc)",len(y_adjc))
    #
    x_train_adjc, x_test_adjc, y_train_adjc, y_test_adjc = train_test_split(X_adjc, y_adjc, test_size = 0.2) 
    #
    ## Create and train the SVM Regressor
    #
    svr_rbf = SVR(kernel = 'rbf', C=1e3, gamma = 0.1)
    
    svr_rbf.fit(x_train_adjc, y_train_adjc)
    #
    ## Testing model score returns the coefficient of the determionation R^2 of the prediction.
    #
    svm_confidence = svr_rbf.score(x_test_adjc, y_test_adjc)

    print("svm_confidence:", svm_confidence)
    #
    ## Create x_forecast_adjc equal to last forecast_out days.
    #
    x_forecast_adjc = np.array(df_close.drop(['Prediction'], 1))[-forecast_out:]
    #
    ## Print the forecast
    #
    svm_prediction = svr_rbf.predict(x_forecast_adjc)
    
    print("svm_prediction:", svm_prediction)

    return svm_confidence, svm_prediction

#------------------------------------#
def train_and_predict(df):
#------------------------------------#
    data = df.filter(['Close'])

    dates = []
    prices = []


    #
    ## Get all data but last row for the SVM models
    #
    df_sv = df[:]

    #
    ## Get all tof the rows from the Open Column
    #
    df_sv_open = df['Open'][:]

    for price in df_sv_open:
        prices.append(float(price))

    df_sv.reset_index(inplace = True)
    #
    ## Get all Date rows
    #
    df_sv_dates = df_sv.iloc[:,0]


    ## Create the independent variable dataset X
    
    for x in range(len(df_sv_dates)):
            dates.append([x+1])


    dataset = data.values

    training_data_len = math.ceil(len(dataset) * train_2_test_ratio)

    scaler = MinMaxScaler(feature_range = (0,1))

    print("#-------------------#")
    print("tools_predict_closing: scaling 'dataset' of ", len(dataset), "records to values between 0 and 1")
    print("#-------------------#")
    print("")

    scaled_data = scaler.fit_transform(dataset)

    print("#-------------------#")
    print("tools_predict_closing: Full data set of just Close price named 'dataset' contains" ,len(dataset), "records. Training data will be first", training_data_len)
    print("#-------------------#")
    print("")
    ###################################
    ## Build training data
    ###################################
    train_data, x_train, y_train = build_train_data(dataset, training_data_len, scaled_data)

    ###################################
    ## Build the LSTM layer
    ###################################
    model = build_model(x_train)
    #
    ## Train the model
    #
    model.fit(x_train, y_train, batch_size =lstm_batch_size, epochs = lstm_epochs)
    #
    ## Create the testing data set
    ## Create the new array containing scaled values from index 143 to 
    #
    test_data = scaled_data[training_data_len - train_2_test_days:, :]
    #
    ## Create the data sets x_test and y_test
    #
    x_test = []

    y_test = dataset[ training_data_len:,: ]

    # print("tools_predict_closing: len(y_test)", len(y_test), "y_test:", y_test)


    for i in range(train_2_test_days, len(test_data) ): 

        x_test.append(test_data[i-train_2_test_days:i, 0]) 

    # print("len(x_test)", len(x_test), "x_test:", x_test)
    ## Convert the data to a numpy array
    #
    x_test = np.array(x_test)
    #
    ## Reshape the data

    # print("len(xtest)", len(x_test), "x_test.shape[0]", x_test.shape[0], "x_test.shape[1]:", x_test.shape[1])
    #
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    #
    ## Get the models predicted price values
    #
    predictions = model.predict(x_test)
    #
    ## Return predictions to same format as y_test
    #
    predictions = scaler.inverse_transform(predictions)
    #
    ## Get the root mean squared error (RMSE)
    #
    rmse = np.sqrt( np.mean( predictions - y_test )**2)

    print("rmse:", rmse)
    #
    ## Plot the data
    #
    train = data[:training_data_len]

    valid = data[training_data_len:]

    valid['Predictions_x_test'] = predictions

    return train, valid
 
######################################
# HOUSE KEEPING START HERE
######################################

train_2_test_days = 60 # Days from now going backwards to save off from training data to use as test data

train_2_test_ratio = .80 # What percent of population is allocated for training?

lstm_epochs = 10

lstm_batch_size = 10


currPath = os.getcwd()              # Directory you are in NOW

savePath = 'askew'                  # We will be creating this new sub-directory

myPath = (currPath + '/' + savePath)# The full path of the new sub-dir

dir_path = os.path.dirname(os.path.realpath(__file__))


if __name__ == '__main__':

    df = pd.DataFrame()

    if len(sys.argv) > 1:
        
        if sys.argv[1]:
        
           df = sys.argv[1]
        
    else:
        
        try:

            os.chdir(myPath)

            ax1_subject = 'JCP'

            df = pd.read_csv((ax1_subject + '.csv'), parse_dates=True, index_col =0)

        except Exception as e:

            print("stocks_1.py did not find", ax1_subject, "information. As it's not in the datawarehouse, is the ticker symbol spelled correctly?")

            print(e)

            popupmsg("Symbol " + ax1_subject + " is not found! -- Spelling?")

            sys.exit(0)

#######################################
# MAIN LOGIC
#######################################
df_future_dates = pd.DataFrame( columns = ["Date", "Close"])

svm_confidence, svm_prediction = get_svr_rbf_predictions(df[:])

next_7_days = calc_future_date()


for i in range(len(next_7_days)):
    df_future_dates.loc[len(df_future_dates)] = [next_7_days[i], svm_prediction[i]]

df_future_dates.set_index('Date', inplace = True)

df_future_dates.reset_index(inplace = True) 

train, valid = train_and_predict(df)

train.reset_index(inplace = True)

for i in range(len(df_future_dates)):
    train.loc[len(train)] = df_future_dates.iloc[i]

train.set_index('Date', inplace = True)

#train = train.iloc[-10:]

# #
# ## Visualize
# #
plt.figure(figsize = (16,8))

plt.title(ax1_subject + ' Model')

plt.xlabel('Date', fontsize = 18)

plt.ylabel('Close Price', fontsize =18)

df_future_dates.set_index('Date', inplace = True)
plt.plot(df_future_dates['Close'])
#plt.plot(train['Close'])
# valid.reset_index(inplace = True)

# plt.plot_date(valid['Date'], valid['Close'])
# plt.plot_date(valid['Date'], valid['Predictions_x_test'])



#plt.plot(valid[['Close', 'Predictions_x_test']])

#plt.legend(['Train_w_prediction' , 'Actual_last_60_day', 'Predicted_last_60_days'], loc = 'center left')
print(df_future_dates)
plt.show()



