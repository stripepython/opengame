import sys

from .version import get_string


def main():
    if len(sys.argv) > 1:
        option = sys.argv[1]
        if option in {'-v', '--version', 'version'}:
            print(get_string())
        if option in {'/?', '-h', '--help', 'help'}:
            print('Use "-v", "--version" or "version" to show the version.')
            print('Use "/?", "-h", "--help", "help" to show help.')
            

if __name__ == '__main__':
    main()
