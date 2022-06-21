function show_login_form() {
	var form = document.getElementById('login_form');
	form.setAttribute("style", 'border-radius:10%;background-color:#343a40;position:absolute;width:15%;height:17.5%;left:77.5%;top:55px;z-index:25;opacity:1;');
}

function hide_login_form() {
	var form = document.getElementById('login_form');
	form.setAttribute("style", 'border-radius:10%;background-color:#343a40;position:absolute;width:15%;height:17.5%;left:77.5%;top:50px;z-index:-1;opacity:0;');
}

function sidebar_open() {
	document.getElementById("sidebar").style.width = "100%";
 	document.getElementById("sidebar").style.display = "block";
}

function sidebar_close() {
	document.getElementById("sidebar").style.display = "none";
}

function job_add_org() {
	var parent = document.getElementById("job_new_org_parent");
	parent.setAttribute("style", "visibility:visible;");

	var selector = document.getElementById("org_selector");
	selector.required = false;
	selector.disabled = true;

	document.getElementById("job_add_org_i").setAttribute("value", "True");
	document.getElementById("j_o_name").required = true;
	document.getElementById("j_o_phone").required = true;
	document.getElementById("j_o_website").required = true;
	document.getElementById("j_o_desc_short").required = true;
	document.getElementById("j_o_address_selector").required = true;
}

function edu_add_org() {
	var parent = document.getElementById("edu_new_org_parent");
	parent.setAttribute("style", "visibility:visible;");

	var selector = document.getElementById("edu_org_selector");
	selector.required = false;
	selector.disabled = true;

	document.getElementById("edu_add_org_i").setAttribute("value", "True");
	document.getElementById("e_o_name").required = true;
	document.getElementById("e_o_phone").required = true;
	document.getElementById("e_o_website").required = true;
	document.getElementById("e_o_desc_short").required = true;
	document.getElementById("e_o_address_selector").required = true;
}

function job_remove_org() {
	var parent = document.getElementById("job_new_org_parent");
	parent.setAttribute("style", "visibility:hidden;height:0px;");
	document.getElementById("org_selector").required = true;
	document.getElementById("org_selector").disabled = false;

	document.getElementById("job_add_org_i").setAttribute("value", "False");
	document.getElementById('job_add_address_i').setAttribute("value", "False");
	document.getElementById("j_o_name").required = false;
	document.getElementById("j_o_phone").required = false;
	document.getElementById("j_o_website").required = false;
	document.getElementById("j_o_desc_short").required = false;
	document.getElementById("j_o_address_selector").required = false;
	document.getElementById("j_o_address_selector").disabled = false;

	document.getElementById("j_o_new_address").required = false;
	document.getElementById("job_new_address_div").setAttribute("style", "visibility:hidden;height:0px;");

}

function edu_remove_org() {
	var parent = document.getElementById("edu_new_org_parent");
	parent.setAttribute("style", "visibility:hidden;height:0px;");
	document.getElementById("edu_org_selector").required = true;
	document.getElementById("edu_org_selector").disabled = false;

	document.getElementById("edu_add_org_i").setAttribute("value", "False");
	document.getElementById('edu_add_address_i').setAttribute("value", "False");
	document.getElementById("e_o_name").required = false;
	document.getElementById("e_o_phone").required = false;
	document.getElementById("e_o_website").required = false;
	document.getElementById("e_o_desc_short").required = false;
	document.getElementById("e_o_address_selector").required = false;
	document.getElementById("e_o_address_selector").disabled = false;

	document.getElementById("e_o_new_address").required = false;
	document.getElementById("edu_new_address_div").setAttribute("style", "visibility:hidden;height:0px;");

}

function job_remove_address() {
	document.getElementById('job_add_address_i').setAttribute("value", "False");
	document.getElementById("j_o_new_address").required = false;
	document.getElementById("j_o_address_selector").required = true;
	document.getElementById("j_o_address_selector").disabled = false;
	document.getElementById("job_new_address_div").setAttribute("style", "visibility:hidden;left:0px;");
}

function edu_remove_address() {
	document.getElementById('edu_add_address_i').setAttribute("value", "False");
	document.getElementById("e_o_new_address").required = false;
	document.getElementById("e_o_address_selector").required = true;
	document.getElementById("e_o_address_selector").disabled = false;
	document.getElementById("edu_new_address_div").setAttribute("style", "visibility:hidden;left:0px;");
}

function job_new_address() {
	document.getElementById('job_add_address_i').setAttribute("value", "True");
	document.getElementById("j_o_new_address").required = true;
	document.getElementById("j_o_address_selector").required = false;
	document.getElementById("j_o_address_selector").disabled = true;
	document.getElementById("job_new_address_div").setAttribute("style", "visibility:visible;left:0px;");
}

function edu_new_address() {
	document.getElementById('edu_add_address_i').setAttribute("value", "True");
	document.getElementById("e_o_new_address").required = true;
	document.getElementById("e_o_address_selector").required = false;
	document.getElementById("e_o_address_selector").disabled = true;
	document.getElementById("edu_new_address_div").setAttribute("style", "visibility:visible;left:0px;");
}

function org_new_address() {
	document.getElementById('org_add_address_i').setAttribute('value', "True");
	document.getElementById('a_o_new_address').required = true;
	document.getElementById('a_o_address_selector').required = false;
	document.getElementById('a_o_address_selector').disabled = true;
	document.getElementById('org_new_address_div').setAttribute('style', 'visibility:visible');
}

function e_org_new_address() {
	document.getElementById('org_edit_address_i').setAttribute('value', "True");
	document.getElementById('e_oo_new_address').required = true;
	document.getElementById('e_oo_address_selector').required = false;
	document.getElementById('e_oo_address_selector').disabled = true;
	document.getElementById('e_org_new_address_div').setAttribute('style', 'visibility:visible');
}

function org_remove_address() {
	document.getElementById('org_add_address_i').setAttribute('value', "False");
	document.getElementById('a_o_new_address').required = false;
	document.getElementById('a_o_address_selector').required = true;
	document.getElementById('a_o_address_selector').disabled = false;
	document.getElementById('org_new_address_div').setAttribute('style', 'visibility:hidden;display:none;');
}

function e_org_remove_address() {
	document.getElementById('org_edit_address_i').setAttribute('value', "False");
	document.getElementById('e_oo_new_address').required = false;
	document.getElementById('e_oo_address_selector').required = true;
	document.getElementById('e_oo_address_selector').disabled = false;
	document.getElementById('e_org_new_address_div').setAttribute('style', 'visibility:hidden;display:none;');
}

function contact_new_address() {
	document.getElementById('contact_add_address_i').setAttribute("value", "True");
	document.getElementById('e_c_new_address').required = true;
	document.getElementById('e_c_address_selector').required = false;
	document.getElementById('e_c_address_selector').disabled = true;
	document.getElementById('contact_new_address_div').setAttribute('style', 'visibility:visible;')
}

function contact_remove_address() {
	document.getElementById('contact_add_address_i').setAttribute("value", "False");
	document.getElementById("e_c_new_address").required = false;
	document.getElementById("e_c_address_selector").required = true;
	document.getElementById("e_c_address_selector").disabled = false;
	document.getElementById("contact_new_address_div").setAttribute("style", "visibility:hidden;display:none;");
}

function edit_contact(cid, name, phone1, phone2, email, objective, aid, aname) {
	document.getElementById('e_c_id').setAttribute('value', cid);
	document.getElementById('e_c_name').setAttribute('value', name);
	document.getElementById('e_c_phone1').setAttribute('value', phone1);
	document.getElementById('e_c_phone2').setAttribute('value', phone2);
	document.getElementById('e_c_email').setAttribute('value', email);
	document.getElementById('e_c_objective').value = objective;
	
	var addr_selector = document.getElementById('e_c_address_selector');
	for (var i = 0; i < addr_selector.options.length; i++) {
		if (addr_selector.options[i].value == aid) {
			addr_selector.options[i].selected = true;
		}
	}
}

function edit_org(oid, name, phone, desc_short, website, aid, aname) {
	var logo = document.getElementById('org_logo_bin').value;
	var head = document.getElementById('org_image_head_bin').value;
	document.getElementById('e_oo_img1').setAttribute('src', logo);
	document.getElementById('e_oo_img2').setAttribute('src', head);
	document.getElementById('e_oo_img1').setAttribute('style', '');
	document.getElementById('e_oo_img2').setAttribute('style', '');
	
	document.getElementById('e_oo_id').setAttribute('value', oid);
	document.getElementById('e_oo_name').setAttribute('value', name);
	document.getElementById('e_oo_phone').setAttribute('value', phone);
	document.getElementById('e_oo_desc_short').value = desc_short;
	document.getElementById('e_oo_website').setAttribute('value', website);
	
	var addr_selector = document.getElementById('e_oo_address_selector');
	for (var i = 0; i < addr_selector.options.length; i++) {
		if (addr_selector.options[i].value == aid) {
			addr_selector.options[i].selected = true;
		}
	}
}

function job_add_skill(number, mobile) {
	number = number + 1;

	var parent_div = document.getElementById("job_add_skill_div");
	var add_btn = document.getElementById("job_add_skill_button");
	add_btn.setAttribute("onClick", "javascript: job_add_skill(" + String(number) + ", " + String(mobile) + ")");
	var main_div = document.getElementById("job_new_skill_parent");
	main_div.setAttribute("style", "visibility:visible;");

	var add_skills = document.getElementById('job_add_skills_i');
	add_skills.setAttribute("value", "True");

	var max_skills = document.getElementById('job_max_skills');
	max_skills.setAttribute("value", String(number));

	make_add_skill(number, parent_div, mobile, 'j');
}

function edu_add_skill(number, mobile) {
	number = number + 1;

	var parent_div = document.getElementById("edu_add_skill_div");
	var add_btn = document.getElementById("edu_add_skill_button");
	add_btn.setAttribute("onClick", "javascript: edu_add_skill(" + String(number) + ", " + String(mobile) + ")");
	var main_div = document.getElementById("edu_new_skill_parent");
	main_div.setAttribute("style", "visibility:visible;");

	var add_skills = document.getElementById('edu_add_skills_i');
	add_skills.setAttribute("value", "True");

	var max_skills = document.getElementById('edu_max_skills');
	max_skills.setAttribute("value", String(number));

	make_add_skill(number, parent_div, mobile, 'e');
}

function job_remove_skill(number) {
	var container = document.getElementById("j_s_container" + String(number));
	container.remove();

	var parent_div = document.getElementById("job_add_skill_div");
	if (parent_div.childElementCount == 0) {
		var main_div = document.getElementById("job_new_skill_parent");
		main_div.setAttribute("style", "visibility:hidden;height:0px;");

		var add_skills = document.getElementById('job_add_skills_i');
		add_skills.setAttribute("value", "False");
	}
}

function edu_remove_skill(number) {
	var container = document.getElementById("e_s_container" + String(number));
	container.remove();

	var parent_div = document.getElementById("edu_add_skill_div");
	if (parent_div.childElementCount == 0) {
		var main_div = document.getElementById("edu_new_skill_parent");
		main_div.setAttribute("style", "visibility:hidden;height:0px;");

		var add_skills = document.getElementById('edu_add_skills_i');
		add_skills.setAttribute("value", "False");
	}
}

function make_add_skill(number, parent, mobile, letter) {
	if (mobile == 0) {
		var main_container = document.createElement("div");
		main_container.setAttribute("class", "container");
		main_container.setAttribute("id", letter + "_s_container" + String(number));

		var br = document.createElement("br");

		var row1 = document.createElement("div");
		row1.setAttribute("class", "row");
		main_container.appendChild(row1);

		var delbtn = document.createElement("button");
		delbtn.setAttribute("type", "button");
		delbtn.setAttribute("class", "close");
		if (letter == 'j') {
			delbtn.setAttribute("onClick", "javascript: job_remove_skill(" + String(number) + ")");
		}
		else {
			delbtn.setAttribute("onClick", "javascript: edu_remove_skill(" + String(number) + ")");
		}
		
		delbtn.setAttribute("style", "margin-left:auto;margin-right:0;");
		row1.appendChild(delbtn);

		var span = document.createElement("span");
		span.setAttribute("aria-hidden", "true");
		span.innerHTML = "&times;";
		delbtn.appendChild(span);

		var row2 = document.createElement("div");
		row2.setAttribute("class", "row");
		//row2.setAttribute("style", "padding-top:15px;");
		main_container.appendChild(row2);

		var col2_1 = document.createElement("div");
		col2_1.setAttribute("class", "col-sm-6");
		row2.appendChild(col2_1);

		var lbl2_1 = document.createElement("label");
		lbl2_1.setAttribute("for", letter + "_s_name" + String(number));
		lbl2_1.innerHTML = "Name";
		col2_1.appendChild(lbl2_1);

		col2_1.appendChild(br);

		var i2_1 = document.createElement("input");
		i2_1.setAttribute("id", letter + "_s_name" + String(number));
		i2_1.setAttribute("type", "text");
		i2_1.setAttribute("name", letter + "_s_name" + String(number));
		i2_1.setAttribute("placeholder", "Skill name");
		i2_1.required = true;
		col2_1.appendChild(i2_1);

		var col2_2 = document.createElement("div");
		col2_2.setAttribute("class", "col-sm-6");
		row2.appendChild(col2_2);

		var lbl2_2 = document.createElement("label");
		lbl2_2.setAttribute("for", letter + "_s_exposure" + String(number));
		lbl2_2.innerHTML = "Exposure";
		col2_2.appendChild(lbl2_2);

		var br = document.createElement("br");
		col2_2.appendChild(br);

		var i2_2 = document.createElement("input");
		i2_2.setAttribute("id", letter + "_s_exposure" + String(number));
		i2_2.setAttribute("type", "text");
		i2_2.setAttribute("name", letter + "_s_exposure" + String(number));
		i2_2.setAttribute("placeholder", "Exposure");
		i2_2.required = true;
		col2_2.appendChild(i2_2);

		var row3 = document.createElement("div");
		row3.setAttribute("class", "row");
		row3.setAttribute("style", "padding-top:15px;");
		main_container.appendChild(row3);

		var col3_1 = document.createElement("div");
		col3_1.setAttribute("class", "col-sm-6");
		row3.appendChild(col3_1);

		var lbl3_1 = document.createElement("label");
		lbl3_1.setAttribute("for", letter + "_s_reference" + String(number));
		lbl3_1.innerHTML = "Reference website";
		col3_1.appendChild(lbl3_1);

		var br = document.createElement("br");
		col3_1.appendChild(br);

		var i3_1 = document.createElement("input");
		i3_1.setAttribute("id", letter + "_s_reference" + String(number));
		i3_1.setAttribute("type", "text");
		i3_1.setAttribute("name", letter + "_s_reference" + String(number));
		i3_1.setAttribute("placeholder", "URL");
		i3_1.required = true;
		col3_1.appendChild(i3_1);

		var col3_2 = document.createElement("div");
		col3_2.setAttribute("class", "col-sm-6");
		row3.appendChild(col3_2);

		var lbl3_2 = document.createElement("label");
		lbl3_2.setAttribute("for", letter + "_s_category" + String(number));
		lbl3_2.innerHTML = "Skill category";
		col3_2.appendChild(lbl3_2);

		var br = document.createElement("br");
		col3_2.appendChild(br);

		var i3_2 = document.createElement("input");
		i3_2.setAttribute("id", letter + "_s_category" + String(number));
		i3_2.setAttribute("type", "text");
		i3_2.setAttribute("name", letter + "_s_category" + String(number));
		i3_2.setAttribute("placeholder", "Skill category");
		i3_2.required = true;
		col3_2.appendChild(i3_2);

		var row4 = document.createElement("div");
		row4.setAttribute("class", "row");
		row4.setAttribute("style", "padding-top:15px;");
		main_container.appendChild(row4);

		var col4_1 = document.createElement("div");
		col4_1.setAttribute("class", "col-sm-6");
		row4.appendChild(col4_1);

		var lbl4_1 = document.createElement("label");
		lbl4_1.setAttribute("for", letter + "_s_desc_short" + String(number));
		lbl4_1.innerHTML = "Description";
		col4_1.appendChild(lbl4_1);

		var br = document.createElement("br");
		col4_1.appendChild(br);

		var i4_1 = document.createElement("textarea");
		i4_1.setAttribute("name", letter + "_s_desc_short" + String(number));
		if (letter == 'j') {
			i4_1.setAttribute("form", "create_job");
		}
		else {
			i4_1.setAttribute("form", "create_edu");
		}
		i4_1.setAttribute("placeholder", "Short description of what the skill is");
		i4_1.setAttribute("style", "width:95%;height:100px;");
		i4_1.required = true;
		col4_1.appendChild(i4_1);

		var col4_2 = document.createElement("div");
		col4_2.setAttribute("class", "col-sm-6");
		row4.appendChild(col4_2);

		var lbl4_2 = document.createElement("label");
		lbl4_2.setAttribute("for", letter + "_s_desc_long" + String(number));
		lbl4_2.innerHTML = "Commentary";
		col4_2.appendChild(lbl4_2);

		var br = document.createElement("br");
		col4_2.appendChild(br);

		var i4_2 = document.createElement("textarea");
		i4_2.setAttribute("name", letter + "_s_desc_long" + String(number));
		if (letter == 'j') {
			i4_2.setAttribute("form", "create_job");
		}
		else {
			i4_2.setAttribute("form", "create_edu");
		}
		i4_2.setAttribute("placeholder", "Comments on how the skill has been used");
		i4_2.setAttribute("style", "width:95%;height:100px;");
		i4_2.required = true;
		col4_2.appendChild(i4_2);

		var row5 = document.createElement("div");
		row5.setAttribute("class", "row");
		row5.setAttribute("style", "padding-top:15px;");
		main_container.appendChild(row5);

		var col5_1 = document.createElement("div");
		col5_1.setAttribute("class", "col-sm-6");
		row5.appendChild(col5_1);

		var lbl5_1 = document.createElement("label");
		lbl5_1.setAttribute("for", letter + "_s_icon" + String(number));
		lbl5_1.innerHTML = "Icon Image";
		col5_1.appendChild(lbl5_1);

		var br = document.createElement("br");
		col5_1.appendChild(br);

		var i5_1 = document.createElement("input");
		i5_1.setAttribute("id", letter + "_s_icon" + String(number));
		i5_1.setAttribute("type", "file");
		i5_1.setAttribute("name", letter + "_s_icon" + String(number));
		i5_1.setAttribute("accept", "image/png, image/jpeg");
		pp = letter + "_s_icon" + String(number);
		i5_1.setAttribute("onChange", "upload_img('" + pp + "')");
		col5_1.appendChild(i5_1);

		var i5_11 = document.createElement("input");
		i5_11.setAttribute("type", "hidden");
		i5_11.setAttribute("name", letter + "_s_icon" + String(number) + "_val");
		i5_11.setAttribute("id", letter + "_s_icon" + String(number) + "_val");
		col5_1.appendChild(i5_11);

		var col5_2 = document.createElement("div");
		col5_2.setAttribute("class", "col-sm-6");
		row5.appendChild(col5_2);

		var lbl5_2 = document.createElement("label");
		lbl5_2.setAttribute("for", letter + "_s_soft" + String(number));
		lbl5_2.innerHTML = "Soft skill";
		col5_2.appendChild(lbl5_2);

		var br = document.createElement("br");
		col5_2.appendChild(br);

		var i5_2 = document.createElement("input");
		i5_2.setAttribute("id", letter + "_s_soft" + String(number));
		i5_2.setAttribute("type", "checkbox");
		i5_2.setAttribute("name", letter + "_s_soft" + String(number));
		col5_2.appendChild(i5_2);

		var hr = document.createElement("hr");
		main_container.appendChild(hr);

		parent.appendChild(main_container);
	}
	else {
		var main_container = document.createElement("div");
		main_container.setAttribute("class", "container");
		main_container.setAttribute("id", letter + "_s_container" + String(number));



		var br = document.createElement("br");

		var row1 = document.createElement("div");
		row1.setAttribute("class", "row");
		main_container.appendChild(row1);

		var delbtn = document.createElement("button");
		delbtn.setAttribute("type", "button");
		delbtn.setAttribute("class", "close");
		delbtn.setAttribute("onClick", "javascript: job_remove_skill(" + String(number) + ")");
		delbtn.setAttribute("style", "margin-left:auto;margin-right:0;");
		row1.appendChild(delbtn);

		var span = document.createElement("span");
		span.setAttribute("aria-hidden", "true");
		span.innerHTML = "&times;";
		delbtn.appendChild(span);

		var row2 = document.createElement("div");
		row2.setAttribute("class", "row");
		//row2.setAttribute("style", "padding-top:15px;");
		main_container.appendChild(row2);

		var col2_1 = document.createElement("div");
		col2_1.setAttribute("class", "col-sm-6");
		row2.appendChild(col2_1);

		var lbl2_1 = document.createElement("label");
		lbl2_1.setAttribute("for", letter + "_s_name" + String(number));
		lbl2_1.innerHTML = "Name";
		col2_1.appendChild(lbl2_1);

		col2_1.appendChild(br);

		var i2_1 = document.createElement("input");
		i2_1.setAttribute("id", letter + "_s_name" + String(number));
		i2_1.setAttribute("type", "text");
		i2_1.setAttribute("name", letter + "_s_name" + String(number));
		i2_1.setAttribute("placeholder", "Skill name");
		i2_1.required = true;
		col2_1.appendChild(i2_1);

		var row2 = document.createElement("div");
		row2.setAttribute("class", "row");
		row2.setAttribute("style", "padding-top:15px;");
		main_container.appendChild(row2);

		var col2_2 = document.createElement("div");
		col2_2.setAttribute("class", "col-sm-6");
		row2.appendChild(col2_2);

		var lbl2_2 = document.createElement("label");
		lbl2_2.setAttribute("for", letter + "_s_exposure" + String(number));
		lbl2_2.innerHTML = "Exposure";
		col2_2.appendChild(lbl2_2);

		var br = document.createElement("br");
		col2_2.appendChild(br);

		var i2_2 = document.createElement("input");
		i2_2.setAttribute("id", letter + "_s_exposure" + String(number));
		i2_2.setAttribute("type", "text");
		i2_2.setAttribute("name", letter + "_s_exposure" + String(number));
		i2_2.setAttribute("placeholder", "Exposure");
		i2_2.required = true;
		col2_2.appendChild(i2_2);

		var row3 = document.createElement("div");
		row3.setAttribute("class", "row");
		row3.setAttribute("style", "padding-top:15px;");
		main_container.appendChild(row3);

		var col3_1 = document.createElement("div");
		col3_1.setAttribute("class", "col-sm-6");
		row3.appendChild(col3_1);

		var lbl3_1 = document.createElement("label");
		lbl3_1.setAttribute("for", letter + "_s_reference" + String(number));
		lbl3_1.innerHTML = "Reference website";
		col3_1.appendChild(lbl3_1);

		var br = document.createElement("br");
		col3_1.appendChild(br);

		var i3_1 = document.createElement("input");
		i3_1.setAttribute("id", letter + "_s_reference" + String(number));
		i3_1.setAttribute("type", "text");
		i3_1.setAttribute("name", letter + "_s_reference" + String(number));
		i3_1.setAttribute("placeholder", "URL");
		i3_1.required = true;
		col3_1.appendChild(i3_1);

		var row3 = document.createElement("div");
		row3.setAttribute("class", "row");
		row3.setAttribute("style", "padding-top:15px;");
		main_container.appendChild(row3);

		var col3_2 = document.createElement("div");
		col3_2.setAttribute("class", "col-sm-6");
		row3.appendChild(col3_2);

		var lbl3_2 = document.createElement("label");
		lbl3_2.setAttribute("for", letter + "_s_category" + String(number));
		lbl3_2.innerHTML = "Skill category";
		col3_2.appendChild(lbl3_2);

		var br = document.createElement("br");
		col3_2.appendChild(br);

		var i3_2 = document.createElement("input");
		i3_2.setAttribute("id", letter + "_s_category" + String(number));
		i3_2.setAttribute("type", "text");
		i3_2.setAttribute("name", letter + "_s_category" + String(number));
		i3_2.setAttribute("placeholder", "Skill category");
		i3_2.required = true;
		col3_2.appendChild(i3_2);

		var row4 = document.createElement("div");
		row4.setAttribute("class", "row");
		row4.setAttribute("style", "padding-top:15px;");
		main_container.appendChild(row4);

		var col4_1 = document.createElement("div");
		col4_1.setAttribute("class", "col-sm-6");
		row4.appendChild(col4_1);

		var lbl4_1 = document.createElement("label");
		lbl4_1.setAttribute("for", letter + "_s_desc_short" + String(number));
		lbl4_1.innerHTML = "Description";
		col4_1.appendChild(lbl4_1);

		var br = document.createElement("br");
		col4_1.appendChild(br);

		var i4_1 = document.createElement("textarea");
		i4_1.setAttribute("name", letter + "_s_desc_short" + String(number));
		i4_1.setAttribute("form", "create_job");
		i4_1.setAttribute("placeholder", "Short description of what the skill is");
		i4_1.setAttribute("style", "width:95%;height:100px;");
		i4_1.required = true;
		col4_1.appendChild(i4_1);

		var row4 = document.createElement("div");
		row4.setAttribute("class", "row");
		row4.setAttribute("style", "padding-top:15px;");
		main_container.appendChild(row4);

		var col4_2 = document.createElement("div");
		col4_2.setAttribute("class", "col-sm-6");
		row4.appendChild(col4_2);

		var lbl4_2 = document.createElement("label");
		lbl4_2.setAttribute("for", letter + "_s_desc_long" + String(number));
		lbl4_2.innerHTML = "Commentary";
		col4_2.appendChild(lbl4_2);

		var br = document.createElement("br");
		col4_2.appendChild(br);

		var i4_2 = document.createElement("textarea");
		i4_2.setAttribute("name", letter + "_s_desc_long" + String(number));
		i4_2.setAttribute("form", "create_job");
		i4_2.setAttribute("placeholder", "Comments on how the skill has been used");
		i4_2.setAttribute("style", "width:95%;height:100px;");
		i4_2.required = true;
		col4_2.appendChild(i4_2);

		var row5 = document.createElement("div");
		row5.setAttribute("class", "row");
		row5.setAttribute("style", "padding-top:15px;");
		main_container.appendChild(row5);

		var col5_1 = document.createElement("div");
		col5_1.setAttribute("class", "col-sm-6");
		row5.appendChild(col5_1);

		var lbl5_1 = document.createElement("label");
		lbl5_1.setAttribute("for", letter + "_s_icon" + String(number));
		lbl5_1.innerHTML = "Icon Image";
		col5_1.appendChild(lbl5_1);

		var br = document.createElement("br");
		col5_1.appendChild(br);

		var i5_1 = document.createElement("input");
		i5_1.setAttribute("id", letter + "_s_icon" + String(number));
		i5_1.setAttribute("type", "file");
		i5_1.setAttribute("name", letter + "_s_icon" + String(number));
		i5_1.setAttribute("accept", "image/png, image/jpeg");
		pp = letter + "_s_icon" + String(number);
		i5_1.setAttribute("onChange", "upload_img('" + pp + "')");
		col5_1.appendChild(i5_1);

		var i5_11 = document.createElement("input");
		i5_11.setAttribute("type", "hidden");
		i5_11.setAttribute("name", letter + "_s_icon" + String(number) + "_val");
		i5_11.setAttribute("id", letter + "_s_icon" + String(number) + "_val");
		col5_1.appendChild(i5_11);

		var row5 = document.createElement("div");
		row5.setAttribute("class", "row");
		row5.setAttribute("style", "padding-top:15px;");
		main_container.appendChild(row5);

		var col5_2 = document.createElement("div");
		col5_2.setAttribute("class", "col-sm-6");
		row5.appendChild(col5_2);

		var lbl5_2 = document.createElement("label");
		lbl5_2.setAttribute("for", letter + "_s_soft" + String(number));
		lbl5_2.innerHTML = "Soft skill";
		col5_2.appendChild(lbl5_2);

		var br = document.createElement("br");
		col5_2.appendChild(br);

		var i5_2 = document.createElement("input");
		i5_2.setAttribute("id", letter + "_s_soft" + String(number));
		i5_2.setAttribute("type", "checkbox");
		i5_2.setAttribute("name", letter + "_s_soft" + String(number));
		col5_2.appendChild(i5_2);

		var hr = document.createElement("hr");
		main_container.appendChild(hr);

		parent.appendChild(main_container);
	}
}

function edit_edu(eid, oid, oname, degree, gpa, date_stop, desc_short, desc_long, len_skill) {
	var skills_parent = document.getElementById(eid);
	var skill_list = [];
	
	var children = skills_parent.children;
	for (var i = 0; i < children.length; i++) {
		var child = children[i];
		var value = child.value;
		var split = value.split(',');
		skill_list.push(split[0]);
	}
	
	document.getElementById('e_e_id').value = eid;
	document.getElementById('e_e_degree').value = degree;
	document.getElementById('e_e_gpa').value = gpa;
	document.getElementById('e_e_date_stop').value = date_stop;
	document.getElementById('e_e_desc_short').value = desc_short;
	document.getElementById('e_e_desc_long').value = desc_long;
	
	var org_selector = document.getElementById('e_e_org_selector');
	var skill_selector = document.getElementById('e_e_skill_selector');
	
	for (var i = 0; i < skill_selector.options.length; i++) {
		skill_selector.options[i].selected = skill_list.indexOf(skill_selector.options[i].value) >= 0;
	}
	
	for (var i = 0; i < org_selector.options.length; i++) {
		if (org_selector.options[i].value == oid) {
			org_selector.options[i].selected = true;
		}
	}
}

function edit_job(jid, oid, oname, title, present, date_start, date_stop, desc_short, desc_long, len_skill) {
	var skills_parent = document.getElementById(jid);
	var skill_list = [];
	
	var children = skills_parent.children;
	for (var i = 0; i < children.length; i++) {
		var child = children[i];
		var value = child.value;
		var split = value.split(',');
		skill_list.push(split[0]);
	}
	
	document.getElementById('e_j_id').value = jid;
	document.getElementById('e_j_title').value = title
	if (present == 0) {
		document.getElementById('e_j_present').checked = false;
	}
	else {
		document.getElementById('e_j_present').checked = true;
	}
	document.getElementById('e_j_date_start').value = date_start;
	document.getElementById('e_j_date_stop').value = date_stop;
	document.getElementById('e_j_desc_short').value = desc_short;
	document.getElementById('e_j_desc_long').value = desc_long;
	
	var org_selector = document.getElementById('e_j_org_selector');
	var skill_selector = document.getElementById('e_j_skill_selector');
	
	for (var i = 0; i < skill_selector.options.length; i++) {
		skill_selector.options[i].selected = skill_list.indexOf(skill_selector.options[i].value) >= 0;
	}
	
	for (var i = 0; i < org_selector.options.length; i++) {
		if (org_selector.options[i].value == oid) {
			org_selector.options[i].selected = true;
		}
	}
}

function del_edu(eid, degree, org_dangles, oid, oname, addr_dangles, aid, aname) {

	document.getElementById('d_e_aname').disabled = true;
	document.getElementById('d_e_aid').disabled = true;
	document.getElementById('d_e_oname').disabled = true;
	document.getElementById('d_e_oid').disabled = true;
	document.getElementById('d_e_degree').disabled = true;
	document.getElementById('d_e_id').disabled = true;

	document.getElementById('d_e_id').value = eid;
	document.getElementById('d_e_degree').value = degree;
	
	if (org_dangles == 1) {
		document.getElementById('d_e_dangle_org').setAttribute('style', 'visibility:visible');
		document.getElementById('d_e_oid').value = oid;
		document.getElementById('d_e_oname').value = oname;
		if (addr_dangles == 1) {
			document.getElementById('d_e_aid').value = aid;
			document.getElementById('d_e_aname').value = aname;
			document.getElementById('d_e_del_org').setAttribute('onChange', "del_edu_addr()");
		}
		else {
			document.getElementById('d_e_dangle_addr').setAttribute('style', 'visibility:hidden;display:none;');
			document.getElementById('d_e_del_org').setAttribute('onChange', "javascript:void(0)");
		}
	}
	else {
		document.getElementById('d_e_dangle_org').setAttribute('style', 'visibility:hidden;display:none;');
		document.getElementById('d_e_dangle_addr').setAttribute('style', 'visibility:hidden;display:none;');
	}
}

function del_edu_addr() {
	var addr_container = document.getElementById('d_e_dangle_addr');
	if (document.getElementById('d_e_del_org').options.selectedIndex == 0) {
		addr_container.setAttribute('style', 'visibility:hidden;display:none;');
		document.getElementById('d_e_del_addr').options.selectedIndex = 0;
	}
	else {
		addr_container.setAttribute('style', 'visibility:visible;');
	}
}

function del_edu_enable() {
	document.getElementById('d_e_aname').disabled = false;
	document.getElementById('d_e_aid').disabled = false;
	document.getElementById('d_e_oname').disabled = false;
	document.getElementById('d_e_oid').disabled = false;
	document.getElementById('d_e_degree').disabled = false;
	document.getElementById('d_e_id').disabled = false;
}

function del_job(jid, title, org_dangles, oid, oname, addr_dangles, aid, aname) {
	document.getElementById('d_j_aname').disabled = true;
	document.getElementById('d_j_aid').disabled = true;
	document.getElementById('d_j_oname').disabled = true;
	document.getElementById('d_j_oid').disabled = true;
	document.getElementById('d_j_title').disabled = true;
	document.getElementById('d_j_id').disabled = true;
	
	document.getElementById('d_j_id').value = jid;
	document.getElementById('d_j_title').value = title;
	
	if (org_dangles == 1) {
		document.getElementById('d_j_dangle_org').setAttribute('style', 'visibility:visible;');
		document.getElementById('d_j_oid').value = oid;
		document.getElementById('d_j_oname').value = oname;
		if (addr_dangles == 1) {
			document.getElementById('d_j_aid').value = aid;
			document.getElementById('d_j_aname').value = aname;
			document.getElementById('d_j_del_org').setAttribute('onChange', "del_job_addr()");
		}
		else {
			document.getElementById('d_j_dangle_addr').setAttribute('style', 'visibility:hidden;display:none;');
			document.getElementById('d_j_del_org').setAttribute('onChange', "javascript:void(0)");
		}
	}
	else {
		document.getElementById('d_j_dangle_org').setAttribute('style', 'visibility:hidden;display:none;');
		document.getElementById('d_j_dangle_addr').setAttribute('style', 'visibility:hidden;display:none;');
	}
}

function del_job_addr() {
	var addr_container = document.getElementById('d_j_dangle_addr');
	if (document.getElementById('d_j_del_org').options.selectedIndex == 0) {
		addr_container.setAttribute('style', 'visibility:hidden;display:none;');
		document.getElementById('d_j_del_addr').options.selectedIndex = 0;
	}
	else {
		addr_container.setAttribute('style', 'visibility:visible;');
	}
}

function del_job_enable() {
	document.getElementById('d_j_aname').disabled = false;
	document.getElementById('d_j_aid').disabled = false;
	document.getElementById('d_j_oname').disabled = false;
	document.getElementById('d_j_oid').disabled = false;
	document.getElementById('d_j_title').disabled = false;
	document.getElementById('d_j_id').disabled = false;
}

function del_org(oid, name, addr_dangles, aid, aname, job_dangles, job_dangling, edu_dangles, edu_dangling, mobile) {
	console.log(mobile)
	document.getElementById('o_o_del_btn').setAttribute('onClick', 'javascript: void(0)');
	
	document.getElementById('d_o_aname').disabled = true;
	document.getElementById('d_o_aid').disabled = true;
	document.getElementById('d_o_name').disabled = true;
	document.getElementById('d_o_id').disabled = true;
	
	document.getElementById('d_o_id').value = oid
	document.getElementById('d_o_name').value = name
	
	if (addr_dangles == 1) { 
		document.getElementById('d_o_dangle_addr').setAttribute('style', 'visibility:visible;');
		document.getElementById('d_o_aid').value = aid;
		document.getElementById('d_o_aname').value = aname;
	}
	else {
		document.getElementById('d_o_dangle_addr').setAttribute('style', 'visibility:hidden;display:none;');
	}
	
	var all_orgs_n = parseInt(document.getElementById('all_orgs_len').value);
	all_orgs = [];
	
	for (var i = 0; i < all_orgs_n; i++) {
		var inp = document.getElementById('all_orgs' + String(i));
		split = inp.value.split(",");
		o = [split[0], split[1]];
		all_orgs.push(o);
	}
	
	var j_count = 0;
	var e_count = 0;
	
	
	if (job_dangles == 1) {
		document.getElementById('d_o_dangle_jobs').setAttribute('style', 'visibility:visible;');
		
		var parent = document.getElementById('d_o_dangle_jobs_list');
		job_split = job_dangling.split(",");
		console.log(job_split);
		edu_split = edu_dangling.split(",");
		
		if (mobile == 0) {
		
			for (var i = 0; i < job_split.length; i += 2) {
				if (job_split[i] != '') {
					jid = job_split[i];
					jname = job_split[i+1];
					
					var row = document.createElement('div');
					row.setAttribute('class', "row");
					row.setAttribute('style', 'padding-top:15px;');
					parent.appendChild(row);
					
					var col1 = document.createElement('div');
					col1.setAttribute('class', 'col-6');
					row.appendChild(col1);
					
					var idlbl = document.createElement('label');
					idlbl.setAttribute('for', 'd_o_jid' + String(i));
					idlbl.innerHTML = "Job ID";
					col1.appendChild(idlbl);
					
					var br = document.createElement('br');
					col1.appendChild(br);
					
					var idinput = document.createElement('input');
					idinput.setAttribute('type', 'text');
					idinput.disabled = true;
					idinput.setAttribute('value', jid);
					idinput.setAttribute('id', 'd_o_jid' + String(i));
					idinput.setAttribute('name', 'd_o_jid' + String(i));
					idinput.setAttribute('style', 'width:95%;');
					col1.appendChild(idinput);
					
					var br = document.createElement('br');
					col1.appendChild(br);
					var br = document.createElement('br');
					col1.appendChild(br);
					
					var namelbl = document.createElement('label')
					namelbl.setAttribute('for', 'd_o_jname' + String(i));
					namelbl.innerHTML = "Job Name";
					col1.appendChild(namelbl);
					
					var br = document.createElement('br');
					col1.appendChild(br);
					
					var nameinput = document.createElement('input');
					nameinput.setAttribute('type', 'text');
					nameinput.disabled = true;
					nameinput.value = jname;
					nameinput.setAttribute('id', 'd_o_jname' + String(i));
					nameinput.setAttribute('name', 'd_o_jname' + String(i));
					nameinput.setAttribute('style', 'width:95%');
					col1.appendChild(nameinput);
					
					var col2 = document.createElement('div');
					col2.setAttribute('class', 'col-6');
					row.appendChild(col2);
					
					var selectorlbl = document.createElement('label');
					selectorlbl.setAttribute('for', 'd_o_j_selector');
					selectorlbl.innerHTML = 'Select New Organization'
					col2.appendChild(selectorlbl);
					
					var br = document.createElement('br');
					col2.appendChild(br);
					
					var selector = document.createElement('select');
					selector.required = true;
					selector.setAttribute('id', 'd_o_j_selector' + String(i));
					selector.setAttribute('name', 'd_o_j_selector' + String(i));
					selector.setAttribute('style', 'min-width:95%;');
					selector.setAttribute('size', '5');
					col2.appendChild(selector);
					
					for (var j = 0; j < all_orgs.length; j++) {
						if (all_orgs[j][0] != oid) {
							var option = document.createElement('option');
							option.setAttribute('value', all_orgs[j][0]);
							option.innerHTML = all_orgs[j][1];
							selector.appendChild(option);
						}
					}
					
					var row = document.createElement('div');
					row.setAttribute('class', "row");
					parent.appendChild(row);
					var hr = document.createElement('hr');
					hr.setAttribute('style', 'width:90%;left:5%;');
					row.appendChild(hr)
					
					j_count += 1;
				}
			}
		
		}
		else {
			
			for (var i = 0; i < job_split.length; i += 2) {
				if (job_split[i] != '') {
					jid = job_split[i];
					jname = job_split[i+1];
					
					var row = document.createElement('div');
					row.setAttribute('class', "row");
					row.setAttribute('style', 'padding-top:15px;');
					parent.appendChild(row);
					
					var col1 = document.createElement('div');
					col1.setAttribute('class', 'col-12');
					row.appendChild(col1);
					
					var idlbl = document.createElement('label');
					idlbl.setAttribute('for', 'd_o_jid' + String(i));
					idlbl.innerHTML = "Job ID";
					col1.appendChild(idlbl);
					
					var br = document.createElement('br');
					col1.appendChild(br);
					
					var idinput = document.createElement('input');
					idinput.setAttribute('type', 'text');
					idinput.disabled = true;
					idinput.setAttribute('value', jid);
					idinput.setAttribute('id', 'd_o_jid' + String(i));
					idinput.setAttribute('name', 'd_o_jid' + String(i));
					idinput.setAttribute('style', 'width:95%;');
					col1.appendChild(idinput);
					
					var row1 = document.createElement('div');
					row1.setAttribute('class', "row");
					row1.setAttribute('style', 'padding-top:15px;');
					parent.appendChild(row1);
					
					var col1 = document.createElement('div');
					col1.setAttribute('class', 'col-12');
					row1.appendChild(col1);
					
					var namelbl = document.createElement('label')
					namelbl.setAttribute('for', 'd_o_jname' + String(i));
					namelbl.innerHTML = "Job Name";
					col1.appendChild(namelbl);
					
					var br = document.createElement('br');
					col1.appendChild(br);
					
					var nameinput = document.createElement('input');
					nameinput.setAttribute('type', 'text');
					nameinput.disabled = true;
					nameinput.value = jname;
					nameinput.setAttribute('id', 'd_o_jname' + String(i));
					nameinput.setAttribute('name', 'd_o_jname' + String(i));
					nameinput.setAttribute('style', 'width:95%');
					col1.appendChild(nameinput);
					
					var row = document.createElement('div');
					row.setAttribute('class', "row");
					row.setAttribute('style', 'padding-top:15px;');
					parent.appendChild(row);
					
					var col1 = document.createElement('div');
					col1.setAttribute('class', 'col-12');
					row.appendChild(col1);
					
					var selectorlbl = document.createElement('label');
					selectorlbl.setAttribute('for', 'd_o_j_selector');
					selectorlbl.innerHTML = 'Select New Organization'
					col1.appendChild(selectorlbl);
					
					var row = document.createElement('div');
					row.setAttribute('class', "row");
					parent.appendChild(row);
					
					var col1 = document.createElement('div');
					col1.setAttribute('class', 'col-12');
					row.appendChild(col1);
					
					
					var selector = document.createElement('select');
					selector.required = true;
					selector.setAttribute('id', 'd_o_j_selector' + String(i));
					selector.setAttribute('name', 'd_o_j_selector' + String(i));
					selector.setAttribute('style', 'min-width:95%;');
					selector.setAttribute('size', '5');
					col1.appendChild(selector);
					
					for (var j = 0; j < all_orgs.length; j++) {
						if (all_orgs[j][0] != oid) {
							var option = document.createElement('option');
							option.setAttribute('value', all_orgs[j][0]);
							option.innerHTML = all_orgs[j][1];
							selector.appendChild(option);
						}
					}
					
					var row = document.createElement('div');
					row.setAttribute('class', "row");
					parent.appendChild(row);
					var hr = document.createElement('hr');
					hr.setAttribute('style', 'width:90%;left:5%;');
					row.appendChild(hr)
					
					j_count += 1;
				}
			}
		
		}
		
		var hnp = document.createElement('input');
		hnp.setAttribute('type', 'hidden');
		hnp.setAttribute('id', 'd_o_numjobs');
		hnp.setAttribute('name', 'd_o_numjobs');
		hnp.setAttribute('value', String(j_count));
		parent.appendChild(hnp);
		
	}

	if (edu_dangles == 1) {
		document.getElementById('d_o_dangle_edus').setAttribute('style', 'visibility:visible;');
		
		var parent = document.getElementById('d_o_dangle_edus_list');
		job_split = job_dangling.split(",");
		console.log(job_split);
		edu_split = edu_dangling.split(",");
		
		
		if (mobile == 0) {
		
			for (var i = 0; i < edu_split.length; i += 2) {
				if (edu_split[i] != '') {
					eid = edu_split[i];
					ename = edu_split[i+1];
					
					var row = document.createElement('div');
					row.setAttribute('class', "row");
					row.setAttribute('style', 'padding-top:15px;');
					parent.appendChild(row);
					
					var col1 = document.createElement('div');
					col1.setAttribute('class', 'col-6');
					row.appendChild(col1);
					
					var idlbl = document.createElement('label');
					idlbl.setAttribute('for', 'd_o_eid' + String(i));
					idlbl.innerHTML = "Education ID";
					col1.appendChild(idlbl);
					
					var br = document.createElement('br');
					col1.appendChild(br);
					
					var idinput = document.createElement('input');
					idinput.setAttribute('type', 'text');
					idinput.disabled = true;
					idinput.setAttribute('value', eid);
					idinput.setAttribute('id', 'd_o_eid' + String(i));
					idinput.setAttribute('name', 'd_o_eid' + String(i));
					idinput.setAttribute('style', 'width:95%;');
					col1.appendChild(idinput);
					
					var br = document.createElement('br');
					col1.appendChild(br);
					var br = document.createElement('br');
					col1.appendChild(br);
					
					var namelbl = document.createElement('label')
					namelbl.setAttribute('for', 'd_o_ename' + String(i));
					namelbl.innerHTML = "Job Name";
					col1.appendChild(namelbl);
					
					var br = document.createElement('br');
					col1.appendChild(br);
					
					var nameinput = document.createElement('input');
					nameinput.setAttribute('type', 'text');
					nameinput.disabled = true;
					nameinput.value = ename;
					nameinput.setAttribute('id', 'd_o_ename' + String(i));
					nameinput.setAttribute('name', 'd_o_ename' + String(i));
					nameinput.setAttribute('style', 'width:95%');
					col1.appendChild(nameinput);
					
					var col2 = document.createElement('div');
					col2.setAttribute('class', 'col-6');
					row.appendChild(col2);
					
					var selectorlbl = document.createElement('label');
					selectorlbl.setAttribute('for', 'd_o_e_selector');
					selectorlbl.innerHTML = 'Select New Organization'
					col2.appendChild(selectorlbl);
					
					var br = document.createElement('br');
					col2.appendChild(br);
					
					var selector = document.createElement('select');
					selector.required = true;
					selector.setAttribute('id', 'd_o_e_selector' + String(i));
					selector.setAttribute('name', 'd_o_e_selector' + String(i));
					selector.setAttribute('style', 'min-width:95%;');
					selector.setAttribute('size', '5');
					col2.appendChild(selector);
					
					for (var j = 0; j < all_orgs.length; j++) {
						if (all_orgs[j][0] != oid) {
							var option = document.createElement('option');
							option.setAttribute('value', all_orgs[j][0]);
							option.innerHTML = all_orgs[j][1];
							selector.appendChild(option);
						}
					}
					
					var row = document.createElement('div');
					row.setAttribute('class', "row");
					parent.appendChild(row);
					var hr = document.createElement('hr');
					hr.setAttribute('style', 'width:90%;left:5%;');
					row.appendChild(hr)
					
					e_count += 1;
				}
			}
		
		}
		else {
						for (var i = 0; i < edu_split.length; i += 2) {
				if (edu_split[i] != '') {
					eid = edu_split[i];
					ename = edu_split[i+1];
					
					var row = document.createElement('div');
					row.setAttribute('class', "row");
					row.setAttribute('style', 'padding-top:15px;');
					parent.appendChild(row);
					
					var col1 = document.createElement('div');
					col1.setAttribute('class', 'col-12');
					row.appendChild(col1);
					
					var idlbl = document.createElement('label');
					idlbl.setAttribute('for', 'd_o_eid' + String(i));
					idlbl.innerHTML = "Education ID";
					col1.appendChild(idlbl);
					
					var br = document.createElement('br');
					col1.appendChild(br);
					
					var idinput = document.createElement('input');
					idinput.setAttribute('type', 'text');
					idinput.disabled = true;
					idinput.setAttribute('value', eid);
					idinput.setAttribute('id', 'd_o_eid' + String(i));
					idinput.setAttribute('name', 'd_o_eid' + String(i));
					idinput.setAttribute('style', 'width:95%;');
					col1.appendChild(idinput);
					
					var row = document.createElement('div');
					row.setAttribute('class', "row");
					row.setAttribute('style', 'padding-top:15px;');
					parent.appendChild(row);
					
					var col1 = document.createElement('div');
					col1.setAttribute('class', 'col-12');
					row.appendChild(col1);
					
					var namelbl = document.createElement('label')
					namelbl.setAttribute('for', 'd_o_ename' + String(i));
					namelbl.innerHTML = "Job Name";
					col1.appendChild(namelbl);
					
					var br = document.createElement('br');
					col1.appendChild(br);
					
					var nameinput = document.createElement('input');
					nameinput.setAttribute('type', 'text');
					nameinput.disabled = true;
					nameinput.value = ename;
					nameinput.setAttribute('id', 'd_o_ename' + String(i));
					nameinput.setAttribute('name', 'd_o_ename' + String(i));
					nameinput.setAttribute('style', 'width:95%');
					col1.appendChild(nameinput);
					
					var row = document.createElement('div');
					row.setAttribute('class', "row");
					row.setAttribute('style', 'padding-top:15px;');
					parent.appendChild(row);
					
					var col2 = document.createElement('div');
					col2.setAttribute('class', 'col-12');
					row.appendChild(col2);
					
					var selectorlbl = document.createElement('label');
					selectorlbl.setAttribute('for', 'd_o_e_selector');
					selectorlbl.innerHTML = 'Select New Organization'
					col2.appendChild(selectorlbl);
					
					var br = document.createElement('br');
					col2.appendChild(br);
					
					var selector = document.createElement('select');
					selector.required = true;
					selector.setAttribute('id', 'd_o_e_selector' + String(i));
					selector.setAttribute('name', 'd_o_e_selector' + String(i));
					selector.setAttribute('style', 'min-width:95%;');
					selector.setAttribute('size', '5');
					col2.appendChild(selector);
					
					for (var j = 0; j < all_orgs.length; j++) {
						if (all_orgs[j][0] != oid) {
							var option = document.createElement('option');
							option.setAttribute('value', all_orgs[j][0]);
							option.innerHTML = all_orgs[j][1];
							selector.appendChild(option);
						}
					}
					
					var row = document.createElement('div');
					row.setAttribute('class', "row");
					parent.appendChild(row);
					var hr = document.createElement('hr');
					hr.setAttribute('style', 'width:90%;left:5%;');
					row.appendChild(hr)
					
					e_count += 1;
				}
			}
		}
		
		var hnp = document.createElement('input');
		hnp.setAttribute('type', 'hidden');
		hnp.setAttribute('id', 'd_o_numedus');
		hnp.setAttribute('name', 'd_o_numedus');
		hnp.setAttribute('value', String(e_count));
		parent.appendChild(hnp);
	}

}

function del_org_enable() {
	document.getElementById('d_o_aname').disabled = false;
	document.getElementById('d_o_aid').disabled = false;
	document.getElementById('d_o_name').disabled = false;
	document.getElementById('d_o_id').disabled = false;
	
	for (var i = 0; i < 2048; i++) {
		if (document.getElementById('d_o_jid' + String(i)) != null) {
			document.getElementById('d_o_jid' + String(i)).disabled = false;
		}
		if (document.getElementById('d_o_eid' + String(i)) != null) {
			document.getElementById('d_o_eid' + String(i)).disabled = false;
		}
	}
}

async function upload_img(target) {

	var icon_ele = document.getElementById(target)
	file = icon_ele.files[0]
	var b64;

	var reader = new FileReader();
	reader.onload = function(event) {
	  var data = event.target.result;


	  b64 = btoa(data);
	  val_str = target + '_val';
	  document.getElementById(val_str).value = b64
	  if (target == 'e_oo_icon') {
		  document.getElementById('e_oo_img1').setAttribute('src', 'data:image/png;base64,' + b64);
	  }
	  
	  if (target == 'e_oo_header') {
		  document.getElementById('e_oo_img2').setAttribute('src', 'data:image/png;base64,' + b64);
	  }

	  var dataURLReader = new FileReader();
	  dataURLReader.onload = function(event) {
		// Parse image properties
		var dataURL = event.target.result;
		contentType = dataURL.split(",")[0].split(":")[1].split(";")[0];

		var image = new Image();
		image.src = dataURL;
		image.onload = function() {
		  console.log("Image type: " + contentType);
		  console.log("Image width: " + this.width);
		  console.log("Image height: " + this.height);
		};
	  };
	  url = dataURLReader.readAsDataURL(file);

	};
	binstr = reader.readAsBinaryString(file);



}
