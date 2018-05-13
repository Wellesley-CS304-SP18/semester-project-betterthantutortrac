/*
 * filename: startTutorSession.js
 * author: Angelina Li
 * last modified: 05/13/2018
 * description: adding short handler to index page
 */

$(document).ready( function () {

  $("#course").on("change", function() {
    var course = $(this).find(":selected").text();
    $("#courseName").text(course);
  });

});
