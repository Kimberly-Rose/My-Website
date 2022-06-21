document.addEventListener('DOMContentLoaded', () => {
 
  let homeBtn = document.querySelector(".container");
  homeBtn.addEventListener("click", () => {   let theUrl = '/get_interact_home';
       location.href = theUrl;
   });
  
  
 let newToyBtn= document.querySelector('.toys1');
 newToyBtn.classList.add("toys1ON");
 newToyBtn.classList.toggle("toys1ON"); 
 
 let existToyBtn= document.querySelector('.toys2');
 existToyBtn.classList.add("toys2ON");
 existToyBtn.classList.toggle("toys2ON"); 
 
 var form1 = document.getElementById("interactive1");
 var form1a = document.getElementById("interactive1a");
 var form2 = document.getElementById("interactive2");
 
 function displayNewToyForm() {
   if (form2.style.display === "block") {
       existToyBtn.classList.toggle("toys2ON"); 
       form2.style.display = "none";
   }
    
   if (form1.style.display === "none" && form1a.style.display === "none") {
      newToyBtn.classList.toggle("toys1ON"); 
      form1.style.display = "block";
      form1a.style.display = "block";
    } 
    else {
      newToyBtn.classList.toggle("toys1ON"); 
      form1.style.display = "none";
      form1a.style.display = "none";
    }
  }
  
  function displayExistingToyForm(){
    if (form1.style.display === "block" && form1a.style.display === "block") {
       newToyBtn.classList.toggle("toys1ON"); 
       form1.style.display = "none";
       form1a.style.display = "none";
   }
    
   if (form2.style.display === "none") {
      existToyBtn.classList.toggle("toys2ON"); 
      form2.style.display = "block";
    } 
    else {
      existToyBtn.classList.toggle("toys2ON"); 
      form2.style.display = "none";
    }
  }
   newToyBtn.addEventListener("click", displayNewToyForm); 
   existToyBtn.addEventListener("click", displayExistingToyForm);
  
   let checkNameBtn = document.querySelector(".checkBtn");
   checkNameBtn.addEventListener('click', function() {
     let theName = document.getElementById('checkName').value;
     let theURL = '/check_toy_name';
       fetch(theURL, {
         method: 'POST',
         body: theName
       })
       .then(response=>response.json())
       .then(function(response) {
         for (let key in response) {
           document.getElementById('checkResponse').innerHTML = response[key];
         }   
         });
      });
  
      /* I can be used to check FormData
       for (var pair of theRegistration.entries()) {
         console.log(pair[0]+ ', ' + pair[1]);
       }*/
     
   let submitChoiceBtn = document.querySelector(".choiceBtn");
     submitChoiceBtn.addEventListener('click', function() {
       let theChoice = document.getElementById('nameChoice').value;
       let theID = document.getElementById('toyID').value;
       let theRegistration = new FormData();
       theRegistration.append('nameChoice', theChoice);
       theRegistration.append('toyID', theID);
       var theStatus;
       let theURL = '/register_toy';
       fetch(theURL, {
         method: 'POST',
         body: theRegistration
       })
       .then(response=>response.json())
       .then(function(response) {
         for (let key in response) {
          if(key == "status") { 
           document.getElementById('registerResponse').innerHTML = response[key];
           theStatus = response[key]
          }
         }   
         });

         setTimeout(function () {
             console.log(theStatus);
            if (theStatus === "Your toy has been successfully registered!") {
                newToyBtn.classList.toggle("toys1ON");
                form1.style.display = "none";
                form1a.style.display = "none";
            }
         }, 2000);
        });
  
    let theSubmitBtn = document.querySelector('.submitBtn');
    theSubmitBtn.addEventListener("click", () => { 
    var showConfirmBtn = document.getElementById('confirm');
    var showSubmitBtn = document.getElementById('submit')

      if (showConfirmBtn.style.display == "none") {
        showConfirmBtn.style.display = "block";
        showSubmitBtn.style.display = "none";
      }
    }); 

      let confirmGoalBtn = document.querySelector(".confirmBtn");
     confirmGoalBtn.addEventListener('click', function() {
       let theName = document.getElementById('name').value;
       let theGoal = document.getElementById('goal').value;
       var theStatus;
       let theGoalForm = new FormData();
       theGoalForm.append('name', theName);
       theGoalForm.append('goal', theGoal);
       let theURL = '/set_toy_goal';
       fetch(theURL, {
         method: 'POST',
         body: theGoalForm
       })
       .then(response=>response.json())
       .then(function(response) {
         for (let key in response) {
           if(key == "status") {
           document.getElementById('donationResponse').innerHTML = response[key];
           theStatus = response[key]
           }
         }   
         });

         setTimeout(function() {

             if (theStatus === "Goal successfully submitted!") {
                 existToyBtn.classList.toggle("toys2ON");
                 form2.style.display = "none";
             }
         }, 2000);
        });






});