/*
filename: newSession.js
author: Angelina Li
last modified: 05/13/2018
description: JS code for newSession page
 */

$(document).ready( function() {
  
  var validateUserUrl = "/validateUser/";
  var userCoursesUrl = "/getUserClasses/";
  var userTypeUrl = "/getSessionTypes/";
  var defaultCourseText = "Select a course";
  var defaultTypeText = "Select the type of tutoring session";
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
  
  function addUserCourses(username) {
    $.post(
      userCoursesUrl,
      {"username": username},
      function (data) {
        var userCourses = data.courses;
        for(i=0; i < userCourses.length; i++) {
          course = userCourses[i];
          addOption("#course", course.cid, course.name);
        }
        $("#course").attr("readonly", false);
      });
  }
  
  function addTypes() {
    $.post (
      userTypeUrl,
      function (data) {
        var sessionTypes = data.types;
        for(i=0; i < sessionTypes.length; i++) {
          type = sessionTypes[i];
          addOption("#type", type, type);
        }
        $("#type").attr("readonly", false);
      });
  }

  function populateFields(username, valid) {
    $("#username-messages").empty();
    resetSelect("#course", defaultCourseText);
    resetSelect("#type", defaultTypeText);

    if (valid) {
      addUserCourses(username);
      addTypes();
    } else {
      addErrorMessage("#username-messages", unknownUsernameText);
    }
  }

  $("#username").on("input", function (event) {
    var username = $(this).val();
    $.post(
      validateUserUrl,
      {"username": username},
      function (data) { populateFields(username, data.validate); }
    );
  
  });


});
