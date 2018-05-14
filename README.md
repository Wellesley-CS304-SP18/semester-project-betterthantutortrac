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
    * Also, think for a while: is there ever a case where a tutor is attached to only one SECTION of a course? Or are they attached to the overall course itself?
        * Perhaps this suggests we need separate tables for departments, courses and sections??
            * This would be pretty annoying to implement though (at what level do the time columns live? Imagine the amount of joins on that SQL query too)
* If the tutor forgets to log out of a session, when their session data is popped, you should automatically infer their logout time, and then warn them not to do that again.
    * Alternatively, if a tutor forgets to log out of a session somehow, maybe nag at them until they log out.
        * e.g. keep on sending them annoying flashed messages until they log out. Although, this seems worse for data accuracy.
* Only allow users to start sessions if there are currently classes occuring (i.e. school is not yet on break)
    * Perhaps find a more extendible way to determine what the current semester and year are than hard-coding in values.
    * Also find a more extendible way to configure tutor types?
* Update js to use templating instead of manually creating strings
* In view sessions:
    * Either: only display current sessions, or add in time columns
    * when clicking update, should bring up a window displaying all possible values we can update
        * validate update such that you cannot insert incorrect data
    * Think about it: is our update page html safe?
    * Consider: instead of having an update button (or in addition to having an update button), allow users to click on fields to update them directly (excel style)
* Testing:
    * Find some way to test professor level data (may want to disable our CAS system for a while)
* Sessions and data storage:
    * Currently there is some overlap between the way we are relying on CAS provided cookies and data in our own database. It happens to be the case that these data correspond well given username keys. However, we might want to rethink this relationship for the future.
        * Furthermore, consider whether usernames will always be dependable keys - do usernames ever change?
* Go over all our sql queries:
    * Just verify again: are our sql queries (especially when we are manipulating raw query strings) safe to injections?
    * Think about how we can collapse our queries more. e.g., it might be preferable to have general use find functions that use long conditionals to grab the relevant data instead of multiple specific use functions.
* Miscellaneous code quality things:
    * Standardize urls - should really be using url_for consistently
    * Should use containers on front end when we want them (e.g. on index page)
    * should go through and change snake cased functions / routes / etc. to camel case
* Refactor the boolean logic in our routes!
* Front end bonus points:
    * Add a favicon if we'd like!
    * Update colors on viewSessions to match site wide colorscheme
    * Format dates nicer on viewSessions
