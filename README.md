# Better Than TutorTrac

Tasks:
* Need some validation for inserting data: should only be able to create sessions for the current term
* Definitely need to add some more commenting!!!
* Refactoring tasks:
    * Fix interactions such that find functions return only one value when appropriate (e.g. when searching on unique key)
* Testing:
    * Perhaps someone should be tasked with thinking of edge cases to try on our site

Beta version:
* Implement quick stats based on user type
* Re-imagine the relationship between tutors, courses and sessions. Currently, there is no distinction between department level tutors and course level tutors. (The best implementation we can do for department-level tutors currently is to just assign a department level tutor to all the courses in a particular department.) This creates several problems:
    * Tutors are allowed to choose whether or not they want to act like department level tutors by clicking the 'autoPop' box.
    * Tutors are allowed to enter sessions with students that aren't recorded as having the permission to tutor.
    * Courses get inaccurate data on how often and how long tutors are tutoring for.
    * Professors assigned to courses get inaccurate data on how often department level tutors are appearing in tutoring sessions.
    * The 'autoPop' box in general is a hacky fix - tutors shouldn't have to specify whether or not all students attending the session are part of the same course. This allows 'malicious tutors' to skew our data... and also our program should just know!
* If the tutor forgets to log out of a session, when their session data is popped, you should automatically infer their logout time, and then warn them not to do that again.
    * Alternatively, if a tutor forgets to log out of a session somehow, maybe nag at them until they log out.
        * e.g. keep on sending them annoying flashed messages until they log out. Although, this seems worse for data accuracy.
* Update js to use templating instead of manually creating strings
* Refactor the boolean logic in our routes!
* Front end bonus points:
    * Add a favicon if we'd like!
    * Update colors on viewSessions to match site wide colorscheme
    * Format dates nicer on viewSessions
