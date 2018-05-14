# Better Than TutorTrac

Tasks:
* Need some validation for inserting data: should only be able to create sessions for the current term
* Definitely need to add some more commenting!!!
* Refactoring tasks:
    * Fix interactions such that find functions return only one value when appropriate (e.g. when searching on unique key)
* Testing:
    * Perhaps someone should be tasked with thinking of edge cases to try on our site
* Insert session:
    * Create interactions that will get you only the current student courses
    * Validate the courses a student is taking if 'autoPopulate' is true.
    * Given a course and a student, return the cid of the specific section the student is attending (if autoPopulate is true).

Beta version:
* Implement quick stats based on user type
