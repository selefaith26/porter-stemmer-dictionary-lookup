# Porter stemming algorithm, following Porter (1980), "An algorithm for suffix stripping"

VOWELS = "aeiou"


# 1. Letter tests used by the rules
def is_consonant(word, i):
    ch = word[i]
    if ch in VOWELS:
        return False
    if ch == "y":
        return i == 0 or not is_consonant(word, i - 1)
    return True


def measure(stem):
    # m is the number of vowel-consonant (VC) groups in the stem
    m = 0
    previous_was_vowel = False
    for i in range(len(stem)):
        if is_consonant(stem, i):
            if previous_was_vowel:
                m += 1
            previous_was_vowel = False
        else:
            previous_was_vowel = True
    return m


def has_vowel(stem):
    return any(not is_consonant(stem, i) for i in range(len(stem)))


def ends_double_consonant(word):
    return len(word) >= 2 and word[-1] == word[-2] and is_consonant(word, len(word) - 1)


def ends_cvc(word):
    # consonant-vowel-consonant, where the last consonant is not w, x or y
    if len(word) < 3:
        return False
    return (is_consonant(word, len(word) - 3) and not is_consonant(word, len(word) - 2)
            and is_consonant(word, len(word) - 1) and word[-1] not in "wxy")


# 2. Rule tables: (suffix, replacement), tried longest suffix first
STEP2 = [("ational", "ate"), ("tional", "tion"), ("enci", "ence"), ("anci", "ance"),
         ("izer", "ize"), ("abli", "able"), ("alli", "al"), ("entli", "ent"), ("eli", "e"),
         ("ousli", "ous"), ("ization", "ize"), ("ation", "ate"), ("ator", "ate"),
         ("alism", "al"), ("iveness", "ive"), ("fulness", "ful"), ("ousness", "ous"),
         ("aliti", "al"), ("iviti", "ive"), ("biliti", "ble")]

STEP3 = [("icate", "ic"), ("ative", ""), ("alize", "al"), ("iciti", "ic"),
         ("ical", "ic"), ("ful", ""), ("ness", "")]

STEP4 = ["al", "ance", "ence", "er", "ic", "able", "ible", "ant", "ement", "ment",
         "ent", "ion", "ou", "ism", "ate", "iti", "ous", "ive", "ize"]


def replace_suffix(word, rules, min_measure):
    # Only the longest matching suffix is considered; its condition decides the outcome
    for suffix, replacement in sorted(rules, key=lambda r: -len(r[0])):
        if word.endswith(suffix):
            stem = word[:-len(suffix)]
            if measure(stem) > min_measure:
                return stem + replacement
            return word
    return word


# 3. The five steps
def step1a(word):
    if word.endswith("sses"):
        return word[:-2]
    if word.endswith("ies"):
        return word[:-2]
    if word.endswith("ss"):
        return word
    if word.endswith("s"):
        return word[:-1]
    return word


def step1b(word):
    if word.endswith("eed"):
        return word[:-1] if measure(word[:-3]) > 0 else word
    stem = None
    if word.endswith("ed") and has_vowel(word[:-2]):
        stem = word[:-2]
    elif word.endswith("ing") and has_vowel(word[:-3]):
        stem = word[:-3]
    if stem is None:
        return word
    if stem.endswith(("at", "bl", "iz")):
        return stem + "e"
    if ends_double_consonant(stem) and stem[-1] not in "lsz":
        return stem[:-1]
    if measure(stem) == 1 and ends_cvc(stem):
        return stem + "e"
    return stem


def step1c(word):
    if word.endswith("y") and has_vowel(word[:-1]):
        return word[:-1] + "i"
    return word


def step2(word):
    return replace_suffix(word, STEP2, 0)


def step3(word):
    return replace_suffix(word, STEP3, 0)


def step4(word):
    for suffix in sorted(STEP4, key=lambda s: -len(s)):
        if word.endswith(suffix):
            stem = word[:-len(suffix)]
            if suffix == "ion" and not stem.endswith(("s", "t")):
                return word
            return stem if measure(stem) > 1 else word
    return word


def step5a(word):
    if word.endswith("e"):
        stem = word[:-1]
        m = measure(stem)
        if m > 1 or (m == 1 and not ends_cvc(stem)):
            return stem
    return word


def step5b(word):
    if measure(word) > 1 and ends_double_consonant(word) and word.endswith("l"):
        return word[:-1]
    return word


# 4. The stemmer
def stem(word):
    word = word.lower()
    if len(word) <= 2:
        return word
    for step in (step1a, step1b, step1c, step2, step3, step4, step5a, step5b):
        word = step(word)
    return word
