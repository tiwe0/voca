import re
import voca.utils.json as json
from typing import Set, Mapping, Any, Tuple


class Repl:

    cmd_regx: Mapping[str, str] = {
        r'add (?P<new_word>[a-zA-Z]{1,}) from (?P<old_word>[a-zA-Z]{1,}) for (?P<reason>.*)': 'add_word_from_word_for_reason',
        r'check (?P<word>[a-zA-Z]{1,})': 'check_word',
        r'quit': 'quit',
    }

    def __init__(self, book: Mapping[str, Any]) -> None:
        self.voca_book: Mapping[str, str] = book['voca']
        self.voca_mem: Mapping[str, Set[Tuple[str, str]]] = book['mem']

    def parse(self, stmt: str):
        for regx, method_name in self.cmd_regx.items():
            matched = re.match(pattern=regx, string=stmt)
            if matched:
                return (getattr(self, method_name), matched.groupdict())
        return -1, -1

    def eval(self, stmt: str):
        method, kwargs = self.parse(stmt=stmt)
        if method == -1:
            print(f"invalide command: {stmt}")
            return -1
        return method(**kwargs)

    def add_word_from_word_for_reason(self, new_word: str, old_word: str, reason: str):
        if new_word not in self.voca_book:
            print(f"new word {new_word} not in voca book.")
            return -1
        if old_word not in self.voca_book:
            print(f"origin word {old_word} not in voca book.")
            return -1
        if old_word not in self.voca_mem:
            print(f"origin word {old_word} not in voca mem, adding it.")
            self.voca_mem[old_word] = set()
        if not isinstance(self.voca_mem[old_word], set):
            self.voca_mem[old_word] = set(self.voca_mem[old_word])
        new_relation_tuple = (new_word, reason)
        if new_relation_tuple in self.voca_mem[old_word]:
            print(f"current relation already in mem, skip.")
            return -1
        self.voca_mem[old_word].add(new_relation_tuple)
        print(f"relations: {old_word} -> [{new_word} , {reason}] added.")
        return 0

    def check_word(self, word: str):
        if word not in self.voca_book:
            print(f"word {word} not in book.")
            return -1
        print(f"""{word}:
{self.voca_book[word]}
""")
        return 0

    def save(self):
        print("saving...")
        with open("./test/book.json", "wt") as f:
            json.dump({'voca':self.voca_book, 'mem':self.voca_mem}, f, ensure_ascii=False)
        print("saved.")

    def quit(self):
        self.save()
        print("bye~")
        print("")
        exit()

    def quit_without_save(self):
        print("bye~")
        print("")
        exit()