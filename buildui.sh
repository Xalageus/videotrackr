if [ "$1" = "clean" ]; then
    rm videotrackr/main_ui.py
    rm videotrackr/about_ui.py
    rm videotrackr/select_region_ui.py
else
    pyside6-uic videotrackr/main.ui -o videotrackr/main_ui.py
    pyside6-uic videotrackr/about.ui -o videotrackr/about_ui.py
    pyside6-uic videotrackr/select_region.ui -o videotrackr/select_region_ui.py
fi