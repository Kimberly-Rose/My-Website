
document.addEventListener('DOMContentLoaded', () => {

      let homeBtn = document.querySelector(".container2");
      homeBtn.addEventListener("click", () => {
          let theUrl = '/get_interact_home';
          location.href = theUrl;
       });

      let aboutBtn = document.querySelector(".options3");
      aboutBtn.addEventListener("click", () => {   
          let theUrl = '/get_about';
          location.href = theUrl;
      });

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