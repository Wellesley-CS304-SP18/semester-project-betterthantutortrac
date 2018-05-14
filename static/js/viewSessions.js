/*
filename: viewSessions.js
authors: Angelina Li, Priscilla Lee
last modified: 05/13/2018
description: JS code for viewSessions page
*/

$(document).ready(function() {
$("#sessions-table").DataTable();

// Bind to the table, because fails to bind to buttons that are dynamically added
// or that are not on the html page (i.e. on the 2nd page of the session tables).
// Credit to Angelina for this clever fix.
$(document).on("click", ".update_button", function() {
	// Grab the sid and the form fields.
	var sid = $(this).val();
	var modalId = "update_" + sid;
	var tutor = "Priscilla";
	var student = "Kate";
	var course = "CS 230";
	var sessionType = "Help Room";	

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

	console.log("updating session (id " + sid + ")");
    });

$(document).on("click", ".delete_button", function() {
	
	console.log("DELETE: " + $(this).val());
    });
});
