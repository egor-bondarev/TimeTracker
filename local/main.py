"""Start file."""
import logging
from controllers.main_controller import MainController

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logging.basicConfig(filename='myapp.log', level=logging.INFO)
    logger.info('Application started')
    controller = MainController()
