/*
filename: viewSessions.js
author: Angelina Li
last modified: 05/13/2018
description: JS code for viewSessions page
*/

$(document).ready(function() {
  $("#sessions-table").DataTable();

  $("button").click(function() {
    alert($(this).val());         
    console.log($(this).val());
  });
});
