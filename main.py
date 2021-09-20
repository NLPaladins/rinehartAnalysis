import traceback
import argparse
from pprint import pprint

# Custom libs
from nlp_libs import Configuration, ColorizedLogger, ProcessedBook

logger = ColorizedLogger(logger_name='Main', color='yellow')


def get_args() -> argparse.Namespace:
    """Setup the argument parser

    Returns:
        argparse.Namespace:
    """
    parser = argparse.ArgumentParser(
        description='Rinehart Analysis for the NLP (ECE-617) Project 1',
        add_help=False)
    # Required Args
    required_args = parser.add_argument_group('Required Arguments')
    config_file_params = {
        'type': argparse.FileType('r'),
        'required': True,
        'help': "The configuration yml file"
    }
    required_args.add_argument('-c', '--config-file', **config_file_params)
    required_args.add_argument('-l', '--log', required=True, help="Name of the output log file")
    # Optional args
    optional_args = parser.add_argument_group('Optional Arguments')
    optional_args.add_argument('-d', '--debug', action='store_true',
                               help='Enables the debug log messages')
    optional_args.add_argument("-h", "--help", action="help", help="Show this help message and exit")

    return parser.parse_args()


def main():
    """ This is the main function of main.py

    Example:
        python starter/main.py -c confs/proj_1.yml -l logs/proj_1.log
    """

    # Initializing
    args = get_args()
    ColorizedLogger.setup_logger(log_path=args.log, debug=args.debug, clear_log=True)
    # Load the configuration
    conf = Configuration(config_src=args.config_file)
    # Get the books dict
    books = conf.get_config('data_loader')[0]['config']['urls']
    # pprint(books)  # Pretty print the books dict
    # Create ProcessedBook Object
    circular_staircase_processed = ProcessedBook(title=books['The_Circular_Staircase'])
    chapt_2 = '\n'.join(circular_staircase_processed.get_chapter(chapter=2))
    logger.info(f"Chapter 2:\n{chapt_2[:45]} (..)")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.error(str(e) + '\n' + str(traceback.format_exc()))
        raise e
