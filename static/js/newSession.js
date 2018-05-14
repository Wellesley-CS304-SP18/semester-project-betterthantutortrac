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
  var invalidCourseText = "This user is not taking this course!";

  function resetSelect(selector, disabledText) {
    /* selector: a jQuery selector representing object(s) of type select.
     * disabledText: text to display as the default disabled select
     *   option.
     * This function will 'reset' the specified selector to its
     * default state (before the user has entered a valid username)
     * */
    $(selector).empty();
    $(selector).attr("readonly", true);
    $(selector).append(
      $("<option></option>")
        .attr("selected", true)
        .attr("disabled", true)
        .text(disabledText));
  }

  function addErrorMessage(selector, errorText) {
    /* selector: a valid jQuery selector
     * errorText: the error text to display
     * This function will add an error with text 'errorText' to the
     * specified selector
     * */
    $(selector).append(
      $("<p></p>")
        .addClass("text-error form-text")
        .text(errorText));
  }

  function addOption(selector, optionValue, optionText) {
    /* selector: a jQuery selector representing object(s) of type select.
     * optionValue: value for this option to take.
     * optionText: text for this option to display.
     * This function will add an option with value 'optionValue' and
     * text 'optionText' to the specified select object.
     * */
    $(selector).append(
      $("<option></option>")
        .attr("value", optionValue)
        .text(optionText));
  }
  
  function addUserCourses(username, dept) {
    /* username: string representing the username supplied by the user.
     * dept: string representing the department this user is selecting 
     *       courses from.
     * This function will retrieve all the courses a user is
     * a part of and will add a course option for each course.
     * */
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

  function populateFields(username, dept, validUsername, validCourse) {
    /* username: string representing the username supplied by the user.
     * dept: string representing the department this user is selecting
     *       courses from (will be none if course is already specified).
     * validUsername: boolean == 1 if username exists.
     * validCourse: boolean == 1 if student is taking the default 
     *              course specified.
     * This function will handle validating the user's request and
     * presenting the relevant courses.
     * */
    $("#username-messages").empty();
    resetSelect("#course", defaultCourseText);

    if (!validUsername) {
      addErrorMessage("#username-messages", unknownUsernameText);
    } else if (!validCourse) {
      addErrorMessage("#username-messages", invalidCourseText);
    } else {
      addUserCourses(username, dept);
    }
  }

  $("#username").on("input", function (event) {
    var username = $(this).val();
    var dept = $("#dept").val();
    $.post(
      validateUserUrl,
      {"username": username},
      function (data) { populateFields(username, dept, data.validUsername, data.validCourse); }
    );
  
  });

});
