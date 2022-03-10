// a function to get the server response when form is sent 

function getResponse(event) {
    var theUrl = 'receive_form';
    var request = new XMLHttpRequest();
    request.open('POST', theUrl, true);
    request.onload = function() {
      console.log("success getting response");
      //console.log(request.responseText);
    };
    request.onerror = function() {
      console.log("failed to get response");
    };
    request.send(new FormData(event.target));
    event.preventDefault();
  }
  // add an event listener to detect form submission
  let theSend = document.getElementById('riskForm');
  theSend.addEventListener("submit", getResponse);






  
