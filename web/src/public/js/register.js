document.addEventListener('DOMContentLoaded', () => {

  let homeBtn = document.querySelector(".containerB");
  homeBtn.addEventListener("click", () => {
       let theUrl = '/get_interact_home';
       location.href = theUrl;
   });

   let aboutBtn = document.querySelector(".options3");
   aboutBtn.addEventListener("click", () => {   let theUrl = '/get_about';
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

       let resumeBtn = document.getElementById("resumeLabel");
       let projectBtn = document.getElementById("projectsLabel");
       let resumeMenu = document.getElementById("resumeMenu");
       let projectMenu = document.getElementById("projectsMenu");

       resumeBtn.addEventListener("click", function () {
           if (resumeMenu.style.display === "none") {
               resumeMenu.style.display = "block";
           }
           else {
               resumeMenu.style.display = "none";
           }
        });

       projectBtn.addEventListener("click", function () {
           if (projectMenu.style.display === "none") {
               projectMenu.style.display = "block";
           }
           else {
               projectMenu.style.display = "none";
           }
       });
  
});