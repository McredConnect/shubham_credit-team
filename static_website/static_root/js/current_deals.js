window.onbeforeunload = function () {
  window.scrollTo(0, 0);
}

function openDetails(event, Details) {
  // Declare all variables
  var i, container, tablinks;

  // Get all elements with class="tabcontent" and hide them
  container = document.getElementsByClassName("tabcontent");
  for (i = 0; i < container.length; i++) {
    container[i].style.display = "none";
  }

  // Get all elements with class="tablinks" and remove the class "active"
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  // Show the current tab, and add an "active" class to the button that opened the tab
  document.getElementById(Deals).style.display = "block";
  evt.currentTarget.className += " active";

}