from datetime import datetime


class bcolors:
    NONE = ''
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


level_colour = {
    0: bcolors.OKBLUE,
    1: bcolors.WARNING,
    2: bcolors.FAIL
}

level_text = {
    0: "INFO",
    1: "WARN",
    2: "ERROR"
}


def DatabaseLog(content, level=0):
    Log("DATABASE", content, level)


def SynManagerLog(content, level=0):
    Log("Synonym Manager", content, level)


def Log(category, content, level=0):
    timestamp = datetime.now().strftime("%H:%M:%S")

    output = f"{level_colour[level]}[{timestamp}] [{category} - {level_text[level]}]: {content}{bcolors.ENDC}"
    print(output)
