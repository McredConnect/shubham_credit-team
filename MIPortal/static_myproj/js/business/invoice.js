function showTable(evt, table) {
    // Declare all variables
    var i, container, tablinks;
    if (table == 'current-invoices') {
        document.getElementById('past-invoices').style.display = "none";
        document.getElementById('current-invoices').style.display = "block";
        document.getElementById('btn1').style.borderBottom = "3px solid #4CAF50";
        document.getElementById('btn1').style.color = "#4CAF50";
        document.getElementById('btn2').style.borderBottom = "3px solid #AAAAAA";
        document.getElementById('btn2').style.color = "#AAAAAA";
    } else if (table == 'past-invoices') {
        document.getElementById('current-invoices').style.display = "none";
        document.getElementById('past-invoices').style.display = "block";
        document.getElementById('btn1').style.borderBottom = "3px solid #AAAAAA";
        document.getElementById('btn1').style.color = "#AAAAAA";
        document.getElementById('btn2').style.borderBottom = "3px solid #4CAF50";
        document.getElementById('btn2').style.color = "#4CAF50";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    evt.currentTarget.className += " active";

}