function showTable(evt, table) {
    // Declare all variables
    var i, container, tablinks;
    console.log('OD');
    console.log(table);
    if (table == 'live-invoices') {
        console.log('if');
        document.getElementById('financed-invoices').style.display = "none";
        document.getElementById('live-invoices').style.display = "block";
        document.getElementById('btn1').style.color = "#4CAF50";
        document.getElementById('btn1').style.borderBottom = "3px solid #4CAF50";
        document.getElementById('btn2').style.color = "#AAAAAA";
        document.getElementById('btn2').style.borderBottom = "3px solid #AAAAAA";
    } else if (table == 'financed-invoices') {
        document.getElementById('live-invoices').style.display = "none";
        document.getElementById('financed-invoices').style.display = "block";
        document.getElementById('btn1').style.borderBottom = "3px solid #AAAAAA";
        document.getElementById('btn1').style.color = "#AAAAAA";
        document.getElementById('btn2').style.color = "#4CAF50";
        document.getElementById('btn2').style.borderBottom = "3px solid #4CAF50";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    evt.currentTarget.className += " active";
}