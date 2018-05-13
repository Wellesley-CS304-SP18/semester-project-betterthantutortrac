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
	console.log("UPDATE: " + $(this).val());
    });

$(document).on("click", ".delete_button", function() {
	console.log("DELETE: " + $(this).val());
    });
});
