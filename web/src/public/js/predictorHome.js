document.addEventListener('DOMContentLoaded', () => {

    let formBtn = document.getElementById('survey');
        formBtn.addEventListener("click", () => {
            let theUrl = '/get_form';
            location.href = theUrl;
       });
    
});