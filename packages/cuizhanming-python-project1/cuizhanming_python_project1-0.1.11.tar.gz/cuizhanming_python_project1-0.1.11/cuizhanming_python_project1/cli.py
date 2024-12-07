import argparse

from cuizhanming_python_project1.services import get_random_poem, declaim

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("declaim", help="Declaim a random poem")
    args = parser.parse_args()

    if args.declaim:
        poem = get_random_poem()
        declaim(poem["title"], poem["poem"], poem["author"])


if __name__ == "__main__":
    main()