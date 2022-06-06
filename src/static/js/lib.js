function show_login_form() {
	var form = document.getElementById('login_form');
	form.setAttribute("style", 'border-radius:10%;background-color:#343a40;position:absolute;width:15%;height:15%;left:77.5%;top:55px;z-index:25;opacity:1;');
}

function hide_login_form() {
	var form = document.getElementById('login_form');
	form.setAttribute("style", 'border-radius:10%;background-color:#343a40;position:absolute;width:15%;height:15%;left:77.5%;top:50px;z-index:-1;opacity:0;');
}

function sidebar_open() {
	document.getElementById("sidebar").style.width = "100%";
 	document.getElementById("sidebar").style.display = "block";
}

function sidebar_close() {
	document.getElementById("sidebar").style.display = "none";
}
