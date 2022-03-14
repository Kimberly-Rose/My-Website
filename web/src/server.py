from pyramid.config import Configurator
from pyramid.renderers import render_to_response
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound
import os
from waitress import serve
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn import preprocessing

# for debugging
#pd.set_option('display.max_columns', None)

# Derek's normalization function to normalize data for the model
def normaliziation(df):
    '''
    Normaliziated the input data frame
    df(data frame): data frame that havs the label as last coloumn
    df_n(data frame): a normaliziation of the input df
    '''
    x = df[df.columns].values
   
    #print('X INSIDE NORMALIZATION:')
    #print(x)
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x.T)
    #print('X SCALED INSIDE NORMALIZATION:')
    #print(x_scaled)
    df_n = pd.DataFrame(x_scaled.T, columns= df[df.columns].columns)
    #print('NORMALIZED ROW')
    #print(df_n)
    return df_n

def get_weighted_bmi(bmi):
  '''
    This function returns a weighted bmi to use with the model
    For Type II Diabetes, being overweight carries a substantial 
    risk so higher BMIs will have higher ranks
  '''
  weighted_bmi = 0
  
  if bmi >= 40:
     weighted_bmi = 5
    
  if bmi in range(30, 40):
     weighted_bmi = 4
    
  if bmi in range(25, 30): 
     weighted_bmi = 3
    
  if  bmi in range(19, 25): 
     weighted_bmi = 2
    
  if bmi < 18:
     weighted_bmi = 1

  return weighted_bmi

def calculate_risk(a_dict):
  '''
     This function converts the input dictionary into a dataframe,
     puts 'Diabetes' in the last column for the normalization function
     which is called to normalize the data, and loads the machine learning 
     model and uses it to predict the risk of diabetes, returning the result
  '''
  # the expected order of columns in the data set
  column_order = ['General_Health', 'BMI', 'Poor_Physical', 'Poor_Mental', 'Exercise',
                  'Sleep', 'Smoker', 'Heavy_Alcohol', 'Stroke', 'Heart_Disease',
                  'Age_Stage', 'Sex', 'Health_Care', 'Poor_Doc', 'Income_Level',
                  'Edu_Level', 'Dental', 'Checkup'
                 ]

  # prepare the dict for conversion to df by converting
  # its values into lists
  the_dict = {key: [value] for key, value in a_dict.items()}
  df = pd.DataFrame.from_dict(the_dict)
 
  # reorder the columns to match the order in the dataset
  df = df.reindex(columns=column_order)
  df.astype('float').dtypes
  #print('df before normalization')
  #print(df)
   
  # normalize the row
  row = normaliziation(df)
  
  # get prediction
  model = pickle.load(open('finalized_model.sav', 'rb'))
  x = row[row.columns].to_numpy()
  y = model.predict(x)[0]
  #print(f'RESULT OF PREDICTION {y}')
  
  results = {
               0: '''    You are currently NOT AT RISK of developing Type II Diabetes. 
    This information is not medical advice from a doctor and is for 
    educational purposes only, please contact your health care provider 
    to completely assess your risk.
    ''',
               1: '''    You are currently AT RISK of developing Type II Diabetes.
    This information is not medical advice from a doctor and is for 
    educational purposes only, please contact your health care provider 
    to completely assess your risk.
    '''
             }
    
  #return {"status" : (results.get(y)) } if results.get(y) is not None else {"status" : "UNDETERMINED"}
  return results.get(y) if results.get(y) is not None else "UNDETERMINED"


def receive_form(req):
    '''
       This function takes the POST request from the diabetes form and extracts all of the
       responses. The fields correspond to the columns in the diabetes data set, and there
       are 3 custom fields (feet, inches, pounds),  which will be used to calculate BMI.
       Race has been excluded since it was not used in the trained model.
    '''
    fields = ['General_Health', 'Poor_Physical', 'Poor_Mental', 'Exercise',
              'Sleep', 'Smoker', 'Heavy_Alcohol', 'Stroke', 'Heart_Disease',
              'Age_Stage', 'Sex', 'Health_Care', 'Poor_Doc', 'Income_Level',
              'Edu_Level', 'Dental', 'Checkup', 'feet', 'inches', 
              'pounds'
              ]
    
    # a python dict where the keys are the names from the html attributes and the values are
    # their values
    formInfo = req.POST.mixed()
    
    # make sure all fields match corresponding columns
    sortedFields = sorted(fields)
    #print('SORTED FIELDS')
    #print(sortedFields)
    sortedColumns = sorted(list(formInfo.keys()))
    #print("SORTED FORM DATA")
    #print(sortedColumns)
    
    assert sortedFields == sortedColumns, "ERROR fields from POST do not match columns"
    
    # calculate BMI and remove the BMI variables of feet, inches, pounds
    feet = formInfo.pop('feet').strip()
    inches = formInfo.pop('inches').strip()
    weight = formInfo.pop('pounds').strip()
    assert all([feet.isnumeric(), inches.isnumeric(), weight.isnumeric()]), "ERROR invalid values for feet,inches,pounds"
    
    # convert feet and inches to inches
    total_inches = (int(feet) * 12) + int(inches) 
    
    # use formula for BMI
    bmi = int(703 * ((int(weight)) / (total_inches*total_inches)))
   
    weighted_bmi = get_weighted_bmi(bmi)

    bmi_string = f'BMI is {bmi}'.format(bmi=bmi)
    #print(bmi_string)

    weighted_bmi_string = f'Weighted BMI is {weighted_bmi}'.format(weighted_bmi=weighted_bmi)
    #print(weighted_bmi_string)

    # add bmi to formInfo
    formInfo['BMI'] = weighted_bmi
    weighted_bmi = 0
    
    if bmi >= 40:
        weighted_bmi = 5
    
    if bmi >= 30:
        weighted_bmi = 4
    
    if bmi >= 25: 
        weighted_bmi = 3
    
    if  bmi >= 19: 
        weighted_bmi = 2
    
    if bmi >= 5:
        weighted_bmi = 1
    # get the prediction
    result = calculate_risk(formInfo)
    return render_to_response('templates/predictorResults.html', {'results': result}, request=req)


def get_home(req):
  return render_to_response('templates/home.html', [], request=req)

def get_form(req):
  return render_to_response('templates/riskForm.html', [], request=req)

def get_predictor_home(req):
  return render_to_response('templates/predictorHome.html', [], request=req)

def get_amazon_study(req):
  return render_to_response('templates/amazonStudy.html', [], request=req)


if __name__ == '__main__':
  
  # Configure routes and views associated with them.
  config = Configurator()

  config.include('pyramid_jinja2')
  config.add_jinja2_renderer('.html')

  config.add_route('get_home', '/')
  config.add_view(get_home, route_name='get_home')

  config.add_route('get_predictor_home', '/get_predictor_home')
  config.add_view(get_predictor_home, route_name = 'get_predictor_home')

  config.add_route('get_amazon_study', '/get_amazon_study')
  config.add_view(get_amazon_study, route_name = 'get_amazon_study')



  config.add_route('get_form', '/get_form')
  config.add_view(get_form, route_name = 'get_form')

  config.add_route('receive_form', '/receive_form')
  config.add_view(receive_form, route_name ='receive_form')


  config.add_static_view(name='/', path='./public', cache_max_age=3600)

  app = config.make_wsgi_app()
  serve(app, host ="0.0.0.0", port =6000)
