Time tracker application for logging your time.

Functionality
TimeTracker is desktop application with logging time to .json files. New file for each new day.
On input frame you can add your task description and category of the task (optional).
For start you need to push button start and button finish for finishing it. You can push button finish without starting, in this case start time would be get from finish time of previous task.

On the analytic frame you can create result table with task in choosen time period. Also you can choose visible parameters in report like: date, description, category, start time, finish time and duration.
For merge tasks on categories you need to choose special checkbox.

If you want to change report, you need to push clean and then push report button for update.

Run tests:
from project folder with run_tests.sh you need to run this script
sh ./run_tests.sh -c
with options:
h         print this help information
c         clean previous allure results