# TODO: Create a ConsolePrinter class maybe (?)
def print_error(message: str = ''):
    print('>>>> [ERROR] <<<< ' + message)

def print_in_progress(message: str = ''):
    print('.... ' + message)

def print_completed(message: str = ''):
    print('[OK] ' + message)