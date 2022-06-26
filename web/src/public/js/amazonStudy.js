document.addEventListener('DOMContentLoaded', () => {
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

   var filtersMenu = document.getElementById('filters');
var climatePledgeMenu = document.getElementById('certifications');
var showClimateResults = document.getElementById('climateResultsBtn');
var showFilterResults = document.getElementById('filterResultsBtn');
var activeIcons = 0;

document.getElementById('mainFilterBtn').addEventListener('click', function()  {
   filtersMenu.style.display = "block";
});

document.getElementById('closeFilters').addEventListener('click', function()  {
   filtersMenu.style.display = "none";
});

document.getElementById('climate').addEventListener('click', function()  {
   climatePledgeMenu.style.display= "block";
   filtersMenu.style.display= "none";
});

document.getElementById('backToFilters').addEventListener('click', function()  {
  filtersMenu.style.display= "block";
  climatePledgeMenu.style.display= "none";
  if (activeIcons > 0) {
    document.getElementById('climate').classList.remove('selection');
    document.getElementById('climate').classList.add('selectionON');
    showFilterResults.style.display = "block";
  }

  else {
     if (document.getElementById('climate').classList.contains('selectionON')) {
         document.getElementById('climate').classList.remove('selectionON');
         document.getElementById('climate').classList.add('selection');
         showFilterResults.style.display = "none";
     }
  }
});

document.getElementById('carbonNeutral').addEventListener('click', function()  {
  if (this.classList.contains('logoBox')) {
    this.classList.remove('logoBox');
    this.classList.add('logoBoxON');
    activeIcons += 1;
    showClimateResults.style.display = "block";
  }
  else {
    this.classList.remove('logoBoxON');
    this.classList.add('logoBox');
    activeIcons -= 1;
    if (activeIcons < 1) {
      showClimateResults.style.display = "none";
    }
  }
});

document.getElementById('carbonFree').addEventListener('click', function()  {
  if (this.classList.contains('logoBox')) {
    this.classList.remove('logoBox');
    this.classList.add('logoBoxON');
    activeIcons += 1;
    showClimateResults.style.display = "block";
  }
  else {
    this.classList.remove('logoBoxON');
    this.classList.add('logoBox');
    activeIcons -= 1;
    if (activeIcons < 1) {
      showClimateResults.style.display = "none";
    }
  }
});

document.getElementById('compactDesign').addEventListener('click', function()  {
  if (this.classList.contains('logoBox')) {
    this.classList.remove('logoBox');
    this.classList.add('logoBoxON');
    activeIcons += 1;
    showClimateResults.style.display = "block";
  }
  else {
    this.classList.remove('logoBoxON');
    this.classList.add('logoBox');
    activeIcons -= 1;
    if (activeIcons < 1) {
      showClimateResults.style.display = "none";
    }
  }
});

document.getElementById('climatePartner').addEventListener('click', function()  {
  if (this.classList.contains('logoBox')) {
    this.classList.remove('logoBox');
    this.classList.add('logoBoxON');
    activeIcons += 1;
    showClimateResults.style.display = "block";
  }
  else {
    this.classList.remove('logoBoxON');
    this.classList.add('logoBox');
    activeIcons -= 1;
    if (activeIcons < 1) {
      showClimateResults.style.display = "none";
    }
  }
});

document.getElementById('organic').addEventListener('click', function()  {
  if (this.classList.contains('logoBox')) {
    this.classList.remove('logoBox');
    this.classList.add('logoBoxON');
    activeIcons += 1;
    showClimateResults.style.display = "block";
  }
  else {
    this.classList.remove('logoBoxON');
    this.classList.add('logoBox');
    activeIcons -= 1;
    if (activeIcons < 1) {
      showClimateResults.style.display = "none";
    }
  }
});

document.getElementById('ewg').addEventListener('click', function()  {
  if (this.classList.contains('logoBox')) {
    this.classList.remove('logoBox');
    this.classList.add('logoBoxON');
    activeIcons += 1;
    showClimateResults.style.display = "block";
  }
  else {
    this.classList.remove('logoBoxON');
    this.classList.add('logoBox');
    activeIcons -= 1;
    if (activeIcons < 1) {
      showClimateResults.style.display = "none";
    }
  }
});




});