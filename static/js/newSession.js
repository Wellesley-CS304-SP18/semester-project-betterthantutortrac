/*
 * filename: newSession.js
 * author: Angelina Li
 * last modified: 05/13/2018
 * description: JS code for newSession page
 */

$(document).ready( function() {
  
  var validateUserUrl = "/validateUser/";
  var userCoursesUrl = "/getUserClasses/";
  var defaultCourseText = "Select a course";
  var unknownUsernameText = "Unknown username";

  function resetSelect(selector, disabledText) {
    $(selector).empty();
    $(selector).attr("readonly", true);
    $(selector).append(
      $("<option></option>")
        .attr("selected", true)
        .attr("disabled", true)
        .text(disabledText));
  }

  function addErrorMessage(selector, errorText) {
    $(selector).append(
      $("<p></p>")
        .addClass("text-error form-text")
        .text(errorText));
  }

  function addOption(selector, optionValue, optionText) {
    $(selector).append(
      $("<option></option>")
        .attr("value", optionValue)
        .text(optionText));
  }
  
  function addUserCourses(username, dept) {
    $.post(
      userCoursesUrl,
      {"username": username, "dept": dept},
      function (data) {
        var userCourses = data.courses;
        for(i=0; i < userCourses.length; i++) {
          course = userCourses[i];
          addOption("#course", course.cid, course.name);
        }
        $("#course").attr("readonly", false);
      });
  }

  function populateFields(username, dept, valid) {
    $("#username-messages").empty();
    resetSelect("#course", defaultCourseText);

    if (valid) {
      addUserCourses(username, dept);
    } else {
      addErrorMessage("#username-messages", unknownUsernameText);
    }
  }

  $("#username").on("input", function (event) {
    var username = $(this).val();
    var dept = $("#dept").val();
    $.post(
      validateUserUrl,
      {"username": username},
      function (data) { populateFields(username, dept, data.validate); }
    );
  
  });

});
