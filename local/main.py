"""Start file."""
import logging
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from local.controllers.main_controller import MainController

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logging.basicConfig(filename='myapp.log', level=logging.INFO)
    logger.info('Application started')
    controller = MainController()
