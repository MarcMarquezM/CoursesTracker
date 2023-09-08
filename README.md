# CoursesTracker
Track and plan your learning journey with ease, a Python and customtkinter-based desktop application.
## Preview
![Preview 1](https://github.com/MarcMarquezM/CoursesTracker/assets/55757884/9418f410-c862-4071-85b0-41289f0c0dfe)
![Preview 2](https://github.com/MarcMarquezM/CoursesTracker/assets/55757884/91d4f183-7724-465c-be91-a7c13de5c2cc)
![Preview 3](https://github.com/MarcMarquezM/CoursesTracker/assets/55757884/a660e5e2-7a35-4d49-907c-061c74003ec4)
## Description
CoursesTracker is a desktop application designed to help you manage and monitor your progress in various courses. Developed using Python and the customtkinter library, it allows you to input course details and control daily study time allocation per course, facilitating a structured approach to your learning journey.
## Setup
### Requirements
- Python 3.11
- customtkinter library
```bash
pip3 install customtkinter
```
### Run
```bash
python3 main.py
```
## Features to Add
* Weekly progress window to visualize your learning trajectory
* Days off feature to exclude selected courses on specified days
* Info section providing explanations for each widget
* Adjustable time increments for the progress bar (15m, 30m, 45m)
* Data preservation on exit using `Cmd + Q` or `Alt + F4`
* Functionality to modify course completion percentage
* Option to proceed without setting a completion percentage
## Known bugs
* Over-allocation of daily hours for courses nearing completion
* Restriction on total time input to multiples of 0.5
  * Ensure hours are inputted in base 10 format (e.g., 3.5 for 3 hours and 30 minutes)
* Issues with non-zero initial progress settings when adding a new course
  * Recommended to start with 0% progress and adjust total hours accordingly
* Timer reset issue upon exiting settings, even without changes to the timer length
