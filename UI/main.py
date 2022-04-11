import eel

from exposes import *

def main():
    eel.init("src")
    eel.start("index.html", port=8050, size=(1270, 800), position=(0, 0))

if __name__ == "__main__":
    main()

    