document.addEventListener('DOMContentLoaded', () => {
  
    let homeBtn = document.querySelector(".container2");
     homeBtn.addEventListener("click", () => {   let theUrl = '/';
          location.href = theUrl;
      });


var fillBar= document.querySelector(".progress");
let donateButton = document.querySelector(".donateBtn");
const toyId = document.getElementById("theToyId").innerHTML;

 donateButton.addEventListener('click', function() {

  donation = document.getElementById("amount").value;


 let theURL = `/add_donation/${toyId}/${donation}`;
    fetch(theURL)
      .then((response)=>response.json())
      .then(function(response) {
      var totalDonations = 0;
      var theGoal = 0;
      for (let key in response) {
        if (key === "donations"){totalDonations = response["donations"];}
        if (key === "goal"){theGoal = response["goal"];}
        document.getElementById(key).innerHTML = response[key];
      }
      fillBar.style.width = `${(totalDonations/theGoal)*100}%`;
     });
  
 });
  
});