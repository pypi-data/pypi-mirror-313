import sys


def stop_app():
    print("Stopping the application...")
    sys.exit(1)


def log(message: str, is_error: bool = False):
    sign = '[!]' if is_error else '[+]'
    print(f'{sign} {message}')
    if is_error:
        stop_app()
