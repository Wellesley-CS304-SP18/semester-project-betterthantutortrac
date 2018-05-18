/*
filename: viewSessions.js
authors: Angelina Li, Priscilla Lee
last modified: 05/13/2018
description: JS code for viewSessions page
*/

function renderTemplate(templateSelector, data) {
  /* templateSelector: a jQuery selector representing a mustache template object.
   * data: JSON data to populate the template with.
   * This function will parse & render an object as formatted using the mustache
   * templating engine, populated with the data as specified in data.
   * */
  var template = $(templateSelector).html();
  Mustache.parse(template);
  var rendered = Mustache.render(template, data);
  return rendered;
}

function createUpdateModalForm(modalId, tutor, student, course, sessionType, sessionId) {
	/* This function creates a modal that contains a form that allows
	a user to update a session's information. The form is auto-populated
	with the appropriate information.
	*/
	$("body").append(
		renderTemplate("#update-modal-template", 
		{
			"modalId": modalId,
			"tutor": tutor,
			"student": student,
			"course": course,
			"sessionType": sessionType,
			"sessionId": sessionId
		}))
	$("#" + modalId).modal();
}

function createDeleteModalForm(modalId, sessionId) {
	/* This function creates a modal that confirms whether or not a user
	really does want to delete a given session.
	*/
	$("body").append(
		renderTemplate("#delete-modal-template", {"modalId": modalId, "sessionId": sessionId}))
	$("#" + modalId).modal();
}

/* This chunk of code sets up the sessions tables, using the DataTable plugin.
It also binds the click event handlers to the update and delete buttons. */
$(document).ready(function() {
	$("#sessions-table").DataTable();

	/* Here is the click event handler for the update buttons. Note that these are the 
	update buttons on the session table (that open the form modal). Notice that we
	bind the handler to the document because jquery fails to bind to buttons that are 
	dynamically added or that are not currently on the html page (i.e. on the 2nd page 
	of the session tables). Credit to Angelina for this clever fix.
	*/
	$(document).on("click", ".update_modal", function() {
		// Grab the sid.
		var sid = $(this).val();
		var modalId = "update_" + sid;
		console.log("updating session (id " + sid + ")");

		// Grab the form fields, using a post request, and create an update modal form.
		$.post(
			"/getSession/",
			{"sid": sid},
			function(data) {
				var tutor = data.name;
				var student = data.student;
				var course = data.dept + " " + data.courseNum + "-" + data.section;
				var sessionType = data.sessionType;

				createUpdateModalForm(modalId, tutor, student, course, sessionType, sid);
			});
	});

	/* Here is the click event handler for the delete buttons. Note that these are the
	delete buttons on the view session table (that open the delete confirmation modals),
	not the actual "confirm" delete buttons.
	implemented. TODO(priscilla).
	*/
	$(document).on("click", ".delete_modal", function() {
		// Grab the sid.
		var sid = $(this).val();
		var modalId = "delete_" + sid;
		console.log("deleting session (id " + sid + ")");

		createDeleteModalForm(modalId, sid);
	});

	/* Here is the click event handler for the "confirm" update buttons.
	*/
	$(document).on("click", ".confirm_update", function() {
		console.log($(this));
	});

	/* Here is the click event handler for the "confirm" delete buttons.
	*/
	$(document).on("click", ".confirm_delete", function() {
		console.log($(this));
		sid = $(this)[0].value;
		modalId = $(this).closest(".modal")[0].id;

		// Delete the session, using a post request.
		$.post(
			"/deleteSession/",
			{"sid": sid},
			function(data) {
				console.log("successfully deleted session " + data.sid);
				console.log("modal id " + modalId);
				$("#" + modalId).modal("hide");
				location.reload() // Force-refresh page, to remove deleted session
			});
	});

});
