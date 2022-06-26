
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






  
