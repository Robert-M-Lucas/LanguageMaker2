import markdown
import os
import shutil


def compile():
    print("Cache not created, creating now...")

    try:
        shutil.rmtree("CACHE")
    except FileNotFoundError:
        pass

    os.mkdir("CACHE")

    with open("VERSION.txt", "r") as v:
        with open("CACHE/CACHE_VERSION.txt", "w+") as cv:
            cv.write(v.read())

    os.mkdir("CACHE/CompiledHelpText")

    help_files = [f for f in os.listdir("HelpText") if os.path.isfile(os.path.join("HelpText", f))]

    for f in help_files:
        with open(f"HelpText/{f}", "r") as rf:
            with open(f"CACHE/CompiledHelpText/{f}.html", "w+") as html:
                html.write(markdown.markdown(rf.read()))


if not os.path.exists("CACHE"):
    compile()
elif not os.path.exists("CACHE/CACHE_VERSION.txt"):
    compile()
else:
    failed = False
    with open("VERSION.txt", "r") as v:
        with open("CACHE/CACHE_VERSION.txt", "r") as cv:
            if v.read() != cv.read():
                failed = True
    if failed:
        compile()
