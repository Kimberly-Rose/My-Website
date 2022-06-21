document.addEventListener('DOMContentLoaded', () => {
   let readMoreBtn = document.querySelector(".readMore");
   let readLessBtn = document.querySelector(".readLess");
   let infoDisplay = document.getElementById("moreInfo");
   let showDemoBtn = document.querySelector(".showDemo");
   let hideDemoBtn = document.querySelector(".hideDemo");
   let demoDisplay = document.querySelector(".demo");


   readMoreBtn.addEventListener("click", function () {
      readMoreBtn.style.display = "none";
      readLessBtn.style.display = "block";
      infoDisplay.style.display = "block";
   });

  readLessBtn.addEventListener("click", function () {
      readLessBtn.style.display = "none";
      readMoreBtn.style.display = "block";
      infoDisplay.style.display = "none";
   });

   showDemoBtn.addEventListener("click", function () {
      showDemoBtn.style.display = "none";
      hideDemoBtn.style.display = "block";
      demoDisplay.style.display = "block";
   });

  hideDemoBtn.addEventListener("click", function () {
      hideDemoBtn.style.display = "none";
      showDemoBtn.style.display = "block";
      demoDisplay.style.display = "none";
   });

    let sballOn = document.querySelector('.sball');
    sballOn.classList.add("ballON");
    sballOn.classList.toggle("ballON");

    let iballOn = document.querySelector('.iball');
    iballOn.classList.add("ballON");
    iballOn.classList.toggle("ballON");

    let rballOn = document.querySelector('.rball');
    rballOn.classList.add("ballON");
    rballOn.classList.toggle("ballON");

    let aballOn = document.querySelector('.aball');
    aballOn.classList.add("ballON");
    aballOn.classList.toggle("ballON");

    let registerBtn = document.getElementById('register');
    registerBtn.addEventListener("click", function () {
        rballOn.classList.toggle("ballON");
        let theUrl = '/get_register';
        location.href = theUrl;
    });

    let shopBtn = document.getElementById('shop');
    shopBtn.addEventListener("click", function () {
        sballOn.classList.toggle("ballON");
        let theUrl = '/get_shop';
        location.href = theUrl;
    });

     let resetBtn = document.getElementById('reset');
    resetBtn.addEventListener("click", function () {
        aballOn.classList.toggle("ballON");
        let theUrl = '/reset_interact';
         fetch(theUrl)
        .then(response=>response.json())
        .then(function(response) {
        console.log(response);
          });
         aballOn.classList.toggle("ballON");
    });

    let interactBtn = document.getElementById('interact');
    interactBtn.addEventListener("click", function () {
        iballOn.classList.toggle("ballON");
        let theUrl = '/get_donation_setup';
        location.href = theUrl;
    });


    let aboutBtn = document.querySelector(".container3");
    aboutBtn.addEventListener("click", () => {   let theUrl = '/get_about';
         location.href = theUrl;
     });















});