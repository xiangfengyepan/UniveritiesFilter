class CliOutput:
    COLORS = {
        "default": "\033[0m",
        "green": "\033[92m",
        "red": "\033[91m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "bold": "\033[1m",
    }

    @staticmethod
    def print(message, color="default"):
        print(f"{CliOutput.COLORS.get(color, CliOutput.COLORS['default'])}{message}{CliOutput.COLORS['default']}")

    @staticmethod
    def success(message):
        CliOutput.print(message, "green")

    @staticmethod
    def error(message):
        CliOutput.print(message, "red")

    @staticmethod
    def warning(message):
        CliOutput.print(message, "yellow")

    @staticmethod
    def info(message):
        CliOutput.print(message, "blue")


class CliInput:
    @staticmethod
    def prompt(message, default=None):
        if default is not None:
            full_message = f"{message} [default: {default}]: "
        else:
            full_message = f"{message}: "
        value = input(full_message).strip()
        return value if value else default

    @staticmethod
    def confirm(message):
        while True:
            value = input(f"{message} (yes/no): ").strip().lower()
            if value in {"yes", "y"}:
                return True
            elif value in {"no", "n"}:
                return False
            CliOutput.warning("Invalid input, please type 'yes' or 'no'.")
