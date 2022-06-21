document.addEventListener('DOMContentLoaded', () => {
  
    let homeBtn = document.querySelector(".container2");
     homeBtn.addEventListener("click", () => {   let theUrl = '/get_interact_home';
          location.href = theUrl;
      });
    
      let aboutBtn = document.querySelector(".container3");
      aboutBtn.addEventListener("click", () => {   let theUrl = '/get_about';
           location.href = theUrl;
       });
  
});