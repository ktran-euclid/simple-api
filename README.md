## Coding test


At `http://live-test-scores.herokuapp.com/scores` you'll find a service that follows the [Server-Sent Events](https://www.w3.org/TR/2015/REC-eventsource-20150203/) protocol. You can connect to the service using cURL:

        curl http://live-test-scores.herokuapp.com/scores

Periodically, you'll receive a JSON payload that represents a student's test score (a JavaScript number between 0 and 1), the exam number, and a student ID that uniquely identifies a student. For example:


        event: score
        data: {"exam": 3, "studentId": "foo", score: .991}

This represents that student foo received a score of `.991` on exam #3.

Your job is to build an application that consumes this data, processes it, and provides a simple REST API that exposes the processed results.

You may build this application in any language or stack that you prefer. You may also use any open-source libraries or resources that you find helpful.

Here's the REST API we want you to build:

1. A REST API `/students` that lists all users that have received at least one test score
2. A REST API `/students/{id}` that lists the test results for the specified student, and provides the student's average score across all exams
3. A REST API `/exams` that lists all the exams that have been recorded
4. A REST API `/exams/{number}` that lists all the results for the specified exam, and provides the average score across all students

Coding tests are often contrived, and this exercise is no exception. To the best of your ability, make your solution reflect the kind of code you'd want shipped to production. A few things we're specifically looking for:


* Well-structured, well-written, idiomatic, safe, performant code.
* Tests, reflecting the level of testing you'd expect in a production service.
* Good RESTful API design. Whatever that means to you, make sure your implementation reflects it, and be able to defend your design.
* Ecosystem understanding. Your code should demonstrate that you understand whatever ecosystem you're coding against— including project layout and organization, use of third party libraries, and build tools.

That said, we'd like you to cut some corners so we can focus on certain aspects of the problem:


* Store the results in memory instead of a persistent store. In production code, you'd never do this, of course.
* Since you're storing results in memory, you don't need to worry about the “ops” aspects of deploying your service— load balancing, high availability, deploying to a cloud provider, etc. won't be necessary.


That's it. Commit your solution to the provided GitHub repository (this one).  When you come in, we'll pair with you and  walk through your solution and extend it in an interesting way.


## Setup the application

This application has three main parts:
1. A WSGI Flask application to serve as the REST API, responding to external requests
2. A Celery application to execute background task such as fetching data from the given sse content server
3. A Redis server being used by Celery to process tasks and also serves as a in memory database for a. and b.

In order to setup the testing environment and start a local server, please follow these steps:
0. Install the components:

    Flask

        pip install --editable .

    Celery and Redis

        pip install -U "celery[redis]"

    pytest watch for watching the test

        pip install pytest-watch

1. To start the Flask application:

        flask run

2. On a separate window, to watch the test suite:

        ptw

3. On another window, start celery worker and watch their logs.  This worker is required to fetch data from content-server

        celery -A application.application.celery worker --loglevel=info

4. Optionally, we can check for redis service to see if data goes in there. If you install redis correctly

        redis-cli

should bring you to the right place. Redis comes in default with 3 data store. Database index 1 and 2 are stores where data from the content-server is being saved.  Database index 0 is what celery app uses to process tasks

5. And voila, your server is ready at 127.0.0.1:5000.  As requested in the documentation above, only 4 endpoints are available

        127.0.0.1:5000/students
        127.0.0.1:5000/students/<student_name>
        127.0.0.1:5000/exams/
        127.0.0.1:5000/exams/<exam_id>

6. I have added an extra filter to toggle the display. This filter should not affect average score

        127.0.0.1:5000/students/<student_name>?exam_id=''
        127.0.0.1:5000/exams/exam_id?student_name=''

7. Pagination ?
