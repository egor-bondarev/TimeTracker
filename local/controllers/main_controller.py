"""main_controller.py"""

from views.main_view import MainView
from models.main_model import MainModel

class MainController():
    """Main controller."""
    def __init__(self):
        self.view = MainView()
        self.model = MainModel()
