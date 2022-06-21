document.addEventListener('DOMContentLoaded', () => {

  let homeBtn = document.querySelector(".containerB");
  homeBtn.addEventListener("click", () => {   let theUrl = '/get_interact_home';
       location.href = theUrl;
   });
  
  let newUserBtn= document.querySelector('.users1');
 newUserBtn.classList.add("users1ON");
 newUserBtn.classList.toggle("users1ON"); 
 
 let existUserBtn= document.querySelector('.users2');
 existUserBtn.classList.add("users2ON");
 existUserBtn.classList.toggle("users2ON"); 
 
 var form1 = document.getElementById("interactive1");
 var form2 = document.getElementById("interactive2");
 
 function displayNewUserForm() {
   if (form2.style.display === "block") {
       existUserBtn.classList.toggle("users2ON"); 
       form2.style.display = "none";
   }
    
   if (form1.style.display === "none") {
      newUserBtn.classList.toggle("users1ON"); 
      form1.style.display = "block";
    } 
    else {
      newUserBtn.classList.toggle("users1ON"); 
      form1.style.display = "none";
    }
  }
  
  function displayExistingUserForm(){
    if (form1.style.display === "block") {
       newUserBtn.classList.toggle("users1ON"); 
       form1.style.display = "none";
   }
    
   if (form2.style.display === "none") {
      existUserBtn.classList.toggle("users2ON"); 
      form2.style.display = "block";
    } 
    else {
      existUserBtn.classList.toggle("users2ON"); 
      form2.style.display = "none";
    }
  }
   
  
   newUserBtn.addEventListener("click", displayNewUserForm); 
   existUserBtn.addEventListener("click", displayExistingUserForm);
  
   
   /*let submitBtn = document.getElementById("submitExist");
   submitBtn.addEventListener('click', function() {
     let theEmail = document.getElementById('text2').value;
     let thePassword = document.getElementById('password2').value;
     let getAccount = new FormData();
     getAccount.append('text2', theEmail);
     getAccount.append('password2', thePassword);
      
     
      let theURL = '/get_owner';
     fetch(theURL, {
       method: 'POST',
       body: getAccount
     })
     .then(response=>response.json())
     .then(function(response) {
      for (let key in response) {
        if(key == "status") { 
         console.log(key);
        }
      }
      });   
    });*/
   

});