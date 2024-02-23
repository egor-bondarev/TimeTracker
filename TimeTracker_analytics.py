import flet as ft
import datetime
import asyncio
import glob
import os
import re

class ParsedDate():
    def __init__(self, source): 
         self._source = source.split('-')      
         self._year = int(self._source[0])
         self._month = int(self._source[1])
         self._day = int(re.match(r'\d\d', self._source[2]).group())

    def get_year(self):
        return self._year
    
    def get_month(self):
        pass


def main(page: ft.Page):
    #t = ft.Text(value="Hello, world!", color="green")
    #page.controls.append(t)
    #page.update()

    def change_date(e):
        print(f"Date picker changed, value is {date_picker.value}")

    def date_picker_dismissed(e):
        print(f"Date picker dismissed, value is {date_picker.value}")

    files_dates = get_dates()
    first_file_date = ParsedDate(files_dates[0])
    last_file_date = ParsedDate(files_dates[-1])

    date_picker = ft.DatePicker(
        on_change=change_date,
        on_dismiss=date_picker_dismissed,
        first_date=datetime.datetime(year = first_file_date._year, month = first_file_date._month, day = first_file_date._day),
        last_date=datetime.datetime(year = last_file_date._year, month = last_file_date._month, day = last_file_date._day),
    )

    page.overlay.append(date_picker)

    date_button = ft.ElevatedButton(
        "Pick date",
        icon=ft.icons.CALENDAR_MONTH,
        on_click=lambda _: date_picker.pick_date()
    )

    page.add(date_button)

def start():
    ft.app(main, view = ft.AppView.WEB_BROWSER)

def get_dates():
    dates = [files for files in os.listdir('./') if re.search(r'\d{4}-\d\d-\d\d.json$', files)]
    dates.sort()

    return dates

#get_dates()