import argparse
import random

def main():
    parser = argparse.ArgumentParser(description="Motivational Quotes Generator")
    parser.add_argument("count", type=int, help="Number of quotes to generate")
    parser.add_argument("--output", help="Output file to save quotes", default=None)
    args = parser.parse_args()

    quotes = [
        "Believe you can and you're halfway there.",
        "You are stronger than you think.",
        "The only limit to our realization of tomorrow is our doubts of today.",
        "The future belongs to those who believe in the beauty of their dreams.",
        "Do not wait to strike till the iron is hot; but make it hot by striking."
    ]

    try:
        selected_quotes = [random.choice(quotes) for _ in range(args.count)]

        if args.output:
            with open(args.output, 'w') as f:
                for quote in selected_quotes:
                    f.write(quote + "\n")
            print(f"{args.count} quotes written to {args.output}")
        else:
            for quote in selected_quotes:
                print(quote)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()