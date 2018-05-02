$(document).ready( function() {

  var validateUserUrl = "/validateUser/";
  var userCoursesUrl = "/getUserClasses/";
  var userTypeUrl = "/getSessionTypes/";
  var defaultCourseText = "Select a course";
  var defaultTypeText = "Select the type of tutoring session";
  
  function syncPost( postUrl, postData, successFunction ) {
    $.ajax({
      url: postUrl,
      type: "POST",
      data: postData,
      async: false,
      success: successFunction
    });
  }

  function validateUser (username) {
    var validUser = false;
    syncPost(validateUserUrl,
      { "username": username },
      function (data) { validUser = data; }
    );
    return validUser;
  }

  function getUserCourses (username) {
    var userCourses;
    syncPost(userCoursesUrl,
      { "username": username },
      function (data) { userCourses = data; }
    );
    return userCourses;
  }

  function getSessionTypes () {
    var sessionTypes;
    syncPost(userTypeUrl, {},
      function (data) { sessionTypes = data; }
    );
    return sessionTypes;
  }

  function resetSelect (selector, disabledText) {
    $(selector).empty();
    $(selector).attr("readonly", true);
    $(selector).append(
      $("<option></option>")
        .attr("selected", true)
        .attr("disabled", true)
        .text(disabledText));
  }

  function addOption (selector, optionValue, optionText) {
    $(selector).append(
      $("<option></option>")
        .attr("value", optionValue)
        .text(optionText));
  }

  function addErrorMessage (selector, errorText) {
    $(selector).append(
      $("<p></p>")
        .addClass("text-error")
        .addClass("form-text")
        .text(errorText));
  }

  function addUserCourses (username) {
    /* first, clear course select of previous data */
    resetSelect("#course", defaultCourseText);
    var userCourses = getUserCourses(username);
    userCourses.each(function(course) {
      addOption("#course", course.id, course.name);
    })
    $("#course").attr("readonly", false);
  }

  function addTypes () {
    resetSelect("#type", defaultTypeText);
    var sessionTypes = getSessionTypes();
    sessionTypes.each(function(type) {
      addOption("#type", type, type);
    })
    $("#type").attr("readonly", false);
  }

  $("#username")
    .on("input", function (event) {
        var username = $(this).val();

        if ( validateUser(username) ) {
          $("#username-messages").empty();
          addUserCourses(username);
          addTypes();
        }
        else {
          resetSelect("#course", defaultCourseText);
          resetSelect("#type", defaultTypeText);

          $("#username-messages").empty();
          addErrorMessage("#username-messages", "Incorrect username");
        }
        
      });

});