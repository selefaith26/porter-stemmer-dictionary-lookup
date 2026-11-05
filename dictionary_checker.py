import argparse
import os
import time

from porter_stemmer import stem

UNIX_DICTIONARY = "/usr/share/dict/words"
BUNDLED_DICTIONARY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "words.txt")


# 1. Load the dictionary, one word per line, letters only
def load_dictionary(path):
    words = set()
    with open(path, encoding="utf-8", errors="ignore") as f:
        for line in f:
            word = line.strip().lower()
            if word.isascii() and word.isalpha():
                words.add(word)
    return words


# 2. Stem every dictionary word and remember which words share each stem
def build_stem_index(words):
    index = {}
    for word in words:
        index.setdefault(stem(word), []).append(word)
    return index


# 3. Clean the user's input and look it up
def clean_input(text):
    word = text.strip().strip(".,;:!?\"'()[]").lower()
    if word.isascii() and word.isalpha():
        return word
    return None


def look_up(text, index):
    word = clean_input(text)
    if word is None:
        return None, None, []
    word_stem = stem(word)
    matches = index.get(word_stem, [])
    return ("yes" if matches else "no"), word_stem, matches


# 4. Print one answer
def show_answer(text, index):
    answer, word_stem, matches = look_up(text, index)
    if answer is None:
        print("Please enter a single word made of letters only.")
        return
    shown = ", ".join(sorted(matches)[:4]) + (" ..." if len(matches) > 4 else "")
    detail = f"stem '{word_stem}'" + (f", dictionary: {shown}" if matches else "")
    print(f"{answer}   ({detail})")


# 5. Run
def run_demo():
    index = build_stem_index({"swim", "fish", "cheese"})
    print("Dictionary: swim, fish, cheese")
    for word in ["swimming", "fishing", "cheeses", "chocolate", "swam"]:
        print(f"> {word}")
        show_answer(word, index)


# 6. Main program
def main():
    parser = argparse.ArgumentParser(description="Stemmed dictionary lookup")
    parser.add_argument("--dict", help="path to a word list (default: UNIX words file or words.txt)")
    parser.add_argument("--demo", action="store_true", help="run the swim/fish/cheese example")
    args = parser.parse_args()

    if args.demo:
        run_demo()
        return

    path = args.dict or (UNIX_DICTIONARY if os.path.exists(UNIX_DICTIONARY) else BUNDLED_DICTIONARY)
    start = time.time()
    words = load_dictionary(path)
    index = build_stem_index(words)
    print(f"Loaded {len(words):,} words ({len(index):,} distinct stems) from {path} in {time.time() - start:.1f} seconds")
    print("Type a word to check it, or 'quit' to stop.")

    while True:
        try:
            text = input("> ")
        except EOFError:
            break
        if text.strip().lower() in ("quit", "exit"):
            break
        show_answer(text, index)


if __name__ == "__main__":
    main()
