from tkinter import messagebox, END, NORMAL, DISABLED, CENTER, LEFT
from datetime import datetime
import customtkinter as ctk
from platform import system
from math import floor
import json
import os

from Course import Course

# ---------------------- VARIABLES AND SET-UP ----------------------- #

system = system()
date: str = str(datetime.now().date())
last_day_saved: str = ""
courses: [Course] = []
selected_courses: [
    [Course, float, int, float]] = []  # float for hours per day and int for days taken and a float for current hours
streaks: int = 0
top_level_open: bool = False
timer_length: int = 0
appearance: str = ""
color_scheme: str = ""
max_courses: int = 0
CANCEL_BTN_COLOR: str = "#909190"
CANCEL_BTN_HOVER_COLOR: str = "#787878"


# ----------------- UNSELECT COURSES SETTINGS CLASS ----------------- #


class UnselectCoursesSettings(ctk.CTkToplevel):
    def __init__(self, *args, num_courses_unselect, **kwargs):
        super().__init__(*args, **kwargs)
        self.num_courses_unselect = num_courses_unselect
        self.total = 0

        self.attributes("-topmost", True)
        self.lift()
        self.grab_set()
        self.title("Settings")
        self.resizable(width=False, height=False)

        self.header_lbl = ctk.CTkLabel(
            master=self,
            text=f"Unselect {self.num_courses_unselect} course" if self.num_courses_unselect == 1 else
            f"Unselect {self.num_courses_unselect} courses",
            wraplength=150
        )
        self.header_lbl.grid(row=0, column=0, padx=20, pady=(10, 0))

        # Add selected courses checkbox
        self.selected_courses_check = []
        for i in range(len(selected_courses)):
            self.selected_courses_check.append(
                ctk.CTkCheckBox(
                    master=self,
                    text=selected_courses[i][0].name
                )
            )
            self.selected_courses_check[i].grid(row=i + 1, column=0, padx=20, pady=10, sticky="W")

        # Add checkbox commands
        for sel_course in self.selected_courses_check:
            sel_course.configure(command=lambda s=sel_course: self.checkbox_event(s))

        btn_row = self.grid_size()[1]

        self.cancel_btn = ctk.CTkButton(
            master=self,
            text="Cancel",
            width=60,
            fg_color=CANCEL_BTN_COLOR,
            hover_color=CANCEL_BTN_HOVER_COLOR,
            command=self.close_window
        )
        self.cancel_btn.grid(row=btn_row, column=0, padx=20, pady=10, sticky="W")

        self.save_btn = ctk.CTkButton(master=self, text="Save", width=60, command=self.save, state=DISABLED)
        self.save_btn.grid(row=btn_row, column=0, padx=20, pady=10, sticky="E")

        # Bind window
        self.bind("<Key>", self.check_bind)

    def check_bind(self, event):
        if event.keysym == "Escape":
            self.close_window()
        elif event.keysym == "Return" and self.save_btn.cget("state") == NORMAL:
            self.save()

    def checkbox_event(self, checkbox):
        if checkbox.get() == 1:
            self.total += 1
        else:
            self.total -= 1

        if self.total == self.num_courses_unselect:
            for lst in self.selected_courses_check:
                if lst.get() == 0:
                    lst.configure(state=DISABLED)
            self.save_btn.configure(state=NORMAL)
        else:
            for lst in self.selected_courses_check:
                if lst.get() == 0:
                    lst.configure(state=NORMAL)
            self.save_btn.configure(state=DISABLED)

    def close_window(self):
        self.destroy()
        self.update()
        self.master.lift()

    def save(self):
        for i in range(len(self.selected_courses_check)):
            # Check for those courses which where selected
            if self.selected_courses_check[i].get() == 1:
                for selected_course in selected_courses:
                    if self.selected_courses_check[i].cget("text") == selected_course[0].name:
                        selected_courses.remove(selected_course)
                        break

        self.close_window()


# -------------------------- SETTINGS CLASS ------------------------- #


class Settings(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.attributes("-topmost", True)
        self.lift()
        self.grab_set()
        self.title("Settings")
        self.resizable(width=False, height=False)

        # Select appearance label
        self.appearance_lbl = ctk.CTkLabel(master=self, text="Select theme")
        self.appearance_lbl.grid(row=0, column=0, padx=(20, 10), pady=(10, 5), sticky="W")

        # Select appearance option menu
        self.appearance_option_menu = ctk.CTkOptionMenu(master=self, values=["Light", "Dark", "System"])
        self.appearance_option_menu.grid(row=0, column=1, padx=(10, 20), pady=(10, 5))
        self.appearance_option_menu.set(appearance.capitalize())

        # Select color scheme label
        self.color_scheme_label = ctk.CTkLabel(master=self, text="Select color scheme")
        self.color_scheme_label.grid(row=1, column=0, padx=(20, 10), pady=(10, 5), sticky="W")

        # Select color scheme option menu
        self.color_scheme_option_menu = ctk.CTkOptionMenu(master=self, values=["Blue", "Dark-blue", "Green"])
        self.color_scheme_option_menu.grid(row=1, column=1, padx=(10, 20), pady=(10, 5))
        self.color_scheme_option_menu.set(color_scheme.capitalize())

        # Timer length label
        self.timer_length_lbl = ctk.CTkLabel(master=self, text="Timer length")
        self.timer_length_lbl.grid(row=2, column=0, padx=(20, 10), pady=(10, 5), sticky="W")

        # Timer length SpinBox
        self.timer_length_spinbox = SpinBox(master=self, width=140, height=28, step_size=15)
        self.timer_length_spinbox.grid(row=2, column=1, padx=(10, 20), pady=(10, 5))
        self.timer_length_spinbox.set_value(float(timer_length))
        self.timer_length_spinbox.subtract_btn.configure(state=NORMAL)

        # Max courses label
        self.max_courses_lbl = ctk.CTkLabel(master=self, text="Max number of courses", wraplength=124, justify=LEFT)
        self.max_courses_lbl.grid(row=3, column=0, padx=(20, 10), pady=(10, 5), sticky="W")

        # Max courses selector
        self.max_courses_selector = ctk.CTkSegmentedButton(master=self, width=140, height=28, values=["1", "2", "3"])
        self.max_courses_selector.grid(row=3, column=1, padx=(10, 20), pady=(10, 5))
        self.max_courses_selector.set(str(max_courses))

        # Cancel button
        self.cancel_btn = ctk.CTkButton(
            master=self,
            text="Cancel",
            width=50,
            fg_color=CANCEL_BTN_COLOR,
            hover_color=CANCEL_BTN_HOVER_COLOR,
            command=self.close_window
        )
        self.cancel_btn.grid(row=4, column=0, padx=(20, 10), pady=(5, 10))

        # Apply button
        self.apply_btn = ctk.CTkButton(master=self, text="Apply", width=50, state=DISABLED, command=self.apply)
        self.apply_btn.grid(row=4, column=1, padx=(10, 20), pady=(5, 10))

        # Bind window
        self.bind("<Button-1>", self.check_bind)
        self.bind("<Key>", self.check_bind)

    def check_bind(self, event):
        if event.keysym == "Escape":
            self.close_window()
        elif event.keysym == "Return" and self.apply_btn.cget("state") == NORMAL:
            self.apply()
        else:
            if appearance != self.appearance_option_menu.get().lower() or \
                    color_scheme != self.color_scheme_option_menu.get().lower() or \
                    (timer_length != int(self.timer_length_spinbox.get_value()) and int(
                        self.timer_length_spinbox.get_value()) != 0) or \
                    max_courses != int(self.max_courses_selector.get()):
                # Enable apply button
                self.apply_btn.configure(state=NORMAL)
            else:
                self.apply_btn.configure(state=DISABLED)

    def close_window(self):
        self.destroy()
        self.update()
        self.master.lift()

    def apply(self):
        global appearance, color_scheme, timer_length, max_courses
        # Change appearance value
        appearance = self.appearance_option_menu.get().lower()
        # Check if color scheme changed
        if color_scheme != self.color_scheme_option_menu.get().lower():
            # We need to restart the app
            self.bell()
            self.master.lift()
            self.attributes("-topmost", False)
            messagebox.showinfo(
                title="Restart required",
                message="To change the color scheme you must restart the app.",
                parent=self.master
            )
            self.attributes("-topmost", True)
            self.lift()
            # Only change the value
            color_scheme = self.color_scheme_option_menu.get().lower()
        # Check if new max_courses value is less than before
        if max_courses > int(self.max_courses_selector.get()):
            # One or more courses must be unselected
            self.bell()
            self.master.lift()
            self.attributes("-topmost", False)
            confirm = messagebox.askyesno(
                title="Courses must be unselected",
                message="To change the max number of courses, some of the courses you have selected must be unselected first,"
                        " are you sure?",
                parent=self.master
            )
            self.attributes("-topmost", True)
            self.lift()

            if confirm:
                # Open UnselectCoursesSettings
                self.attributes("-topmost", False)
                num_courses_unselect = max_courses - int(self.max_courses_selector.get())
                window = UnselectCoursesSettings(num_courses_unselect=num_courses_unselect)
                window.wait_window()

                self.attributes("-topmost", True)
                # Check if we did unselect the necessary courses
                if num_courses_unselect == window.total:
                    # Total unselected is correct, change max_courses value
                    max_courses = int(self.max_courses_selector.get())

        # Change timer length value
        timer_length = int(self.timer_length_spinbox.get_value())

        ctk.set_appearance_mode(appearance)
        self.close_window()


# -------------------------- SPINBOX CLASS -------------------------- #


class SpinBox(ctk.CTkFrame):
    def __init__(self, *args, width: int = 100, height: int = 32, step_size=1.0, extra_time=True, **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.step_size = step_size
        self.extra_time = extra_time

        self.value = 0.0

        self.configure(fg_color=('gray78', 'gray28'))
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)

        self.subtract_btn = ctk.CTkButton(
            master=self,
            text='-',
            width=height - 6,
            height=height - 6,
            state=DISABLED if self.value == 0.0 else NORMAL,
            command=lambda: self.value_btn(False)
        )
        self.subtract_btn.grid(row=0, column=0, padx=(3, 0), pady=3)

        self.entry = ctk.CTkEntry(master=self, width=width - (2 * height), height=height - 6, border_width=0)
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky='EW')
        self.entry.insert(0, self.value)

        self.add_btn = ctk.CTkButton(
            master=self,
            text='+',
            width=height - 6,
            height=height - 6,
            state=DISABLED if self.value == 3.0 and not self.extra_time else NORMAL,
            command=lambda: self.value_btn(True)
        )
        self.add_btn.grid(row=0, column=2, padx=(0, 3), pady=3)

        self.entry.configure(state=DISABLED)
        self.update()
        self.update_idletasks()

    def get_value(self):
        return self.value

    def reset(self):
        self.subtract_btn.configure(state=DISABLED)
        self.add_btn.configure(state=NORMAL)
        self.entry.configure(state=NORMAL)
        self.value = 0.0
        self.entry.delete(0, END)
        self.entry.insert(0, self.value)
        self.entry.configure(state=DISABLED)

    def set_value(self, value):
        self.value = value
        self.entry.configure(state=NORMAL)
        self.entry.delete(0, END)
        self.entry.insert(0, self.value)
        self.entry.configure(state=DISABLED)

    def value_btn(self, add):
        if add:
            self.value = float(self.entry.get()) + self.step_size
        else:
            self.value = float(self.entry.get()) - self.step_size
        self.entry.configure(state=NORMAL)
        self.entry.delete(0, END)
        self.entry.insert(0, self.value)
        self.subtract_btn.configure(state=DISABLED if self.value == 0 else NORMAL)
        self.entry.configure(state=DISABLED)
        if not self.extra_time:
            self.check_btn_values()

    def check_btn_values(self):
        self.add_btn.configure(state=DISABLED if self.value == 2.5 else NORMAL)


# ---------------------- WEEKLY PROGRESS CLASS ---------------------- #


class WeeklyProgress(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# ------------------------ ADD COURSE CLASS ------------------------- #


class AddCourseWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.attributes("-topmost", True)
        self.lift()
        self.grab_set()
        self.title("")
        self.resizable(width=False, height=False)

        # Add a course header
        self.header = ctk.CTkLabel(master=self, text="Add a Course", font=("", 15, "normal"))
        self.header.grid(row=0, column=0, columnspan=2, pady=5)

        # Course name label
        self.course_name_lbl = ctk.CTkLabel(master=self, text="Name:")
        self.course_name_lbl.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="W")

        # Add a char limit to name entry
        self.validate_command = self.register(self.limit_char)

        # Course name entry
        self.course_name_entry = ctk.CTkEntry(
            master=self,
            placeholder_text="Name",
            validate="key",
            validatecommand=(self.validate_command, "%P")
        )
        self.course_name_entry.grid(row=1, column=1, padx=(10, 20), pady=10)

        # Course hours label
        self.course_hours_lbl = ctk.CTkLabel(master=self, text="Hours:")
        self.course_hours_lbl.grid(row=2, column=0, padx=(20, 10), pady=10, sticky="W")

        # Course hours entry
        self.course_hours_entry = ctk.CTkEntry(master=self, placeholder_text="Enter hours")
        self.course_hours_entry.grid(row=2, column=1, padx=(10, 20), pady=10)

        # Course percentage done label
        self.course_percentage_done_lbl = ctk.CTkLabel(master=self, text="Percentage done:", wraplength=74,
                                                       justify=LEFT)
        self.course_percentage_done_lbl.grid(row=3, column=0, padx=(20, 10), pady=10, sticky="W")

        # Course percentage done entry
        self.course_percentage_done_entry = ctk.CTkEntry(master=self)
        self.course_percentage_done_entry.grid(row=3, column=1, padx=(10, 20), pady=10)
        self.course_percentage_done_entry.insert(0, "0")

        # Cancel button
        self.cancel_btn = ctk.CTkButton(
            master=self,
            text="Cancel",
            width=60,
            fg_color=CANCEL_BTN_COLOR,
            hover_color=CANCEL_BTN_HOVER_COLOR,
            command=self.close_window
        )
        self.cancel_btn.grid(row=4, column=0, columnspan=2, padx=(65, 10), pady=20, sticky="W")

        # Save button
        self.save_btn = ctk.CTkButton(master=self, text="Save", width=60, state=DISABLED, command=self.save)
        self.save_btn.grid(row=4, column=0, columnspan=2, padx=(10, 65), pady=20, sticky="E")

        # Bind window
        self.bind("<Button-1>", self.check_bind)
        self.bind("<Key>", self.check_bind)

    def check_bind(self, event):
        if event.keysym == "Escape":
            self.close_window()
        elif event.keysym == "Return" and self.save_btn.cget("state") == NORMAL:
            self.save()
        else:
            if len(self.course_name_entry.get()) != 0 and \
                    len(self.course_hours_entry.get()) != 0 and \
                    len(self.course_percentage_done_entry.get()) != 0:
                self.save_btn.configure(state=NORMAL)
            else:
                self.save_btn.configure(state=DISABLED)

    @staticmethod
    def limit_char(content):
        if len(content) > 20:
            return False
        return True

    def close_window(self):
        self.destroy()
        self.update()
        self.master.lift()

    def save(self):
        course_name = self.course_name_entry.get()
        try:
            # Get the float value of hours and percentage_done
            hours = float(self.course_hours_entry.get())
            percentage_done = float(self.course_percentage_done_entry.get())
        except ValueError or TypeError:
            # Values are not a num
            self.del_values("One or some values are wrongly entered")
        else:
            if course_name in [course.name for course in courses]:
                # Course already exists
                self.del_values(f"Course {course_name} already exists.")
            elif hours == 0:
                # Hours cannot be 0
                self.del_values("Hours cannot be 0.")
            elif hours % 0.5 != 0:
                # Hours must be divisible by 30m
                self.del_values("Hours must be divisible by 30 minutes.")
            else:
                # Add course and close window
                courses.append(Course(name=course_name, hours=hours, percentage=percentage_done))
                self.bell()
                self.close_window()
                messagebox.showinfo(title="SUCCESS", message="Successfully added new course.", parent=self.master)

    def del_values(self, message):
        # Error messagebox
        self.bell()
        self.master.lift()
        self.attributes("-topmost", False)
        messagebox.showerror(
            title="ERROR",
            message=message,
            parent=self.master
        )
        self.course_hours_entry.delete(0, END)
        self.course_percentage_done_entry.delete(0, END)
        self.course_percentage_done_entry.insert(0, "0")
        self.attributes("-topmost", True)
        self.lift()


# ------------------------ DEL COURSE CLASS ------------------------- #


class DelCourseWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.attributes("-topmost", True)
        self.lift()
        self.grab_set()
        self.title("")
        self.resizable(width=False, height=False)

        # Delete a course header
        self.header = ctk.CTkLabel(master=self, text="Delete a course", font=("", 15, "normal"))
        self.header.grid(row=0, column=0, pady=5)

        # Option menu for courses to delete
        self.option_menu = ctk.CTkOptionMenu(
            master=self,
            values=[course.name for course in courses],
            dynamic_resizing=False
        )
        self.option_menu.grid(row=1, column=0, pady=10, padx=20)

        # Cancel button
        self.cancel_btn = ctk.CTkButton(
            master=self,
            text="Cancel",
            width=60,
            fg_color=CANCEL_BTN_COLOR,
            hover_color=CANCEL_BTN_HOVER_COLOR,
            command=self.close_window
        )
        self.cancel_btn.grid(row=2, column=0, padx=20, pady=20, sticky="W")

        # Delete course button
        self.del_button = ctk.CTkButton(master=self, text="Delete", width=60, command=self.delete_course)
        self.del_button.grid(row=2, column=0, padx=20, pady=20, sticky="E")

        # Bind window
        self.bind("<Key>", self.check_bind)

    def check_bind(self, event):
        if event.keysym == "Escape":
            self.close_window()
        elif event.keysym == "Return":
            self.delete_course()

    def close_window(self):
        self.destroy()
        self.update()
        self.master.lift()

    def delete_course(self):
        course_name = self.option_menu.get()
        # First confirm is want to delete
        self.bell()
        self.master.lift()
        self.attributes("-topmost", False)
        confirm = messagebox.askyesno(
            title="Confirm",
            message=f"You are about to delete course: {course_name}, are you sure?",
            parent=self.master
        )
        if confirm:
            # Delete course from list of courses
            for course in courses:
                if course_name == course.name:
                    courses.remove(course)
                    break
            # Delete course from list of chosen courses
            for selected_course in selected_courses:
                if course_name == selected_course[0].name:
                    selected_courses.remove(selected_course)
                    break
            # Update and close window
            self.bell()
            self.close_window()
            messagebox.showinfo(title="SUCCESS", message="Successfully deleted course", parent=self.master)
        else:
            self.attributes("-topmost", True)
            self.lift()


# ----------------------- COURSE FRAME CLASS ------------------------ #


class CourseFrame(ctk.CTkFrame):
    def __init__(self, selected_course_num, selected_course, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_propagate(False)

        self.selected_course_num = selected_course_num
        self.selected_course = selected_course
        # If hours per day is more than the hours left on the course, reduce the time
        if self.selected_course[0].hours_left < self.selected_course[1]:
            self.selected_course[1] = self.selected_course[0].hours_left
        # Time left on course for the day
        self.time_left = self.selected_course[1] - self.selected_course[3]  # Hours per day - current hours
        # Beginning progress value for progress bar
        self.beginning_progress_value = self.selected_course[3] / self.selected_course[
            1]  # Current hours / hours per day
        # Steps size
        self.step = 0.5 / self.selected_course[1]  # step of 30 min divided by the hours per day
        # Done for today
        self.done = True if self.time_left == 0 else False

        # Course name label
        self.course_name_lbl = ctk.CTkLabel(
            master=self,
            text=f"Course #{self.selected_course_num + 1}: {self.selected_course[0].name}",
            font=("Courier", 20, "normal")
        )
        self.course_name_lbl.grid(row=0, column=0, columnspan=2, padx=10, pady=(1, 0), sticky="W")

        # Progress frame
        self.progress_frame = ctk.CTkFrame(master=self, width=28)
        self.progress_frame.grid(row=1, column=0, padx=10, pady=(2, 0), sticky="W")

        # Hours per day progress bar minus button
        self.hours_per_day_minus_btn = ctk.CTkButton(
            master=self.progress_frame,
            text="-30m",
            width=50,
            height=20,
            font=("", 11),
            state=DISABLED if self.time_left == self.selected_course[1] or self.time_left == 0 else NORMAL,
            command=self.dec_percentage
        )
        self.hours_per_day_minus_btn.grid(row=0, column=0, padx=5, pady=4)

        # Hours per day progress bar
        self.hours_per_day_progress_bar = ctk.CTkProgressBar(master=self.progress_frame, width=250, height=20,
                                                             mode="determinate")
        self.hours_per_day_progress_bar.grid(row=0, column=1, padx=5, pady=4)
        # Set the progress bar based on the current hours
        self.hours_per_day_progress_bar.set(self.beginning_progress_value)

        # Hours per day progress bar plus button
        self.hours_per_day_plus_btn = ctk.CTkButton(
            master=self.progress_frame,
            text="+30m",
            width=50,
            height=20,
            font=("", 11),
            state=DISABLED if self.time_left == 0 else NORMAL,
            command=self.inc_percentage
        )
        self.hours_per_day_plus_btn.grid(row=0, column=2, padx=5, pady=4)

        # Hours left label
        self.time_left_lbl = ctk.CTkLabel(master=self, text=f"Time left: {self.time_left} hours",
                                          font=("", 15, "normal"))
        self.time_left_lbl.grid(row=1, column=1, padx=10, pady=(2, 0), sticky="E")

        # Hours per day and percentage done label
        self.hours_per_day_percentage_done_lbl = ctk.CTkLabel(
            master=self,
            text=f"Hours per day: {self.selected_course[1]}      -      "
                 f"Course percentage done: {int(self.selected_course[0].percentage)} / 100%",
            font=("", 15, "normal")
        )
        self.hours_per_day_percentage_done_lbl.grid(row=2, column=0, columnspan=2, padx=10, pady=(3, 0), sticky="W")

        # SpinBox for extra time
        self.extra_time_spinbox = SpinBox(master=self, width=120, height=30, step_size=30, extra_time=True)
        self.extra_time_spinbox.grid(row=3, column=0, padx=(10, 0), pady=3, sticky="W")

        # Minus button click bind
        minus_btn = self.extra_time_spinbox.subtract_btn
        # Set the command from the button to None so bind goes first
        minus_btn.configure(command=None)
        minus_btn.bind("<Button-1>",
                       lambda event, s=self.extra_time_spinbox: self.spinbox_dec_percentage(_=event, spinbox=s))

        # Plus button click bind
        plus_btn = self.extra_time_spinbox.add_btn
        # Set the command from the button to None so bind goes first
        plus_btn.configure(command=None)
        plus_btn.bind("<Button-1>",
                      lambda event, s=self.extra_time_spinbox: self.spinbox_inc_percentage(_=event, spinbox=s))

        # Extra time label
        self.extra_time_lbl = ctk.CTkLabel(master=self, text="Extra time", font=("", 15, "normal"))
        self.extra_time_lbl.grid(row=3, column=0, padx=(0, 50), pady=3)

    def spinbox_dec_percentage(self, _, spinbox):
        # Check if the spinbox subtract button is active
        if spinbox.subtract_btn.cget("state") == NORMAL:
            # Decrease course percentage
            self.selected_course[0].decrease_percentage()
            # Call the value_btn method
            spinbox.value_btn(False)
            # Update percentage lbl
            self.hours_per_day_percentage_done_lbl.configure(
                text=f"Hours per day: {self.selected_course[1]}      -      "
                     f"Course percentage done: {int(self.selected_course[0].percentage)} / 100%"
            )
            # Update select courses
            self.master.master.select_courses.show_selected_courses_and_days()

    def spinbox_inc_percentage(self, _, spinbox):
        # Check if the spinbox add button is active
        if spinbox.add_btn.cget("state") == NORMAL:
            # Increase course percentage
            self.selected_course[0].increase_percentage()
            # Call the value_btn method
            spinbox.value_btn(True)
            # Update percentage lbl
            self.hours_per_day_percentage_done_lbl.configure(
                text=f"Hours per day: {self.selected_course[1]}      -      "
                     f"Course percentage done: {int(self.selected_course[0].percentage)} / 100%"
            )
            # Update select courses
            self.master.master.select_courses.show_selected_courses_and_days()
            # Check if we have finished the course
            if self.selected_course[0].percentage == 100.0:
                self.finished_course()

    def inc_percentage(self):
        # Increase course percentage
        self.selected_course[0].increase_percentage()
        # Increase progress bar value
        curr_value = self.hours_per_day_progress_bar.get()
        new_value = curr_value + self.step
        self.hours_per_day_progress_bar.set(new_value)
        # Update time left and current hours
        self.selected_course[3] += 0.5
        self.time_left = self.selected_course[1] - self.selected_course[3]
        # Check if we are done
        self.done = True if self.time_left == 0 else False
        # Update time left lbl
        self.time_left_lbl.configure(text=f"Time left: {self.time_left} hours")
        # Update percentage lbl
        self.hours_per_day_percentage_done_lbl.configure(
            text=f"Hours per day: {self.selected_course[1]}      -      "
                 f"Course percentage done: {int(self.selected_course[0].percentage)} / 100%"
        )
        if self.done:  # Check if we have finished and disable both buttons
            self.hours_per_day_minus_btn.configure(state=DISABLED)
            self.hours_per_day_plus_btn.configure(state=DISABLED)
            # Update select courses
            self.master.master.select_courses.show_selected_courses_and_days()
            # Update show selected courses
            self.master.master.show_selected_courses.enable_extra_time()
            # Update days done
            self.selected_course[2] += 1
        elif self.time_left != self.selected_course[1]:  # Check if we can enable decrease btn
            self.hours_per_day_minus_btn.configure(state=NORMAL)
        # Check if we have finished the course
        if self.selected_course[0].percentage == 100.0:
            self.finished_course()

    def dec_percentage(self):
        # Decrease course percentage
        self.selected_course[0].decrease_percentage()
        # Decrease progress bar value
        curr_value = self.hours_per_day_progress_bar.get()
        new_value = curr_value - self.step
        self.hours_per_day_progress_bar.set(new_value)
        # Update time left and current hours
        self.selected_course[3] -= 0.5
        self.time_left = self.selected_course[1] - self.selected_course[3]
        # Update time left lbl
        self.time_left_lbl.configure(text=f"Time left: {self.time_left} hours")
        # Update percentage lbl
        self.hours_per_day_percentage_done_lbl.configure(
            text=f"Hours per day: {self.selected_course[1]}      -      "
                 f"Course percentage done: {int(self.selected_course[0].percentage)} / 100%"
        )
        # Check if we can disable decrease btn
        if self.time_left == self.selected_course[1]:
            self.hours_per_day_minus_btn.configure(state=DISABLED)

    def finished_course(self):
        self.bell()
        confirm = messagebox.askyesno(
            title="Finished Course",
            message=f"You have successfully finished the course {self.selected_course[0].name}, would you like to delete it? If no,"
                    f" it can no longer be selected.",
            parent=self.master.master
        )
        if confirm:
            # Delete course from courses and selected_courses
            course = self.selected_course[0]
            selected_courses.remove(self.selected_course)
            courses.remove(course)
            # Update select courses frame
            self.master.master.select_courses.show_selected_courses_and_days()
            # Update show selected courses
            self.master.master.show_selected_courses.add_selected_courses()
            # Update nav bar
            self.master.master.nav_bar.update_nav()
        else:
            # Delete course from selected_courses
            selected_courses.remove(self.selected_course)
            # Update select courses frame
            self.master.master.select_courses.show_selected_courses_and_days()
            # Update show selected courses
            self.master.master.show_selected_courses.add_selected_courses()
            # Update nav bar
            self.master.master.nav_bar.update_nav()


# ----------------------- EDIT COURSES CLASS ------------------------ #


class EditSelectCourses(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.attributes("-topmost", True)
        self.lift()
        self.grab_set()
        self.title("")
        self.resizable(width=False, height=False)

        # Select course label
        self.select_course_lbl = ctk.CTkLabel(master=self, text="Select a Course", font=("", 15, "normal"))
        self.select_course_lbl.grid(row=0, column=0, padx=20, pady=5)

        # Get the available courses
        self.available_courses = []
        for course in courses:
            if course.name not in [selected_course[0].name for selected_course in
                                   selected_courses] and course.percentage != 100.0:
                self.available_courses.append(course.name)

        # Available courses option menu
        self.select_option_menu = ctk.CTkOptionMenu(master=self, values=self.available_courses, dynamic_resizing=False)
        self.select_option_menu.grid(row=1, column=0, padx=20, pady=10)

        # SpinBox hours per day
        self.hours_per_day = SpinBox(master=self, width=140, height=28, step_size=0.5, extra_time=False)
        self.hours_per_day.grid(row=2, column=0, padx=20, pady=10)

        # Select course button
        self.select_btn = ctk.CTkButton(master=self, text="Select", command=self.select, state=DISABLED)
        self.select_btn.grid(row=3, column=0, padx=20, pady=(10, 20))

        # Unselect course label
        self.unselect_course_lbl = ctk.CTkLabel(master=self, text="Unselect a Course", font=("", 15, "normal"))
        self.unselect_course_lbl.grid(row=0, column=1, padx=20, pady=5)

        # Unselect option menu
        self.unselect_option_menu = ctk.CTkOptionMenu(
            master=self,
            values=[selected_course[0].name for selected_course in selected_courses],
            dynamic_resizing=False
        )
        self.unselect_option_menu.grid(row=1, column=1, rowspan=2, padx=20, pady=10)

        # Unselect course button
        self.unselect_btn = ctk.CTkButton(master=self, text="Unselect", command=self.unselect)
        self.unselect_btn.grid(row=3, column=1, padx=20, pady=(10, 20))

        # Edit hours per day label
        self.edit_hours_per_day_lbl = ctk.CTkLabel(master=self, text="Edit Hours per Day", font=("", 15, "normal"))
        self.edit_hours_per_day_lbl.grid(row=0, column=2, padx=20, pady=5)

        # Edit courses option menu
        self.edit_hours_per_day_option_menu = ctk.CTkOptionMenu(
            master=self,
            values=[selected_course[0].name for selected_course in selected_courses],
            dynamic_resizing=False
        )
        self.edit_hours_per_day_option_menu.grid(row=1, column=2, padx=20, pady=10)

        # SpinBox edit hours per day
        self.edit_hours_per_day = SpinBox(master=self, width=140, height=28, step_size=0.5, extra_time=False)
        self.edit_hours_per_day.grid(row=2, column=2, padx=20, pady=10)

        # Edit hours per day save
        self.edit_hours_per_day_btn = ctk.CTkButton(
            master=self,
            text="Save hours",
            command=self.edit_selected_course_hours,
            state=DISABLED
        )
        self.edit_hours_per_day_btn.grid(row=3, column=2, padx=10, pady=(10, 20))

        # Bind window
        self.bind("<Button-1>", self.check_bind)
        self.bind("<Key>", self.check_bind)

        self.check_availability()

    def check_bind(self, event):
        if event.keysym == "Escape":
            self.close_window()
        else:
            # Check if select course hours per day value is not 0
            if self.hours_per_day.get_value() == 0.0:
                self.select_btn.configure(state=DISABLED)
            else:
                self.select_btn.configure(state=NORMAL)
            # Check if edit hours per day value is not 0
            if self.edit_hours_per_day.get_value() == 0.0:
                self.edit_hours_per_day_btn.configure(state=DISABLED)
            else:
                self.edit_hours_per_day_btn.configure(state=NORMAL)

    def close_window(self):
        self.destroy()
        self.update()
        self.master.lift()

    def select(self):
        # Validate num of courses
        if len(selected_courses) >= max_courses:
            # Already more than max_courses
            if max_courses == 1:
                self.del_values(f"Cannot take more than {max_courses} course at the same time")
            else:
                self.del_values(f"Cannot take more than {max_courses} courses at the same time")
        else:
            hours = self.hours_per_day.get_value()
            # Course and hours are accepted
            selected_course = self.get_course(self.select_option_menu.get(), "course")
            # First check that the hours per day are not bigger than the total hours of a course
            if hours > selected_course.hours_left:
                self.del_values("Hours per day cannot be bigger than the total amount of hours left in this course")
            else:
                # Append selected course to Selected Courses List
                selected_courses.append([selected_course, hours, 0, 0.0])
                self.bell()
                self.close_window()
                messagebox.showinfo(title="SUCCESS", message="Successfully selected course", parent=self.master)

    def unselect(self):
        # Get the course name
        course_name = self.unselect_option_menu.get()
        # Confirm if you want to unselect course
        self.bell()
        self.master.lift()
        self.attributes("-topmost", False)
        confirm = messagebox.askyesno(
            title="Confirm",
            message=f"You are about to unselect course: {course_name}, all progress and data will be lost except its current percentage,"
                    f" are you sure?",
            parent=self.master
        )
        if confirm:
            # Remove the course based on its name
            for selected_course in selected_courses:
                if course_name == selected_course[0].name:
                    selected_courses.remove(selected_course)
                    break
            # Message box success
            self.bell()
            self.close_window()
            messagebox.showinfo(title="SUCCESS", message="Successfully unselected course", parent=self.master)
        else:
            self.attributes("-topmost", True)
            self.lift()

    def edit_selected_course_hours(self):
        # Get the course name and new hours per day
        course_name = self.edit_hours_per_day_option_menu.get()
        hours = self.edit_hours_per_day.get_value()
        selected_course = self.get_course(course_name, "selected_course")
        if selected_course[1] == hours:
            # New hours cannot be the same as before
            self.del_values("The new hours per day cannot be the same as before")
        elif hours > selected_course[0].hours_left:
            # New hours cannot be more than the hours left in the course
            self.del_values("New hours per day cannot be bigger than the total amount of hours left in this course")
        else:
            # Change to the new hours per day
            selected_course[1] = hours
            # Check if our current hours are more than the new hours per day
            if hours < selected_course[3]:
                # The current hours is now equal to new hours
                selected_course[3] = hours
            # Update select courses frame
            self.master.select_courses.show_selected_courses_and_days()
            # Update show selected courses
            self.master.show_selected_courses.add_selected_courses()
            # Update nav bar
            self.master.nav_bar.update_nav()
            # Message box success
            self.bell()
            self.close_window()
            messagebox.showinfo(
                title="SUCCESS",
                message="Successfully edited the course hours",
                parent=self.master
            )

    def check_availability(self):
        # Check if there are available courses to select
        if len(self.available_courses) == 0:
            self.select_option_menu.set("None")
            self.select_option_menu.configure(state=DISABLED)
            for child in self.hours_per_day.winfo_children():
                child.configure(state=DISABLED)
            self.select_btn.configure(state=DISABLED)
        # Check if there are available courses to unselect
        if len(selected_courses) == 0:
            # Disable unselect section
            self.unselect_option_menu.set("None")
            self.unselect_option_menu.configure(state=DISABLED)
            self.unselect_btn.configure(state=DISABLED)
            # Disable edit hours
            self.edit_hours_per_day_option_menu.set("None")
            self.edit_hours_per_day_option_menu.configure(state=DISABLED)
            for child in self.edit_hours_per_day.winfo_children():
                child.configure(state=DISABLED)
            self.edit_hours_per_day_btn.configure(state=DISABLED)
        self.update()

    def del_values(self, message):
        # Error messagebox
        self.bell()
        self.master.lift()
        self.attributes("-topmost", False)
        messagebox.showerror(
            title="ERROR",
            message=message,
            parent=self.master
        )
        self.hours_per_day.reset()
        self.edit_hours_per_day.reset()
        self.attributes("-topmost", True)
        self.lift()

    @staticmethod
    def get_course(name, type_lst):
        if type_lst == "course":
            # Get the course object based on the name given
            for course in courses:
                if course.name == name:
                    return course
        elif type_lst == "selected_course":
            for selected_course in selected_courses:
                if selected_course[0].name == name:
                    return selected_course


# -------------------------- NAV BAR CLASS -------------------------- #


class NavBar(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_propagate(False)

        # Add course button
        self.add_course_btn = ctk.CTkButton(master=self, text="+", width=50, command=self.add_course)
        self.add_course_btn.place(x=15, y=6)

        # Delete course button
        self.del_course_btn = ctk.CTkButton(
            master=self,
            text="-",
            width=50,
            state=NORMAL if len(courses) != 0 else DISABLED,
            command=self.delete_course
        )
        self.del_course_btn.place(x=85, y=6)

        # Streaks label
        self.streaks_lbl = ctk.CTkLabel(master=self, text=f"Streaks: {streaks}")
        self.streaks_lbl.place(x=155, y=6)

        # Date label
        self.date_lbl = ctk.CTkLabel(master=self, text=date)
        self.date_lbl.place(x=425, y=20, anchor=CENTER)

        # Weekly progress button
        self.weekly_progress_btn = ctk.CTkButton(master=self, text="Progress", width=50, command=self.weekly_progress)
        self.weekly_progress_btn.place(x=680, y=6)
        self.weekly_progress_btn.configure(state=DISABLED)  # AÚN NO ESTÁ ESCRITO

        # Settings button
        self.settings_btn = ctk.CTkButton(master=self, text="Settings", width=50, command=self.settings)
        self.settings_btn.place(x=770, y=6)

    def add_course(self):
        # Open Add Course Window
        global top_level_open
        top_level_open = True
        window = AddCourseWindow()
        window.wait_window()

        self.update_nav()
        top_level_open = False
        # Update selected courses frame
        self.master.select_courses.show_selected_courses_and_days()
        self.update()

    def delete_course(self):
        # Open Delete Course Window
        global top_level_open
        top_level_open = True
        window = DelCourseWindow()
        window.wait_window()

        self.update_nav()
        top_level_open = False
        # Update selected courses frame
        self.master.select_courses.show_selected_courses_and_days()
        # Update show selected courses
        self.master.show_selected_courses.add_selected_courses()
        self.update()

    def weekly_progress(self):
        pass

    def settings(self):
        # Open Settings Window
        global top_level_open
        top_level_open = True
        window = Settings()
        window.wait_window()

        # Update nav bar
        self.update_nav()
        top_level_open = False
        # Update selected courses frame
        self.master.select_courses.show_selected_courses_and_days()
        # Update show selected courses
        self.master.show_selected_courses.add_selected_courses()
        # Update timer
        self.master.timer.reset_timer(True)
        self.update()

    def update_nav(self):
        self.del_course_btn.configure(state=NORMAL if len(courses) != 0 else DISABLED)
        self.streaks_lbl.configure(text=f"Streaks: {streaks}")
        self.date_lbl.configure(text=date)
        self.settings_btn.configure(state=NORMAL)
        self.update()


# ---------------------- SELECT COURSES CLASS ----------------------- #


class SelectCourses(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_propagate(False)

        # Title frame for edit button and label
        self.title_frame = ctk.CTkFrame(master=self)
        self.title_frame.grid(row=0, column=0, columnspan=2, padx=20, pady=6)

        # Frame edit button
        self.edit_btn = ctk.CTkButton(master=self.title_frame, text="Edit", width=50, command=self.edit_courses)
        self.edit_btn.grid(row=0, column=0, padx=(7, 6), pady=6)

        # Frame title label
        self.title_lbl = ctk.CTkLabel(master=self.title_frame, text="Select Courses", font=("", 15, "normal"))
        self.title_lbl.grid(row=0, column=1, padx=(6, 7), pady=6)

        # Info label
        self.info_lbl = ctk.CTkLabel(master=self)
        self.info_lbl.grid(row=1, column=0, columnspan=2, padx=5)

        self.selected_courses_names_list = []
        self.selected_courses_days_left_list = []

        # Check for courses chosen
        self.show_selected_courses_and_days()

    def edit_courses(self):
        global top_level_open
        top_level_open = True
        window = EditSelectCourses()
        window.wait_window()

        top_level_open = False
        # Update selected courses frame
        self.show_selected_courses_and_days()
        # Update show selected course frame
        self.master.show_selected_courses.add_selected_courses()
        self.update()

    def show_selected_courses_and_days(self):
        # Clear selected courses to get again
        if len(self.selected_courses_names_list) != 0:
            for i in range(len(self.selected_courses_names_list)):
                self.selected_courses_names_list[i].destroy()
                self.selected_courses_days_left_list[i].destroy()
            self.selected_courses_names_list.clear()
            self.selected_courses_days_left_list.clear()
        self.info_lbl.configure(text="")

        if len(selected_courses) != 0:
            # If there are selected courses
            self.edit_btn.configure(state=NORMAL)
            # Show all selected courses and days left
            for i in range(len(selected_courses)):
                self.selected_courses_names_list.append(ctk.CTkLabel(
                    master=self,
                    text=selected_courses[i][0].name,
                    wraplength=79,
                    justify=LEFT
                ))
                self.selected_courses_days_left_list.append(ctk.CTkLabel(
                    master=self,
                    text=f"~ {round(selected_courses[i][0].days_left_to_complete(selected_courses[i][1]))} days"
                ))
                self.selected_courses_names_list[i].grid(row=i + 1, column=0, sticky="W", padx=20, pady=5)
                self.selected_courses_days_left_list[i].grid(row=i + 1, column=1, sticky="E", padx=20, pady=5)
        else:
            if len(courses) == 0:
                # There are no courses
                self.info_lbl.configure(text="There are no courses")
                self.edit_btn.configure(state=DISABLED)
            else:
                # No courses have been selected
                self.info_lbl.configure(text="No courses have been selected")
                self.edit_btn.configure(state=NORMAL)
        self.update()


# --------------------------- TIMER CLASS --------------------------- #


class Timer(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.running = False
        self.grid_propagate(False)

        # Title frame
        self.title_frame = ctk.CTkFrame(master=self, width=174, height=40)
        self.title_frame.grid(row=0, column=0, columnspan=2, padx=20, pady=6)

        # Frame title label
        self.title_lbl = ctk.CTkLabel(master=self.title_frame, text="Timer", font=("", 15, "normal"))
        self.title_lbl.grid(row=0, column=0, padx=70, pady=6)

        # Timer label
        self.timer = ctk.CTkLabel(master=self, text=f"{timer_length}:00", font=("Courier", 30, "bold"))
        self.timer.grid(row=1, column=0, columnspan=2, pady=20)

        # Start button
        self.start_btn = ctk.CTkButton(master=self, text="Start", width=50, command=self.start_timer)
        self.start_btn.grid(row=2, column=0, pady=10)

        # Reset button
        self.reset_btn = ctk.CTkButton(master=self, text="Reset", width=50, state=DISABLED,
                                       command=lambda: self.reset_timer(False))
        self.reset_btn.grid(row=2, column=1, pady=10)

        self.time = None

    def start_timer(self):
        self.running = True
        self.bell()
        self.start_btn.configure(state=DISABLED)
        self.reset_btn.configure(state=NORMAL)
        count = timer_length * 60
        self.count_down(count)

    def reset_timer(self, settings):
        self.start_btn.configure(state=NORMAL)
        self.reset_btn.configure(state=DISABLED)
        if not settings or self.running:
            self.after_cancel(self.time)
        self.timer.configure(text=f"{timer_length}:00")
        self.running = False

    def times_up(self):
        self.start_btn.configure(state=DISABLED)
        self.reset_btn.configure(state=DISABLED)
        self.timer.configure(text="TIME'S UP")
        self.master.lift()
        self.after(2000, lambda: self.reset_timer(False))

    def count_down(self, count):
        count_min = floor(count / 60)
        count_sec = count % 60
        if count_min < 10:
            count_min = f"0{count_min}"
        if count_sec < 10:
            count_sec = f"0{count_sec}"
        self.timer.configure(text=f"{count_min}:{count_sec}")
        if count > 0:
            self.time = self.after(1000, self.count_down, count - 1)
        else:
            # DONE
            self.bell()
            self.times_up()


# ------------------- SHOW SELECTED COURSES CLASS ------------------- #


class ShowSelectedCourses(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_propagate(False)
        self.selected_courses_list = []

        # Add all selected courses
        self.add_selected_courses()

    def add_selected_courses(self):
        # Delete selected course list for redraw
        for selected_course in self.selected_courses_list:
            selected_course.destroy()
        self.selected_courses_list.clear()

        # Add a CourseFrame per selected course
        for i in range(len(selected_courses)):
            self.selected_courses_list.append(CourseFrame(
                master=self,
                selected_course_num=i,
                selected_course=selected_courses[i],
                width=600,
                height=126
            ))
            self.selected_courses_list[i].grid(row=i, column=0, columnspan=2, pady=(8, 0), padx=15)

        self.enable_extra_time()
        self.update()

    def enable_extra_time(self):
        can_use_extra_time = True
        # Check if all courses for today are finished
        for selected_course in self.selected_courses_list:
            if not selected_course.done:
                can_use_extra_time = False
                break

        # Check if we can enable extra time spinboxes
        if can_use_extra_time:
            for selected_course in self.selected_courses_list:
                selected_course.extra_time_spinbox.add_btn.configure(state=NORMAL)
        else:
            for selected_course in self.selected_courses_list:
                selected_course.extra_time_spinbox.add_btn.configure(state=DISABLED)
        self.update()


# ---------------------------- MAIN CLASS --------------------------- #


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # WINDOW
        self.title('Courses Tracker')
        self.geometry('850x450')
        self.resizable(width=False, height=False)

        # LOAD DATA
        self.load_data()

        # NAVBAR
        self.nav_bar = NavBar(
            master=self,
            corner_radius=0,
            border_width=1,
            width=850,
            height=40,
            fg_color='transparent'
        )
        self.nav_bar.grid(row=0, column=0, columnspan=2, sticky='EW')

        # SHOW SELECTED COURSES
        self.show_selected_courses = ShowSelectedCourses(
            master=self,
            corner_radius=0,
            width=630,
            height=410
        )
        self.show_selected_courses.grid(row=1, column=0, rowspan=2, sticky='NSEW')

        # SIDEBAR SELECT COURSES
        self.select_courses = SelectCourses(
            master=self,
            corner_radius=0,
            border_width=1,
            width=220,
            height=205,
            fg_color='transparent'
        )
        self.select_courses.grid(row=1, column=1, sticky='NSEW')

        # SIDEBAR TIMER
        self.timer = Timer(
            master=self,
            corner_radius=0,
            border_width=1,
            width=220,
            height=205,
            fg_color='transparent'
        )
        self.timer.grid(row=2, column=1, sticky='NSEW')

        # SAVE DATA
        self.protocol('WM_DELETE_WINDOW', self.on_closing)

        # QUITING APP
        # if system == 'WINDOWS':
        #     # Running on windows
        #     self.bind_all('Command-q', lambda event: print(event))
        # elif system == 'DARWIN':
        #     # Running on macOS
        #     self.bind_all('Command-q', lambda event: print(event))

        # CHECK DATE
        self.update_data()

    @staticmethod
    def set_appearance_color_scheme():
        ctk.set_appearance_mode(appearance)
        ctk.set_default_color_theme(color_scheme)

    def update_data(self):
        global date, streaks, last_day_saved
        # Check the current date
        current_date = str(datetime.now().date())
        if current_date != date or last_day_saved != date:
            last_day_saved = date
            # The day has changed
            date = current_date
            # Check if we have finished all courses for today
            add_to_streaks = True
            for selected_course in selected_courses:
                # Check if hours per day are equal to the current hours
                if selected_course[1] != selected_course[3]:
                    # One or more courses are not finished
                    add_to_streaks = False
                # Make current hours 0
                selected_course[3] = 0.0
            if add_to_streaks:
                # We have completed all the hours
                streaks += 1
            else:
                streaks = 0
            # Update selected courses frame
            self.select_courses.show_selected_courses_and_days()
            # Update show selected courses
            self.show_selected_courses.add_selected_courses()
            # Update Nav bar
            self.nav_bar.update_nav()

        # Run the function again after 1 second
        self.after(1000, self.update_data)

    def on_closing(self):
        if not top_level_open:
            self.save_data()
            self.destroy()

    def load_data(self):
        global streaks, appearance, color_scheme, timer_length, max_courses, last_day_saved
        file_worked = True
        self.update()
        if os.path.exists('data.json'):
            if os.stat('data.json').st_size != 0:
                with open('data.json', 'r') as file:
                    data = json.load(file)

                # Load all courses
                for course in data['courses']:
                    courses.append(Course(course['name'], course['hours'], course['percentage']))

                # Load all chosen courses
                for selected_course in data['selected_courses']:
                    for course in courses:
                        if selected_course['name'] == course.name:
                            selected_courses.append(
                                [course,
                                 selected_course['hours_per_day'],
                                 selected_course['days_done'],
                                 selected_course['current_hours']]
                            )

                # Load streaks data
                streaks = data['streaks']

                # Load window appearance, color scheme and timer length
                appearance = data['appearance']
                color_scheme = data['color_scheme']
                timer_length = data['timer_length']
                max_courses = data['max_courses']

                # Load last day saved
                last_day_saved = data['last_day_saved']

                # Set appearance and color scheme
                self.set_appearance_color_scheme()

            else:
                self.bell()
                messagebox.showinfo(title="ERROR", message="Data File is empty, no values will be added.", parent=self)
                file_worked = False
        else:
            self.bell()
            messagebox.showinfo(
                title="ERROR",
                message="No Data File found, will be created after program ends.",
                parent=self
            )
            file_worked = False

        if not file_worked:
            appearance = "system"
            color_scheme = "blue"
            timer_length = 30
            max_courses = 3
            # Set appearance and color scheme
            self.set_appearance_color_scheme()

    @staticmethod
    def save_data():
        json_dict = {
            'courses': [],
            'selected_courses': [],
            'streaks': 0,
            "appearance": "",
            "color_scheme": "",
            "timer_length": 0,
            "max_courses": 0,
            'last_day_saved': ''
        }

        # Add all courses
        for course in courses:
            c = {
                'name': course.name,
                'hours': course.hours,
                'percentage': course.percentage
            }
            json_dict['courses'].append(c)

        # Add chosen courses
        for selected_course in selected_courses:
            cc = {
                'name': selected_course[0].name,
                'hours_per_day': selected_course[1],
                'days_done': selected_course[2],
                'current_hours': selected_course[3]
            }
            json_dict['selected_courses'].append(cc)

        # Add streaks
        json_dict['streaks'] = streaks

        # Add appearance, color scheme, timer length and max courses
        json_dict['appearance'] = appearance
        json_dict['color_scheme'] = color_scheme
        json_dict['timer_length'] = timer_length
        json_dict['max_courses'] = max_courses

        # Add last day saved
        json_dict['last_day_saved'] = date

        with open('data.json', 'w') as file:
            json.dump(json_dict, file, indent=2)


# ------------------------------- RUN ------------------------------- #

if __name__ == '__main__':
    # RUN
    app = App()
    app.mainloop()
