# Module 6 
By Michael Pogue on 21Feb23

### Project Purpose
This project is designed to take incoming streaming data and monitor it in real time. Temperature flucuations will trigger an alert to the user 
should the data be outside the expected levels.

### Project Prerequisites
1. CSV data file with a similar format of the following: 
5/22/2021 16:23	261.4
5/22/2021 16:23	261.4		
5/22/2021 16:23		147.9	
5/22/2021 16:23		147.9	142.3
5/22/2021 16:23			142.3
2. Have the following modules installed: 
import pika, sys, time, os
from collections import deque
    
### Project Information
This project works by with two functions. One to check for queued data, and the other to read it and determine if there is a problem in 
the times given. The two functions are interchangeable as no unique data exists within them. To alter the name of the queue, your deque
values, or your warning triggers, simply update the variables at the beginning of the code.

# Check List
## Task 1. Open Your Existing Project
1. On your machine, open your existing streaming-05-getting-started repo in VS Code. :heavy_check_mark:
2. Create a file for your consumer (or 3 files if you'd like to use 3 consumers). :heavy_check_mark:

## Task 2. Design and Implement Each Consumer
1. Design and implement each bbq consumer. You could have one. You could have 3.  More detailed help provided in links below. :heavy_check_mark: 
2. Use the logic, approach, and structure from prior modules (use the recommended versions). :heavy_check_mark: 
3. Modifying them to serve your purpose IS part of the assignment. :heavy_check_mark: 
4. Do not start from scratch - do not search for code - do not use a notebook. ***One of these days I'm going to learn.*** :heavy_check_mark: 
5. Use comments in the code and repo to explain your work. :heavy_check_mark:  
6. Use docstring comments and add your name and date to your README and your code files. :heavy_check_mark: 

## Task 3. Professionally Present your Project
1. Explain your project in the README. :heavy_check_mark:
2. Include your name, date. :heavy_check_mark:
3. Include prerequisites and how to run your code.  :heavy_check_mark:
4. Explain and show how your project works.  :heavy_check_mark:
5. Tell us what commands are needed. Use code fencing in GitHub or backtics for inline code to share commands. :heavy_check_mark:
6. Display screenshots of your console with the producer and consumer running. :heavy_check_mark:
7. Display screenshots of at least one interesting part of the RabbitMQ console.  :heavy_check_mark:

## Requirements
In your callback function, make sure you generate alerts - there will be a smoker alert and both Food A and Food B will stall.  :heavy_check_mark:

Your README.md screenshots must show 4 concurrent processes:
1. Producer (getting the temperature readings) :heavy_check_mark:
2. Smoker monitor :heavy_check_mark:
3. Food A monitor :heavy_check_mark:
4. Food B monitor :heavy_check_mark:

In addition, you must show at least 3 significant events.

Run each terminal long enough that you can show the significant events in your screenshots:
1. Visible Smoker Alert with timestamp :heavy_check_mark:
2. Visible Food A stall with timestamp :heavy_check_mark:
3. Visible Food B stall with timestamp :heavy_check_mark:

### Proof of Viability
![image](https://user-images.githubusercontent.com/115908053/220511783-0e59619b-55a8-4878-9a62-4a4014e22c39.png)


