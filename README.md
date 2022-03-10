# **README**


### **FINAL UPDATE**
#### Categorized BMI has helped with normalization when using only 1 row
#### and the model now works as expected and aesthetics are complete with
#### a home page, form page, and results page

### **UPDATE**
#### Aesthetics are finished, results are properly displayed,
#### home page has been improved, navigation works properly
#### between home page, form, and results page. Results page
#### was added to clearly display results and give the option
#### to return home or fill out form again

### **STILL NEEDS IMPROVEMENT**
#### There has been a lot of issues getting the row properly
#### normalized for the model, The problem persists and results
#### are still not as expected. Normalized row does not contain
#### values similar to original normalized data. If troubles persist
#### it may be necessary to load the whole data set. Derek is
#### currently investigating the issue.

### **Current Progress** 
#### This program creates a website inside of a docker container with
#### a pyramid 2.0 waitress backend and very basic HTML and CSS on the pages.
#### The website is containerized for deployment to the cloud.
#### To run the container, install Docker and run docker-compose up --build
#### from the command line in the directory. Once the container is
#### running, open a browser (use incognito if you have Chrome) and type
#### in 'localhost' to view the website on your computer. There is 
#### a very basic home screen with a button that links to a form.
#### The form has radio boxes to select choices and a few text fields
#### for collecting information. Once it is submitted, javascript is
#### used to post the data to the backend. At the backend the info
#### is parsed from the form, the BMI is calculated from provided
#### measurements, a dataframe is constructed from the values, and
#### the model is loaded from a file to predict the result. Once the
#### result is determined, it is sent back to the front end for display.

### **TO DO before presentation
#### 1. I need to make the pages nicer.
#### 2. Currently the result message appears as a response window
####    and all attempts to inject it in to the page where it belongs
####    have not worked yet.
#### 3  I need to refresh the page after a form submit.
#### 4. The code for using the model should be checked to ensure
####    I have used it properly because it seems impossible to get
####    a value other than 0.