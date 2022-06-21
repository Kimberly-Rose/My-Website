
document.addEventListener('DOMContentLoaded', () => {

  let homeBtn = document.querySelector(".container2");
  homeBtn.addEventListener("click", () => {   let theUrl = '/get_interact_home';
       location.href = theUrl;
   });

});