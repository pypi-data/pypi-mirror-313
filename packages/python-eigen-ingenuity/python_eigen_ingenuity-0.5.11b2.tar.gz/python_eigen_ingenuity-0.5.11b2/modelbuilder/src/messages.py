none = '\033[0m'
bold = '\033[1m'
pale = '\033[2m'
italic = '\033[3m'
underline = '\033[4m'
grey = '\033[90m'
red = '\033[91m'
green = '\033[92m'
yellow = '\033[93m'
blue = '\033[94m'
purple = '\033[95m'
cyan = '\033[96m'

info = green
warning = yellow
error = red
status = blue
report = cyan
details = cyan

print_cr = False

def set_cr_needed(needed):
    global print_cr
    print_cr = needed

def check_cr_needed():
    global print_cr
    if print_cr:
        print()
        print_cr = False

def message(message1, check_cr=True):
    if check_cr:
        check_cr_needed()
    print(f'{message1}')
    set_cr_needed(False)

def message_no_cr(message1):
    print(f'{message1}', end='')
    set_cr_needed(True)

def report_message(message1, message2 = ''):
    check_cr_needed()
    print(f'{report}{message1}{none}{message2}')
    set_cr_needed(False)

def info_message(message1, message2 = ''):
    check_cr_needed()
    print(f'{info}{message1}{none}{message2}')
    set_cr_needed(False)

def warning_message(message1, message2 = ''):
    check_cr_needed()
    print(f'{yellow}Warning! {none}{message1}{details}{message2}{none}')
    set_cr_needed(False)

def error_message(message1, message2 = ''):
    check_cr_needed()
    print(f'{error}Error! {none}{message1}{status}{message2}{none}')
    set_cr_needed(False)
