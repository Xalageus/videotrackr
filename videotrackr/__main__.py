import sys
import argparse
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel
from videotrackr.main_controller import main_controller
from videotrackr.__init__ import __name__ as videotrackr_name

def main():
    parser = argparse.ArgumentParser(prog=videotrackr_name)
    parser.add_argument('video_file', metavar='video_file', type=str, nargs='?', help='Video file to use')
    parser.add_argument('--debug', help='Enable debug mode', action='store_true')
    args = parser.parse_args()

    app = QApplication([])
    form = main_controller(args.debug)
    form.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()