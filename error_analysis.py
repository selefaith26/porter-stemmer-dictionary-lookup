import random

from dictionary_checker import BUNDLED_DICTIONARY, build_stem_index, load_dictionary, look_up
from porter_stemmer import ends_cvc, is_consonant, stem

random.seed(42)
words = load_dictionary(BUNDLED_DICTIONARY)
index = build_stem_index(words)
long_words = sorted(w for w in words if len(w) >= 6)
sample = random.sample(long_words, 5000)


def yes_rate(candidates):
    hits = sum(look_up(w, index)[0] == "yes" for w in candidates)
    return hits, len(candidates)


# 1. Regular inflections that are not in the dictionary (should be yes)
print("1. Regular inflections of 5,000 sampled words, written correctly")
plain_ends = ("s", "x", "z", "ch", "sh", "ic", "ed", "ing", "ly", "ive", "ous", "al", "ful", "less", "ness", "ment", "ion", "er", "or", "able", "ible", "ity", "ish", "ism", "ist", "ate", "ize", "ant", "ent")
safe = [w for w in long_words if not ends_cvc(w) and not w.endswith(plain_ends)]
forms = []
for w in random.sample(safe, 5000):
    if w.endswith("e"):
        forms += [w + "s", w + "d", w[:-1] + "ing"]
    elif w.endswith("y") and is_consonant(w, len(w) - 2):
        forms += [w[:-1] + "ies", w[:-1] + "ied", w + "ing"]
    else:
        forms += [w + "s", w + "ed", w + "ing"]
forms = [f for f in forms if f not in words]
hits, total = yes_rate(forms)
print(f"   {hits:,} of {total:,} answered yes ({100 * hits / total:.1f}%)")
misses = [f for f in forms if look_up(f, index)[0] == "no"]
print("   examples that failed:", ", ".join(random.sample(misses, min(10, len(misses)))))

# 2. Irregular forms, with a dictionary that holds only the base words
print("2. Irregular forms against a base-word dictionary")
irregular = {"swim": "swam", "go": "went", "run": "ran", "eat": "ate", "see": "saw", "sing": "sang",
             "write": "wrote", "buy": "bought", "teach": "taught", "think": "thought", "break": "broke",
             "choose": "chose", "drive": "drove", "give": "gave", "take": "took", "know": "knew",
             "child": "children", "mouse": "mice", "goose": "geese", "foot": "feet", "tooth": "teeth",
             "man": "men", "woman": "women", "good": "better", "knife": "knives", "leaf": "leaves"}
small = build_stem_index(set(irregular))
rejected = [form for form in irregular.values() if look_up(form, small)[0] == "no"]
print(f"   {len(rejected)} of {len(irregular)} rejected: {', '.join(rejected)}")
accepted = [form for form in irregular.values() if look_up(form, small)[0] == "yes"]
print(f"   accepted: {', '.join(accepted)}")

# 3. Wrong spellings that stemming lets through
print("3. Misspellings of the same 5,000 words")
wrong = [w + "eing" for w in sample]
wrong = [w for w in wrong if w not in words]
hits, total = yes_rate(wrong)
print(f"   extra e before -ing (for example walkeing): {hits:,} of {total:,} answered yes ({100 * hits / total:.1f}%)")
cut = [w[:-1] for w in sample if w[:-1] not in words]
hits, total = yes_rate(cut)
print(f"   last letter removed: {hits:,} of {total:,} answered yes ({100 * hits / total:.1f}%)")
swap = []
for w in sample:
    i = random.randrange(1, len(w) - 2)
    t = w[:i] + w[i + 1] + w[i] + w[i + 2:]
    if t not in words:
        swap.append(t)
hits, total = yes_rate(swap)
print(f"   two letters swapped: {hits:,} of {total:,} answered yes ({100 * hits / total:.1f}%)")

# 4. Unrelated words that share a stem, and related words that do not
print("4. Collisions and misses")
print("   same stem, different meaning:")
for a, b in [("universe", "university"), ("organ", "organization"), ("general", "generate"),
             ("news", "new"), ("experience", "experiment"), ("authority", "author")]:
    if a in words and b in words:
        print(f"     {a} -> {stem(a)}, {b} -> {stem(b)}   {'collide' if stem(a) == stem(b) else 'different'}")
print("   related words, different stems:")
for a, b in [("absorb", "absorption"), ("knife", "knives"), ("matrix", "matrices"), ("analysis", "analyses"),
             ("decide", "decision"), ("explain", "explanation"), ("happy", "happiness"), ("sleep", "slept")]:
    if a in words and b in words:
        print(f"     {a} -> {stem(a)}, {b} -> {stem(b)}   {'same' if stem(a) == stem(b) else 'different'}")

# 5. Size of the stem index
shared = sum(1 for v in index.values() if len(v) > 1)
print(f"5. {len(words):,} words reduce to {len(index):,} stems; {shared:,} stems are shared by two or more words")
