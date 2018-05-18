# Better Than TutorTrac

Tasks:

Beta version:
* Implement quick stats based on user type
    * Some interesting questions we have the data to answer:
        * Who has been to help room most frequently?
        * Pivot table style - how many times has each student been coming to tutoring?
        * Investigative - how many people come to each type of session? How many UNIQUE people?
        * But also: obviously there are ethical problems with displaying user data, and potentially negative side effects of displaying certain numbers over others. What SHOULD we choose to implement?
        * In the LR thinking about 'what the interesting questions are' sounds like a mini project in itself.
            * What is the literature on how tutoring impacts students?
* Re-imagine the relationship between tutors, courses and sessions. Currently, there is no distinction between department level tutors and course level tutors. (The best implementation we can do for department-level tutors currently is to just assign a department level tutor to all the courses in a particular department.) This creates several problems:
    * Tutors are allowed to choose whether or not they want to act like department level tutors by clicking the 'autoPop' box.
    * Tutors are allowed to enter sessions with students that aren't recorded as having the permission to tutor.
    * Courses get inaccurate data on how often and how long tutors are tutoring for.
    * Professors assigned to courses get inaccurate data on how often department level tutors are appearing in tutoring sessions.
    * The 'autoPop' box in general is a hacky fix - tutors shouldn't have to specify whether or not all students attending the session are part of the same course. This allows 'malicious tutors' to skew our data... and also our program should just know!
    * Also, think for a while: is there ever a case where a tutor is attached to only one SECTION of a course? Or are they attached to the overall course itself?
        * Perhaps this suggests we need separate tables for departments, courses and sections??
            * This would be pretty annoying to implement though (at what level do the time columns live? Imagine the amount of joins on that SQL query too)
    * While you're at it, maybe rethink the relationship between students and tutors too. Tutoring is currently a relation between a specific student and a specific tutor. But this is a sort of awkward way to represent real life tutoring. For instance, in one helproom, each student may interact with multiple different tutors. This is both a representational problem (the information the tutors table captures is not the complete set of information about a tutoring relation we might like to capture) and is maybe just an unwieldy way to think about this in genral. Maybe we should be thinking about multiple people - tutors as well as students - as 'checking in' to a tutoring session instead? Where constraints are that at least one tutor must be present? idk.. maybe this IS the easiest / best representation.
        * What is this data ultimately going to be used for? Maybe think more about the end user's use cases first...
* Only allow users to start sessions if there are currently classes occuring (i.e. school is not yet on break)
    * Perhaps find a more extendible way to determine what the current semester and year are than hard-coding in values.
    * Also find a more extendible way to configure tutor types?
        * Tutor types should be an attribute of each course (or dept maybe)?
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
* Have some way to enforce that tutors must be students?
* Miscellaneous code quality things:
    * Standardize urls - should really be using url_for consistently
    * Should use containers on front end when we want them (e.g. on index page)
* Refactor the boolean logic in our routes!
* Allow tutors to add a list of users faster (one line per user)
* Front end bonus points:
    * Add a favicon if we'd like!
        * And if you're going to do that, might as well add a logo of some sort.
    * Update colors on viewSessions to match site wide colorscheme
    * Format dates nicer on viewSessions
