TimeTracker application for logging your time.

# Functionality
TimeTracker is desktop application with logging time to .json files. New file is created each new day.

## Track you time
On input frame you can add your task description (is required) and category of the task (is optional). 
For starting your task push button **Start** and button **Finish** for finishing it. If you forgot to start task, you may push button **Finish**, and start timestamp of the surrent task will be finish timestamp of the previous task.

## Get report
On the analytic frame you can create result table with task in choosen time period. Also you can choose visible parameters in report like: * *date* *, * *description* *, * *category* *, * *start timestamp* *, * *finish timestamp* * and * *duration* *.
For merge tasks on categories you need to choose special checkbox. In this case tasks without category will not be shown.

If you want to change report, you need to push **Clean** and then again push **Report** button for update.

# Run tests
From project folder with run_tests.sh you need to run this script
> sh ./run_tests.sh -c \n
> with options: \n 
> h         print this help information \n
> c         clean previous allure results

# Run app
> python3 ./main.py