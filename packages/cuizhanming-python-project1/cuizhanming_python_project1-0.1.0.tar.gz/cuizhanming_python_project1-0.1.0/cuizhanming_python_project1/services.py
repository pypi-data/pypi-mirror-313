import requests

def declaim(title, poem, author):
    print("---------------------------------------------------")
    print(f"{title}\n")
    print(poem)
    print(f"\nBy {author}")
    print("---------------------------------------------------")

def get_random_poem():
    response = requests.get("https://poetrydb.org/random")
    response.raise_for_status()
    poem = response.json()[0]

    return dict(
        title=poem["title"],
        poem="\n".join(poem["lines"]),
        author=poem["author"]
    )