import voca.utils.json as json

with open("./test/book.json", mode="rt") as f:
    book = json.load(f)