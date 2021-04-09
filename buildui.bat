@echo off

IF "%1" == "clean" (
    del videotrackr\main_ui.py
    del videotrackr\about_ui.py
) ELSE (
    pyside6-uic videotrackr\main.ui -o videotrackr\main_ui.py
    pyside6-uic videotrackr\about.ui -o videotrackr\about_ui.py
)