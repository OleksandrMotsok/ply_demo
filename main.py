from core.engine import parser

if __name__ == "__main__":
    print(parser.parse("a = 2 + 2 * 2"))
    print(parser.parse("foo(a)"))





