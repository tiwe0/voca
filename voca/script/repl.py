from voca.interface.repl import Repl
from voca.model.book import book


def main():
    repl = Repl(book=book)
    print("welcome to voca!")
    while True:
        try:
            stmt = input("> ")
            repl.eval(stmt)
        except KeyboardInterrupt:
            print("Have a good day.")
            exit

if __name__ == "__main__":
    main()