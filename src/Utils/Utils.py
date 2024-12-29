import sys



Red: str = "\033[31m"
Green: str = "\033[32m"
Yellow: str = "\033[33m"
Blue: str = "\033[34m"
Magenta: str = "\033[35m"
Cyan: str = "\033[36m"
White: str = "\033[37m"


BrightRed: str = "\033[91m"
BrightGreen: str = "\033[92m"
BrightYellow: str = "\033[93m"
BrightBlue: str = "\033[94m"
BrightMagenta: str = "\033[95m"
BrightCyan: str = "\033[96m"
BrightWhite: str = "\033[97m"

Reset: str = "\033[0m"



def rprint(args, end_="\n"):
    print(args, end=end_, file=sys.stderr)

def spaceout(x: int) -> str:
    return len(str(x)) * ' '

def repp(filler: str, points: list[int]) -> str:
    string = ""
    for i in points:
        if len(string) < i - 1:
            string+= (i - 1 - len(string)) * filler
        
        string+="^"
    
    return string

def fillfrp(fill: str, points: list[int], end: int) -> str:
    string = ""
    for i in points:
        if len(string) < i - 1:
            string+= (i - 1 - len(string)) * fill
        
        string+=" "

    if len(string) < end:
        while len(string) < end:
            string+="^"

    return string


def Format(OgStr: str, Foramtter: dict) -> str:
    for i in list(Foramtter.keys()):
        OgStr = OgStr.replace("!{" + i + "}", Foramtter[i])

    return OgStr