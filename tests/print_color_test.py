def print_colored_text(text, color):
    colors = {
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'reset': '\033[0m'
    }

    if color in colors:
        colored_text = f"{colors[color]}{text}{colors['reset']}"
        print(colored_text)
    else:
        print(text)


# Example usage
print_colored_text("This is a red text", "red")
print_colored_text("This is a blue text", "blue")
print_colored_text("This is a yellow text", "yellow")
