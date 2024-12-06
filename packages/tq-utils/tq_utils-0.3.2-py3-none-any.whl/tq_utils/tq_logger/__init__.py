"""
Usage of TQRunLogger

def case(logger):
    logger.info('asd')
    logger.warning('123')
    logger.error('456')

    def save_function(file_path, file_data):
        with FileManager(file_path, 'w') as f:
            f.write(file_data)

    logger.logging_output_file('asd-{}.txt'.format(hash(random.random())), '123123', save_function)


def test_logger_instance():  # instance usage
    logger = TQRunLogger(LOGGER_TEST_DATA_DIR)
    case(logger)


def test_logger_decorator():  # decorator usage
    @TQRunLogger(LOGGER_TEST_DATA_DIR)
    def decorator_method(logger):
        case(logger)

    decorator_method()

def test_logger_context_manager():  # context manager usage
    with TQRunLogger(LOGGER_TEST_DATA_DIR) as logger:
        case(logger)
"""
from .logger import TQRunLogger, LoggingLevel

__all__ = ['TQRunLogger', 'LoggingLevel']
