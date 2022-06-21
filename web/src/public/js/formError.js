document.addEventListener('DOMContentLoaded', () => {
  
    let homeBtn = document.querySelector(".container2");
       homeBtn.addEventListener("click", () => {   let theUrl = '/get_interact_home';
            location.href = theUrl;
        });
      
    let theReturnBtn = document.querySelector(".returnBtn"); 
  theReturnBtn.addEventListener("click", () => { let theUrl = '/get_register';
          location.href = theUrl;
        }); 
    
    
    
    });