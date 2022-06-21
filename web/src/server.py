from pyramid.config import Configurator
from pyramid.renderers import render_to_response
from pyramid.response import Response
import os
from waitress import serve
import pandas as pd
import pickle
from sklearn import preprocessing
import mysql.connector as mysql

db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
db_host = os.environ['MYSQL_HOST']

# -------FUNCTIONS FOR INTERACT LIVE--------------------------------------------------------------------------------------------------------#

'''
This function ensures form data for new toy owners is valid by making
sure the input is valid and the email address doesn't already exist
in the database. Email address is used to distinguish an owner since
it is common for people to share names, but not possible for them
to share email addresses 
'''
def validate_new_owner_form(aForm):
    if (not aForm.get('first_name').isalpha() or not aForm.get('last_name').isalpha()):
        return False
    if (aForm.get('user_name').find("\\") != -1 or aForm.get('user_name').find("/") != -1):
        return False
    if (aForm.get('password').find("\\") != -1 or aForm.get('password').find("/") != -1):
        return False

    try:
        db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
        cursor = db.cursor()
        cursor.execute("select exists(select * from Owners where email = %s)", (aForm.get('email'),))
        theResult = cursor.fetchone()
        db.close()
        return False if theResult[0] != 0 else True

    except:
        return False

'''
This function ensures a valid email is provided for an existing owner
'''
def validateEmail(anEmail):
    try:
        db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
        cursor = db.cursor()
        cursor.execute("select exists(select * from Owners where email = %s)", (anEmail,))
        theResult = cursor.fetchone()
        db.close()
        return True if theResult[0] != 0 else False

    except:
        return False

'''
This function ensures the provided password matches the one
in the database associated with the provided email address
for a toy owner
'''
def validateOwner(anEmail, aPassword):
    theResult = validateEmail(anEmail)

    if theResult:
        db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
        cursor = db.cursor()
        cursor.execute("select password from Owners where email = %s", (anEmail,))
        theData = cursor.fetchone()
        db.close()
        return True if theData[0] == aPassword else False
    return False

'''
This function checks to see if a toy is setup and ready to accept donations
'''
def toyStatusDonators(anID):
    try:
        db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
        cursor = db.cursor()
        cursor.execute("select live from Toys where toyID = %s", (anID,))
        theStatus = cursor.fetchone()

        if (theStatus[0] == 0):
            db.close()
            return False, None

        if (theStatus[0] == 1):
            cursor.execute("select name from Toys where toyID = %s", (anID,))
            theName = cursor.fetchone()
            db.close()
            return True, theName[0]
    except:
        return False, None

'''
This function adds a new toy owner to the database 
'''
def addOwner(aForm):
    db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
    cursor = db.cursor()
    query = "insert into Owners (first_name, last_name, user_name, email, password) values (%s, %s, %s, %s, %s)"
    values = (
        aForm.get('first_name'), aForm.get('last_name'), aForm.get('user_name'), aForm.get('email'),
        aForm.get('password'))
    cursor.execute(query, values)
    db.commit()
    db.close()

'''
This function checks to see if a toy name exists
'''
def toyNameExists(aName):
    db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
    cursor = db.cursor()
    cursor.execute("select exists(select * from Toys where name = %s)", (aName,))
    theResult = cursor.fetchone()
    db.close()
    return True if theResult[0] != 0 else False

'''
This function registers a toy by entering it into the database if
a toy with that id does not already exist.
'''
def registerToy(aName, anId):
    try:
        db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
        cursor = db.cursor()
        cursor.execute("select exists(select * from Toys where toyID = %s)", (anId,))
        theResult = cursor.fetchone()

        if theResult[0] != 0:
            return False

        else:
            query = "insert into Toys (toyID, name) values (%s, %s)"
            values = (anId, aName)
            cursor.execute(query, values)
            db.commit()
            return True

    except:
        return False

'''
This function sets a donation goal for a toy
'''
def setGoal(aName, aGoal):
    try:
        db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
        cursor = db.cursor()
        cursor.execute("update Toys set goal = %s where name = %s", (aGoal, aName,))
        cursor.execute("update Toys set live = true where name = %s", (aName,))
        cursor.execute("update Toys set donations = 0 where name = %s", (aName,))
        db.commit()
        return True

    except:
        return False

'''
This function adds a donation amount to the donation goal of a toy, 
updates its status, and returns the status along with a remainder
value if the last donation exceeded the donation goal
'''
def donate(aToyId, anAmount):
    db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
    cursor = db.cursor()
    cursor.execute("select donations, goal from Toys where toyID = %s", (aToyId,))
    theResult = cursor.fetchone()
    currentDonationAmt = int(theResult[0])
    theGoal = int(theResult[1])

    if theGoal == currentDonationAmt:
        theStatus = dict([('donations', theResult[0]), ('goal', theResult[1])])
        return theStatus

    newDonationAmount = int(anAmount) + currentDonationAmt
    remainder = 0

    if newDonationAmount < theGoal:
        cursor.execute("update Toys set donations = %s where toyID = %s", (newDonationAmount, aToyId,))
        db.commit()

    if newDonationAmount == theGoal:
        cursor.execute("update Toys set donations = %s where toyID = %s", (theGoal, aToyId,))
        cursor.execute("update Toys set live = false where toyID = %s", (aToyId,))
        cursor.execute("update Toys set interact = true where toyID = %s", (aToyId,))
        db.commit()

    if newDonationAmount > theGoal:
        remainder = theGoal - newDonationAmount
        cursor.execute("update Toys set donations = %s where toyID = %s", (theGoal, aToyId,))
        cursor.execute("update Toys set live = false where toyID = %s", (aToyId,))
        cursor.execute("update Toys set interact = true where toyID = %s", (aToyId,))
        db.commit()

    cursor.execute("select donations, goal from Toys where toyID = %s", (aToyId,))
    theResult = cursor.fetchone()
    finalResult = dict([('donations', theResult[0]), ('goal', theResult[1])])
    finalResult['remainder'] = remainder
    db.close()
    return finalResult

'''
This function is for use with arduino/device and it 
checks if the toy is ready to activate
'''
def toyStatus(anID):
    try:
        db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
        cursor = db.cursor()
        cursor.execute("select interact from Toys where toyID = %s", (anID,))
        theStatus = cursor.fetchone()

        if (theStatus[0] == 1):
            cursor.execute("update Toys set interact = false where toyID = %s", (anID,))
            db.commit()
            db.close()
            return True
        else:
            db.close()
            return False

    except:
        return False

'''
This function accepts a request to reset the interact live demo, this drops and recreates
the "Owners" and "Toys" tables to ensure that the demo toy IDs 1402 and 1403 are available
for the user.
'''
def reset_interact(req):
    try:
        db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
        cursor = db.cursor()
        cursor.execute("drop table if exists Toys;")
        cursor.execute("drop table if exists Owners;")

        # close db since init_db will open it
        db.close()
        exec(open("init_db.py").read())
        return {"status": "interact demo reset"}

    except:
        return {"status": "error"}

'''
This function accepts a request containing form data for a new owner and adds the new owner
to the database if the information is valid. An appropriate view is returned
'''
def register_owner(req):
    fields = ["first_name", "last_name", "user_name", "email", "password", "password_repeat", "remember"]
    formInfo = req.POST.mixed()
    if formInfo['password'] == formInfo['password_repeat']:
        if sorted(fields) == sorted(list(formInfo.keys())):
            formInfo.pop('password_repeat')
            formInfo.pop('remember')
            if validate_new_owner_form(formInfo) == True:
                addOwner(formInfo)
                return render_to_response('templates/setupToys.html', [], request=req)
    return render_to_response('templates/formError.html', [], request=req)

'''
This function accepts a request containing an existing owner's email and password
and it returns the setupToys view if the provided information is valid. 
'''
def get_owner(req):
    formInfo = req.POST.mixed()
    theEmail = formInfo.get('text2')
    thePassword = formInfo.get('password2')
    theResult = validateOwner(theEmail, thePassword)

    return render_to_response('templates/setupToys.html', [], request=req) if theResult is True \
        else render_to_response('templates/formError.html', [], request=req)

'''
This function accepts a request containing a toy id and an amount to donate
to the toy. It then calls donate() to handle adding the amount if the goal
has not been met. donate() returns the goal amount and the amount collected
which is returned to the front end to update the status bar on the toy page.
A remainder is also returned from donate() which would serve to refund a donor
any amount that went over the goal.
'''
def add_donation_route(req):
    toyId = req.matchdict.get('toyId')
    donation = req.matchdict.get('donation')
    theResult = donate(toyId, donation)

    if "remainder" in theResult:
        theResult.pop('remainder')

    return theResult

'''
This function accepts a request containing a name the owner would like to assign to a toy.
This is to aid the owner in selecting a name which is not taken before registering the toy.
toyNameExists() is called to check availability and the status is returned to the owner
'''
def check_toy_name(req):
    name = req.text
    if name.find("\\") != -1 or name.find("/") != -1:
        theResponse = {"status": "invalid characters, please try a different name"}
        return theResponse
    theResult = toyNameExists(name)

    if not theResult:
        theResponse = {"status": "That name is available"}
        return theResponse

    if theResult:
        theResponse = {"status": "Sorry, that name is taken"}
        return theResponse

'''
This function accepts a request containing a toy id and toy name choice 
and it calls registerToy() to assign the name to the provided toy id if the name
is available. The status is returned to the owner (front end)
'''
def register_toy(req):
    theInfo = req.POST.mixed()
    theName = theInfo.get('nameChoice')
    theId = int(theInfo.get('toyID'))

    if theName.find("\\") != -1 or theName.find("/") != -1:
        theResponse = {"status": "invalid characters, please try a different name"}
        return theResponse

    if not isinstance(theId, int):
        theResponse = {"status": "Error. Toy ID should be an integer value"}
        return theResponse

    theResult = toyNameExists(theName)
    if theResult:
        theResponse = {"status": "Sorry, that name is taken"}
        return theResponse

    theResult = registerToy(theName, theId)
    theResponse = {"status": "Your toy has been successfully registered!"} if theResult is True \
        else {"status": "Error registering toy, please try again"}

    return theResponse

'''
This function accepts a request containing a owner provided toy name and donation goal.
If the information is valid, setGoal() is called to assign the goal amount to the toy
The status is returned to the owner (front end).
'''
def set_toy_goal(req):
    theInfo = req.POST.mixed()
    name = theInfo.get('name')
    goal = int(theInfo.get('goal'))

    if name.find("\\") != -1 or name.find("/") != -1:
        theResponse = {"status": "invalid characters, please try a different name"}
        return theResponse

    if not isinstance(goal, int):
        theResponse = {"status": "Error. The donation goal should be a whole number value"}
        return theResponse

    theResult = toyNameExists(name)
    if not theResult:
        theResponse = {"status": "Sorry, no toy with that name was found."}
        return theResponse

    theResult = setGoal(name, goal)
    theResponse = {"status": "Sorry there was an error submitting the goal. Please try again"} if not theResult\
        else {"status": "Goal successfully submitted!"}

    return theResponse

'''
This request accepts a link to a toy, provided by the user/donor, and returns the 
view associated with the toy if it is available to accept donations
'''
def get_toy_interact(req):
    theInfo = req.POST.mixed()
    theToyId = int(theInfo.get('link'))
    theStatus, theToyName = toyStatusDonators(theToyId)

    if theStatus:
        theToyImage = 'toyImages/' + str(theToyId) + '.jpg'
        return render_to_response('templates/interact.html', {'theToyName': str(theToyName), 'theToyId': int(theToyId),
                                                              'theToyImg': str(theToyImage)}, request=req)
    else:
        return render_to_response('templates/inactiveToyError.html', [], request=req)

'''
This request is from the arduino/physical device. It accepts the toy id
and returns a boolean value indicating whether or not the toy is ready
to activate
'''
def getDonationStatus(req):
    page_data = req.GET.mixed()
    toyId = int(page_data['id'])
    theStatus = toyStatus(toyId)
    return Response(str(1)) if theStatus else Response(str(0))
# ---------------------------------------------------------------------------------------------------------------------------------------------#

# -------FUNCTIONS FOR DIABETES PREDICTOR------------------------------------------------------------------------------------------------------#

def normalization(df):
    '''
    Author: Derek Chen
    Normalize the input data frame
    df(data frame): data frame that has the label as last coloumn
    df_n(data frame): a normalization of the input df
    '''
    x = df[df.columns].values
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x.T)
    df_n = pd.DataFrame(x_scaled.T, columns=df[df.columns].columns)
    return df_n

def get_weighted_bmi(bmi):
    '''
    Author: Derek Chen
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

    if bmi in range(19, 25):
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

    # normalize the row
    row = normalization(df)

    # get prediction
    model = pickle.load(open('finalized_model.sav', 'rb'))
    x = row[row.columns].to_numpy()
    y = model.predict(x)[0]

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
    sortedColumns = sorted(list(formInfo.keys()))
    assert sortedFields == sortedColumns, "ERROR fields from POST do not match columns"

    # calculate BMI and remove the BMI variables of feet, inches, pounds
    feet = formInfo.pop('feet').strip()
    inches = formInfo.pop('inches').strip()
    weight = formInfo.pop('pounds').strip()
    assert all(
        [feet.isnumeric(), inches.isnumeric(), weight.isnumeric()]), "ERROR invalid values for feet,inches,pounds"

    # convert feet and inches to inches
    total_inches = (int(feet) * 12) + int(inches)

    # use formula for BMI
    bmi = int(703 * ((int(weight)) / (total_inches * total_inches)))
    weighted_bmi = get_weighted_bmi(bmi)

    # add bmi to formInfo
    formInfo['BMI'] = weighted_bmi

    # get the prediction
    result = calculate_risk(formInfo)
    return render_to_response('templates/predictorResults.html', {'results': result}, request=req)
# ---------------------------------------------------------------------------------------------------------------------------------------------#

def get_home(req):
    return render_to_response('templates/home.html', [], request=req)

def get_about_me(req):
    return render_to_response('templates/aboutMe.html', [], request=req)

def get_form(req):
    return render_to_response('templates/riskForm.html', [], request=req)

def get_predictor_home(req):
    return render_to_response('templates/predictorHome.html', [], request=req)

def get_my_database(req):
    return render_to_response('templates/myDatabase.html', [], request=req)

def get_amazon_study(req):
    return render_to_response('templates/amazonStudy.html', [], request=req)

def get_interact_home(req):
    return render_to_response('templates/interactHome.html', [], request=req)

def get_register(req):
    return render_to_response('templates/register.html', [], request=req)

def get_shop(req):
    return render_to_response('templates/shop.html', [], request=req)

# about for interact live
def get_about(req):
    return render_to_response('templates/about.html', [], request=req)

def return_form_error(req):
    return render_to_response('templates/formError.html', [], request=req)

def toy_setup(req):
    return render_to_response('templates/setupToys.html', [], request=req)

def toy_error(req):
    return render_to_response('templates/inactiveToyError.html', [], request=req)

def get_donation_setup(req):
    return render_to_response('templates/getToy.html', [], request=req)

if __name__ == '__main__':
    # Configure routes and views associated with them.
    config = Configurator()

    config.include('pyramid_jinja2')
    config.add_jinja2_renderer('.html')

    config.add_route('get_home', '/')
    config.add_view(get_home, route_name='get_home')

    config.add_route('get_about_me', '/get_about_me')
    config.add_view(get_about_me, route_name='get_about_me')

    config.add_route('get_predictor_home', '/get_predictor_home')
    config.add_view(get_predictor_home, route_name='get_predictor_home')

    config.add_route('get_my_database', '/get_my_database')
    config.add_view(get_my_database, route_name='get_my_database')

    config.add_route('get_amazon_study', '/get_amazon_study')
    config.add_view(get_amazon_study, route_name='get_amazon_study')

    config.add_route('get_form', '/get_form')
    config.add_view(get_form, route_name='get_form')

    config.add_route('receive_form', '/receive_form')
    config.add_view(receive_form, route_name='receive_form')

    config.add_route('get_interact_home', '/get_interact_home')
    config.add_view(get_interact_home, route_name='get_interact_home')

    config.add_route('get_register', '/get_register')
    config.add_view(get_register, route_name='get_register')

    config.add_route('get_shop', '/get_shop')
    config.add_view(get_shop, route_name='get_shop')

    config.add_route('get_about', '/get_about')
    config.add_view(get_about, route_name='get_about')

    config.add_route('reset_interact', '/reset_interact')
    config.add_view(reset_interact, route_name='reset_interact', renderer='json')

    config.add_route('get_donation_setup', '/get_donation_setup')
    config.add_view(get_donation_setup, route_name='get_donation_setup')

    config.add_route('toy_setup', '/toy_setup')
    config.add_view(toy_setup, route_name='toy_setup')

    config.add_route('return_form_error', '/return_form_error')
    config.add_view(return_form_error, route_name='return_form_error')

    config.add_route('register_owner', '/register_owner')
    config.add_view(register_owner, route_name='register_owner', request_method='POST')

    config.add_route('get_owner', '/get_owner')
    config.add_view(get_owner, route_name='get_owner', request_method='POST')

    config.add_route('get_toy_interact', '/get_toy_interact')
    config.add_view(get_toy_interact, route_name='get_toy_interact')

    config.add_route('add_donation', '/add_donation/{toyId}/{donation}')
    config.add_view(add_donation_route, route_name='add_donation', renderer='json')

    config.add_route('check_toy_name', '/check_toy_name')
    config.add_view(check_toy_name, route_name='check_toy_name', renderer='json')

    config.add_route('register_toy', '/register_toy')
    config.add_view(register_toy, route_name='register_toy', renderer='json')

    config.add_route('set_toy_goal', '/set_toy_goal')
    config.add_view(set_toy_goal, route_name='set_toy_goal', renderer='json')

    config.add_route('getDonationStatus', '/getDonationStatus')
    config.add_view(getDonationStatus, route_name='getDonationStatus', request_method='GET')

    config.add_static_view(name='/', path='./public', cache_max_age=3600)

    app = config.make_wsgi_app()
    serve(app, host="0.0.0.0", threads=6, port=6000)
