import argparse

def add(a, b):
    print(f"The sum is: {a + b}")

def subtract(a, b):
    print(f"The difference is: {a - b}")

def main():
    parser = argparse.ArgumentParser(description="A CLI calculator.")
    subparsers = parser.add_subparsers(title="commands", dest="command")

    # Add subcommand: add
    parser_add = subparsers.add_parser("add", help="Add two numbers")
    parser_add.add_argument("a", type=int, help="First number")
    parser_add.add_argument("b", type=int, help="Second number")

    # Add subcommand: subtract
    parser_sub = subparsers.add_parser("subtract", help="Subtract two numbers")
    parser_sub.add_argument("a", type=int, help="First number")
    parser_sub.add_argument("b", type=int, help="Second number")

    args = parser.parse_args()

    if args.command == "add":
        add(args.a, args.b)
    elif args.command == "subtract":
        subtract(args.a, args.b)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
