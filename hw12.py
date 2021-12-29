#!/usr/bin/env python
"""
Name:	Craig Opie
Class: 	CENT110
File:	hw12.py

Algorithm:
1)  Import BeautifulSoup from bs4.
2)  Import dumps from json.
3)  Create a function to open an XML file:
    A)  Open the filename as infile:
        1.  Read infile and store in 'contentsIn'.
        2.  Return 'contentsIn'.
4)  Create a function to process information for each student:
    A)  Create a list to store the information from the students.
    B)  For each person in 'students':
        1.  Create a dictionary called 'student'.
        2.  Create a list called 'scoresList'.
        3.  Store the person's name in 'name'.
        4.  Store the person's major in 'major'.
        5.  Store the person's scores in 'scores'.
        6.  Split the information in 'scores' everywhere there is a
            comma.
        7.  For each score in 'scores':
            a.  Add the score as a float to the list 'scoresList'.
        8.  Add the person's name to the 'student' dictionary.
        9.  Add the person's major to the 'student' dictionary.
        10. Add the person's 'scoresList' to the 'student' dictionary.
        11. Add the 'student' dictionary to the 'studentsList'.
    C)  Return 'studentsList'.
5)  Create a function to process information about the courses:
    A)  Create a dictionary called 'coursesDict'.
    B)  Create a dictionary called 'titlesDict'.
    C)  Create a list called 'weightsList'.
    D)  For each course in 'courses':
        1.  Store the course's title in 'title'.
        2.  Store the course's weight in 'weight'.
        3.  Split the information in 'weight' everywhere there is a
            comma.
        4.  Add 'title' to the 'titlesDict'.
        5.  For each weight in 'weight':
            a.  Add each to the list 'weightsList'.
        7.  Add 'titles' from 'titlesDict' and 'weights' from
            'weightsList' to 'coursesDict'.
        8.  Return 'coursesDict'.
6)  Create a function to save the processed content to a JSON file:
    A)  Create a JSON file using the provided filename and assign to
        'outfile'.
        1.  Write 'contentsOut' in JSON format using 'dumps' to
            'outfile'.
7)  Run the 'openXML' fuction providing the filename and assign to
    'contentsIn'.
8)  Parse 'contentsIn' using BeautifulSoup and assign to 'soup'.
9)  Filter through the soup and find all tags labeled 'student' and
    assign to 'students'.
10) Filter through the soup and find all tags labeled 'course' and
    assign to 'courses'.
11) Run the 'processStudents' function and assign to 'studentsList'.
12) Run the 'processCourses' function and assign to 'coursesDict'.
13) Create a dictionary called 'recordsDict'.
14) Add 'studnetsList' and 'coursesDict' to 'recordsDict'.
15) Run the 'writeJSON' function with 'recordsDict'.
"""
from bs4 import BeautifulSoup as bs
from json import dumps

def openXML(filename):
    """ This function opens an XML file, reads the contents, and returns the
    contents to the user.
    Args:
        filename (str): The only parameter.  Used to specify the filename to
        parse.
    Returns:
        Block String with entire contents of the file specified.
    """
    with open(filename) as infile:
        contentsIn = infile.read()
        return(contentsIn)

def processStudents(students):
    """ This function processes each person in 'students' using lists,
    dictionaries, and for loops to identify a person's name, major, and
    scores.  The values are then added to 'studentsList' and returned to the
    user.
    Args:
        students (str): The only parameter.  Used to specify the list of
        dictionaries to parse.
    Returns:
        A list of dictionaries for each student which contains the person's
        name, major, and scores.
    """
    studentsList = []
    for person in students:
        student = {}
        scoresList = []
        name = person.find("name").get_text()
        major = person.find("major").get_text()
        scores = person.find("scores").get_text()
        scores = scores.split(",")
        for each in scores:
            scoresList.append(float(each))
        student["name"] = name
        student["major"] = major
        student["scores"] = scoresList
        studentsList.append(student)
    return(studentsList)

def processCourses(courses):
    """ This function processes each course in 'courses' using lists,
    dictionaries, and for loops to identify the courses', title, and weight of
    each assignment. The values are then added to 'coursesDict' and returned to
    the user.
    Args:
        courses (str): The only parameter.  Used to specify the list of
        dictionaries to parse.
    Returns:
        A dictionaries for each course which contains the courses' title and
        weight of each assignment.
    """
    coursesDict = {}
    titlesDict = {}
    weightsList = []
    for course in courses:
        title = course.find("titles").get_text()
        weight = course.find("weights").get_text()
        weight = weight.split(",")
        titlesDict["titles"] = title
        for each in weight:
            weightsList.append(float(each))
        coursesDict["course"] = {"titles":titlesDict["titles"], \
        "weights":weightsList}
        return(coursesDict)

def writeJSON(filename, contentsOut):
    """ This function creates a JSON file, using the 'contentsOut' and
    'filename' specified by the user.
    Args:
        filename (str): The first parameter.  Used to specify the filename to
        create.
        contentsOut (str): The Second parameter.  Used to specify the contents
        of the file to write.
    """
    with open(filename, "w") as outfile:
        outfile.write(dumps(contentsOut, indent=2, separators=(","," : "), \
        sort_keys=False))

# Loads the information in 'hw12.xml' and assigns to 'contentsIn'
contentsIn = openXML("hw12.xml")

# Uses BeautifulSoup to filter through the 'soup' to get the major XML tags:
# 'studnets' and 'courses'
soup = bs(contentsIn, "xml")
students = soup.find_all("student")
courses = soup.find_all("course")

# Processes the soup's information for 'students' and 'courses' using functions
studentsList = processStudents(students)
coursesDict = processCourses(courses)

# Create's a new dictionary and stores the culmination of information to
# represent a JSON format
recordsDict = {}
recordsDict["records"] = {"students":studentsList, \
"course":coursesDict["course"]}

# Writes the information in 'recordsDict' to the JSON file
writeJSON("hw12.json", recordsDict)
