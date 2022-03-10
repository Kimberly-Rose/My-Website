document.addEventListener('DOMContentLoaded', () => {

    let surveyBtn = document.getElementById('survey');
        surveyBtn.addEventListener("click", () => {
            let theUrl = '/get_form';
            location.href = theUrl;
       });
      
     let mainBtn = document.getElementById('main');
        mainBtn.addEventListener("click", () => {
            let theUrl = '/get_predictor_home';
            location.href = theUrl;
       });
    
    
    
    });