document.addEventListener('DOMContentLoaded', () => {

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

//The worst thing ever! a block of code copied and pasted 6 times
// because I couldn't make it work any other way and time is short
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