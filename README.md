# CoursesTracker
Course Management Tool: Track and Plan Your Learning Journey with Ease
## Preview
![p1](https://github.com/MarcMarquezM/CoursesTracker/assets/55757884/9418f410-c862-4071-85b0-41289f0c0dfe)
![p2](https://github.com/MarcMarquezM/CoursesTracker/assets/55757884/a660e5e2-7a35-4d49-907c-061c74003ec4)
![p3](https://github.com/MarcMarquezM/CoursesTracker/assets/55757884/91d4f183-7724-465c-be91-a7c13de5c2cc)
## Description
The Course Progress Tracker is a desktop application developed using Python and the customtkinter library. Made to manage and monitor progress in various courses by inputing course details and control daily study time allocation per course.
## Setup
### Requirements
* Made on Python 3.11
* customtkinter
```
pip3 install customtkiner
```
### Run
```
python3 main.py
```
## Features to add
* Weekly progress window
* Days off (don't show selected courses that day).
* Info section (explain what each widget does).
* Be able to change the amount of time for progress bar (15m, 30m, 45m).
* Save data when using `Cmd + Q` or `Alt + F4`.
* Be able to change a course percentage.
* Option for no percentage needed.
## Known bugs
* If a course is close to finishing, reduce the hours per day if there are more than necessary.
* When adding a new course, if the progress of the course is not 0 (percentage done input), check how to increase percentage still by 30m.
* When leaving settings, the timer restars even if the timer length didn't change.
