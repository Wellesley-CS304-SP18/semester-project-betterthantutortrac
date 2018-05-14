/*
filename: viewSessions.js
authors: Angelina Li, Priscilla Lee
last modified: 05/13/2018
description: JS code for viewSessions page
*/

function createUpdateModalForm(modalId, tutor, student, course, sessionType) {
	/* This function creates a modal that contains a form that allows
	a user to update a session's information. The form is auto-populated
	with the appropriate information.
	*/

	// Create the form composed of form groups (to place inside a modal).
	var tutorGroup = '<div class="form-group row">';
	tutorGroup += '<label for="tutor" class="col-sm-2">Tutor</label>';
	tutorGroup += '<div class="col-sm-8">';
	tutorGroup += '<input type="text" class="form-control" id="tutor" ';
	tutorGroup += 'placeHolder="Tutor name" value="' + tutor + '">';
	tutorGroup += '</div></div>';

	var studentGroup = '<div class="form-group row">';
  studentGroup += '<label for="student" class="col-sm-2">Student</label>';
	studentGroup += '<div class="col-sm-8">';
  studentGroup += '<input type="text" class="form-control" id="student" ';
	studentGroup += 'placeHolder="Student name" value="' + student + '">';
	studentGroup += '</div></div>';

	var courseGroup = '<div class="form-group row">';
  courseGroup += '<label for="course" class="col-sm-2">Course</label>';
	courseGroup += '<div class="col-sm-8">';
  courseGroup += '<input type="text" class="form-control" id="course" ';
	courseGroup += 'placeHolder="Course" value ="' + course + '">';
	courseGroup += '</div></div>';

	var sessionGroup = '<div class="form-group row">';
	sessionGroup += '<label for="stype" class="col-sm-2">Session type</label>';
	sessionGroup += '<div class="col-sm-8">';
  sessionGroup += '<input type="text" class="form-control" id="stype" ';
	sessionGroup += 'placeHolder="Session type" value="' + sessionType + '">';
	sessionGroup += '</div></div>';

	var form = '<form class="form-horizontal">';
	form += tutorGroup + studentGroup + courseGroup + sessionGroup;
	form += '</form>';

	// Create the modal (composed of header and body), based off of bootstrap template.
	var modalHeader = '<div class="modal-header">';
	modalHeader += '<h4 class="modal-title">Update session information</h4></div>';

	var modalBody = '<div class="modal-body">' + form + '</div>';

	var modalFooter = '<div class="modal-footer">';
	modalFooter += '<button type="button" class="btn btn-default" data-dismiss="modal">Close</button>';
	modalFooter += '<button type="button" class="btn btn-primary">Update</button>';
	modalFooter += '</div>';

	var modal = '<div id="' + modalId + '" class="modal fade" tabindex="-1" role="dialog">';
	modal += '<div class="modal-dialog modal-lg" role="document">';
	modal += '<div class="modal-content">' + modalHeader + modalBody + modalFooter + '</div></div></div>';

	// Append modal to the DOM and show it.
	$("body").append(modal);
	$("#" + modalId).modal();
}

function createDeleteModalForm(modalId) {
	/* This function creates a modal that confirms whether or not a user
	really does want to delete a given session.
	*/

	// Create the modal (composed of header and body), based off of bootstrap template.
	var modalHeader = '<div class="modal-header">';
	modalHeader += '<h4 class="modal-title">Delete session?</h4></div>';

	var modalBody = '<div class="modal-body">Do you really want to delete this session?</div>';

	var modalFooter = '<div class="modal-footer">';
	modalFooter += '<button type="button" class="btn btn-default" data-dismiss="modal">Cancel</button>';
	modalFooter += '<button type="button" class="btn btn-primary">Delete</button>';
	modalFooter += '</div>';

	var modal = '<div id="' + modalId + '" class="modal fade" tabindex="-1" role="dialog">';
	modal += '<div class="modal-dialog modal-lg" role="document">';
	modal += '<div class="modal-content">' + modalHeader + modalBody + modalFooter + '</div></div></div>';

	// Append modal to the DOM and show it.
	$("body").append(modal);
	$("#" + modalId).modal();
}

/* This chunk of code sets up the sessions tables, using the DataTable plugin.
It also binds the click event handlers to the update and delete buttons. */
$(document).ready(function() {
	$("#sessions-table").DataTable();

	/* Here is the click event handler for the update buttons. Notices that we
	bind the handler to the document because jquery fails to bind to buttons that are 
	dynamically added or that are not currently on the html page (i.e. on the 2nd page 
	of the session tables). Credit to Angelina for this clever fix.
	*/
	$(document).on("click", ".update_button", function() {
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

				createUpdateModalForm(modalId, tutor, student, course, sessionType);
			});
	});

	/* Here is the click event handler for the delete buttons. This needs to be
	implemented. TODO(priscilla).
	*/
	$(document).on("click", ".delete_button", function() {
		// Grab the sid.
		var sid = $(this).val();
		var modalId = "delete_" + sid;
		console.log("deleting session (id " + sid + ")");

		createDeleteModalForm(modalId);
	});
});
