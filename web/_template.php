<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
<style>
* {box-sizing: border-box}

/* Set height of body and the document to 100% */
body, html {
    height: 100%;
    margin: 0;
    font-family: Arial;
    font-size: 102%;
}

/* Style tab links */
.tablink {
    background-color: #555;
    color: white;
    float: left;
    border: none;
    outline: none;
    cursor: pointer;
    padding: 14px 16px;
    font-size: 17px;
    width: 25%;
}

.tablink:hover {
    background-color: #808080;
}

/* Style the tab content (and add height:100% for full page content) */
.tabcontent {
    color: black;
    display: none;
    padding: 75px 20px;
    height: 100%;
}

#HAC 1 {background-color: white;}
#HAC 2 {background-color: white;}
#HAC 4 {background-color: white;}
#HAC 5 {background-color: white;}

/*style for search bar*/
input {
  background-image: url('css/searchicon.png');
  background-position: 5px 5px;
  background-repeat: no-repeat;
  width: 25%;
  font-size: 15px;
  padding: 12px 20px 12px 40px;
  border: 1px solid #cccccc;
  margin-bottom: 12px;
}

table {
  border-collapse: collapse;
  width: 50%;
  border: 2px solid #cccccc;
  font-size: 22px;
  padding: 3px 3px 3px 3px;
}

table th {
  border: 2px solid #cccccc;
  width: 50%;
  font-size: 20px;
  padding: 12px;
}

table td {
  border: 2px solid #cccccc;
  font-size: 16px;
  padding: 6px;
}

table tr {
  border-bottom: 2px solid #cccccc;
  padding: 2px;
}

table tr.header, tr:hover * {
    font-weight: bold;
    background-color: #fdfdfd;
}

</style>
<body onmousemove = "reload()" onClick = "reload()" onkeypress="reload()" onLoad = "reload()" >
<title>HAC Regression Run Portal</title>
<button class="tablink" onclick="openPage('HAC 1', this, '#1a53ff')" id="defaultOpen">HAC 1 - Classic SD</button>
<button class="tablink" onclick="openPage('HAC 2', this, '#1a53ff')">HAC 2 - HiOS SD</button>
<button class="tablink" onclick="openPage('HAC 4', this, '#1a53ff')">HAC 4 - HiOS MD</button>
<button class="tablink" onclick="openPage('HAC 5', this, '#1a53ff')">HAC 5 - Classic MD</button>

<div id="HAC 1" class="tabcontent">
<?php
include 'create_html_page.php';
create_page('10.2.36.251', '/root/Project/Reports/', 'hac1');
?>
</div>

<div id="HAC 2" class="tabcontent">
<?php
create_page('10.2.36.240', '/root/hacpy/logs/', 'hac2');
?>
</div>

<div id="HAC 4" class="tabcontent">
<?php
create_page('10.2.36.212', '/mnt/sda3/Project/Reports/', 'hac4');
?>
</div>

<div id="HAC 5" class="tabcontent">
<?php
create_page('10.2.36.211', '/root/Project/Reports/', 'hac5');
?>
</div>

<script>
function openPage(pageName,elmnt,color) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablink");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].style.backgroundColor = "";
    }
    document.getElementById(pageName).style.display = "block";
    elmnt.style.backgroundColor = color;

}
// Get the element with id="defaultOpen" and click on it
document.getElementById("defaultOpen").click();

function mySearch(tb, col, col2, name) {
  var input, input2, filter, filter2, tr, td, td2, table;
  var neg1, neg2;
  input = document.getElementById(col);
  input2 = document.getElementById(col2);
  filter = input.value.toUpperCase();
  filter2 = input2.value.toUpperCase();
  if (input.value.charAt(0)=="!")
    {   neg1=true;
        filter=filter.substring(1);
    }
  if (input2.value.charAt(0)=="!")
    {   neg2=true;
        filter2=filter2.substring(1);
    }

  var counter = 0;
  table = document.getElementById(tb);
  tr = table.getElementsByTagName("tr");
  for (i = 0; i < tr.length; i++)
  {
    td = tr[i].getElementsByTagName("td")[0];
    td2 = tr[i].getElementsByTagName("td")[1];
    if (td)
    {
        if(neg1){
            if(neg2){

                if (td.innerHTML.toUpperCase().indexOf(filter) == -1 && td2.innerHTML.toUpperCase().indexOf(filter2) == -1)
                    {   tr[i].style.display = "";
                        counter += 1;}
                else
                    {   tr[i].style.display = "none";}
                    }
            else{

                if (td.innerHTML.toUpperCase().indexOf(filter) == -1 && td2.innerHTML.toUpperCase().indexOf(filter2) > -1)
                    {   tr[i].style.display = "";
                        counter += 1;}
                else
                    {   tr[i].style.display = "none";}
                }
                 }
        else if(neg2&& !neg1){
            if (td.innerHTML.toUpperCase().indexOf(filter) > -1 && td2.innerHTML.toUpperCase().indexOf(filter2) == -1)
                {   tr[i].style.display = "";
                    counter += 1;}
            else
                {   tr[i].style.display = "none";}
                     }
        else{
        if (td.innerHTML.toUpperCase().indexOf(filter) > -1 && td2.innerHTML.toUpperCase().indexOf(filter2) > -1)
        {   tr[i].style.display = "";
            counter +=1;}
        else
        {   tr[i].style.display = "none";}
            }
    }
    document.getElementById(name).innerHTML = "Filtered test cases: " + counter;
  }
}

var tmp;

function reload(){
    clearTimeout(tmp);
    tmp = setTimeout(function(){location.reload()}, 900000);
}

// request permission on page load
document.addEventListener('DOMContentLoaded', function () {
  if (!Notification) {
    alert('Desktop notifications not available in your browser. Try Chromium.'); 
    return;
  }

  if (Notification.permission !== "granted")
    Notification.requestPermission();
});

function notifyMe(name,failed) {
  if (Notification.permission !== "granted")
    Notification.requestPermission();
  else {
    var notification = new Notification("Warning!", {
      icon: "css/warningicon.png",
      body: "On " + name + ', ' + failed + " consecutive tests have failed",
    });

//    notification.onclick = function () {
//      window.open("http://stackoverflow.com/a/13328397/1269037");      
//    };

  }

}

</script>
</body>
</head>
</html> 
