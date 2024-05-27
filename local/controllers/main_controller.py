"""main_controller.py"""

from TaskTracker.local.views.main_view import MainView

class MainController():
    """Main controller."""
    def __init__(self):
        self.view = MainView()
