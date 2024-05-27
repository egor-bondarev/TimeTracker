# !/bin/bash

run_tests(){
    pytest --alluredir allure-results ./TaskTracker/tests/local_tests
}

show_allure_results(){
    allure serve allure-results
}

help(){
    echo "Script for running tests."
    echo
    echo "Syntax: scriptTemplate [-h|c]"
    echo
    echo "options:"
    echo "h         print this help information"
    echo "c         clean previous allure results"
    echo
}

clean_allure_results(){
    echo "Removing allure results \n"
    rm -rf ./allure-results/*
}

OPEN_RESULTS=true

while getopts :coh flag; do
    case $flag in
        h) # Print help information
            help
            exit;;
        c) # Clean previous allure results
            clean_allure_results;;
        \?) # Invalid option
            echo "Error: Invalid option"
            exit;;
    esac
done

run_tests
if [[ $OPEN_RESULTS == true ]]; then
    show_allure_results
fi