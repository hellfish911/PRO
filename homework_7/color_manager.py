"""Module contains context manager which changes color of the printed text."""


class colorizer:
    color_codes = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'default': '\033[0m',
    }

    def __init__(self, color):
        self.color = color.lower()
        self.color_code = self.color_codes.get(self.color,
                                               self.color_codes['default'])

    def __enter__(self):
        print(self.color_code, end='')

    def __exit__(self, exc_type, exc_value, traceback):
        print(self.color_codes['default'], end='')


if __name__ == '__main__':
    print('aaa')
    print('bbb')

    with colorizer('red'):
        print('printed in red')

    print('printed in default color')
