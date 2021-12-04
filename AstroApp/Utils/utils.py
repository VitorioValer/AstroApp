def cprint(str_to_print, color, bold=False, underline=False):
    color_set = {
        'HEADER': '\033[95m',
        'BLUE': '\033[94m',
        'CYAN': '\033[96m',
        'GREEN': '\033[92m',
        'WARNING': '\033[93m',
        'FAIL': '\033[91m',
    }

    color = color_set[color]
    bold = '\033[1m' if bold else ''
    underline = '\033[4m' if underline else ''

    print(f'{color}{bold}{underline}{str_to_print}\033[0m')


if __name__ == '__main__':
    cprint(
        str_to_print='This is just a test',
        color='HEADER',
        bold=True,
        underline=True
    )

