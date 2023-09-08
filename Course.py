from math import ceil


class Course:
    def __init__(self, name, hours, percentage=0):
        self.name = name
        self.hours = hours
        self.percentage = percentage
        self.hours_completed = round(self.hours * (self.percentage/100), 2)
        # print(self.hours_completed)
        self.hours_left = self.hours - self.hours_completed

    def days_left_to_complete(self, hours_per_day):
        return ceil(self.hours_left / hours_per_day)

    def increase_percentage(self):
        self.hours_left -= 0.5
        self.hours_completed += 0.5
        self.percentage = (self.hours_completed / self.hours) * 100
        # print(self.percentage)
        # print(self.hours_left)

    def decrease_percentage(self):
        self.hours_completed -= 0.5
        self.hours_left += 0.5
        self.percentage = (self.hours_completed / self.hours) * 100
        # print(self.percentage)
        # print(self.hours_left)
