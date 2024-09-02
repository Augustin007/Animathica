import logging
import sys

def main():
    args = sys.argv[1:]

    level = 30
    settings = 0
    if len(args) > 0:
        try:
            level = int(args[0])
        except ValueError:
            pass
    
    if len(args) > 1:
        try:
            settings = int(args[1])
        except ValueError:
            pass
    if len(args) > 2:
        print('only two arguments mean anything. The rest of the arguments have been lost.')
    logging.basicConfig(level=level)
    logger = logging.getLogger(__name__)

    logger.info(f'Settings: {settings}')
    
if __name__ == '__main__':
    main()
    import Animathica
    Animathica.main()
