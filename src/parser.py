from dataclasses import dataclass
from typing import Literal


@dataclass
class Holder:
    pos: int
    number: bool = False
    open_quote: Literal["'", '"', None] = None
    close_quote: bool = False


def parse(query: str):
    holder = None
    position = 0
    print(query)

    literals = []
    for c in query:
        print(c, end="")
        if c in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            if holder is None:
                holder = Holder(pos=position)
                print(" FOUND NUMBER WITHOUT QUOTE")
            elif holder.open_quote is None:
                print(" FOUND NUMBER WITHOUT QUOTE")
        elif c == ".":
            if holder and not holder.open_quote and query[position - 1].isdigit():
                print(" FOUND PERIOD AFTER NUMBER")
            elif not holder:
                holder = Holder(pos=position)
        elif c in ("'", '"'):
            if c == "'":
                print(" FOUND SINGLE QUOTE")
            else:
                print(" FOUND DOUBLE QUOTE")
            if holder is None:
                holder = Holder(pos=position, open_quote=c)
                print(f"OPEN STRING WITH {c}")
            elif holder.open_quote == c:
                holder.close_quote = c
                print(f"CLOSE STRING WITH {c}")
        elif c in (" ", ",", ";"):
            if c == " ":
                print(" FOUND SPACE")
            elif c == ",":
                print(" FOUND COMMA")
            else:
                print(" FOUND END")
            if holder:
                if holder.open_quote is None:
                    try:
                        literals.append(int(query[holder.pos : position]))
                    except ValueError:
                        try:
                            literals.append(float(query[holder.pos : position]))
                        except ValueError:
                            literals.append(query[holder.pos : position])
                    holder = None
                    print("RESET HOLDER 1")
                elif holder.open_quote and holder.close_quote:
                    literals.append(query[holder.pos + 1 : position - 1])
                    holder = None
                    print("RESET HOLDER 2")

        elif c != " ":
            print(" FOUND VALUE TO STORE")
            if holder is None:
                holder = Holder(pos=position)
        elif c == ";":
            print(" FOUND END")
            if position > holder.pos:
                literals.append(query[holder.pos : position])
            print("RESET THE HOLDER 3")
            break
        else:
            print(f"not caught: {c}")

        position += 1

    print(literals)
    return literals


def assign_nodes(literals: list):
    parsed = []

    for lit in literals:
        if lit in ("TRUE", "FALSE", "true", "false"):
            parsed.append(Bool(lit))
        elif isinstance(lit, str):
            if lit in KEYWORDS:
                parsed.append(Keyword(value=lit))
            else:
                parsed.append(Str(value=lit))
        elif isinstance(lit, int):
            parsed.append(Int(value=lit))
        elif isinstance(lit, float):
            parsed.append(Float(value=lit))
        else:
            raise ValueError(f"Unknown object type: {lit}")

    return parsed


KEYWORDS = ["SELECT"]


@dataclass
class Keyword:
    value: str


@dataclass
class Str:
    value: str


@dataclass
class Int:
    value: int


@dataclass
class Float:
    value: float


@dataclass
class Bool:
    value: str


class Buffer:
    value: str
    kind: str


def is_single_quote(v: str):
    if v == "'":
        return True
    return False


def is_double_quote(v: str):
    if v == '"':
        return True
    return False


def is_char(v: str):
    if v.isalpha():
        return True
    return False


def is_number(v: str):
    if v in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0"):
        return True
    return False


class Boolean:
    _value: bool

    def __str__(self):
        return self.value

    @staticmethod
    def is_type(val):
        if val in ("TRUE", "FALSE", "true", "false"):
            return Boolean
        return None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if value.lower() == "true":
            self._value = True
        elif value.lower() == "false":
            self._value = False


class Number:
    value: int

    def __str__(self):
        return self.value

    @staticmethod
    def is_type(val):
        if "." in val:
            return None
        try:
            int(val)
            return Number
        except ValueError:
            return None
