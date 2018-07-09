## InterviewHub

This web application is designed to let you manage interviews between as many number of interviewers and candidates.

In this application every user can see their respective options and it has a solid authentication service. Everyone who's registered though the application will be considered as a candidate. Intervierwers, in other hand, should be defined by admin through the andmin pannel which is a faily easy task. The only thing that you need to add to the user in which you've added to the interviewer model is to add the interviewer permission to it. This can be done in admin panel at `User permissions:` section.

The permission is shown as following:

    calendarapp | interviewer model | not an candidate
Also, in order to be able to run queries you should be a superuser which can be created through the following command:
    
    python3 manage.py createsuperuser
