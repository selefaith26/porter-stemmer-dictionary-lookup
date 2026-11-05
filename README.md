# Porter Stemmer Dictionary Lookup

Python implementation of Porter's stemming algorithm (Porter, 1980) with a stemmed dictionary lookup. The user types a word, and the program answers yes if the word's stem matches the stem of a dictionary word, and no if it does not.

With a dictionary of swim, fish and cheese, the program says yes to swimming, fishing and cheeses, and no to chocolate and swam.

CST-585 Advanced Applications in AI, NLP Application Analysis Part Two.

## Files

| File | Purpose |
| --- | --- |
| porter_stemmer.py | Porter's algorithm: measure, conditions, and steps 1a to 5b |
| dictionary_checker.py | Builds the stem index and runs the yes/no lookup |
| test_stemmer.py | 15 unit tests, including a comparison with NLTK on every dictionary word |
| error_analysis.py | Measures over-stemming, under-stemming, irregular forms and misspellings |
| words.txt | web2 word list (234,450 words) used when /usr/share/dict/words is missing |
| test_output.txt, error_analysis_output.txt, sample_run.txt | Saved outputs |

## Requirements

Python 3. The program itself needs no extra libraries. Only the NLTK comparison test needs `pip install nltk`.

## How to run

Interactive lookup (type `quit` to stop):

    python dictionary_checker.py

Assignment example (swim, fish, cheese):

    python dictionary_checker.py --demo

Use a different dictionary file:

    python dictionary_checker.py --dict path/to/words

Run the tests:

    python -m unittest -v

Run the error analysis:

    python error_analysis.py

The program uses /usr/share/dict/words when it exists and falls back to the bundled words.txt.

## Example

    > swimming
    yes   (stem 'swim', dictionary: swim)
    > chocolate
    no   (stem 'chocol')

## Known limits

Porter's rules look only at spelling, so some unrelated words share a stem (universe and university), some related words do not (absorb and absorption), and irregular forms such as swam are not recognized. A yes means the stems match, not that the word is correctly spelled.

## Reference

Bird, S., Klein, E., & Loper, E. (2009). Natural language processing with Python. O'Reilly Media.

Lovins, J. B. (1968). Development of a stemming algorithm. Mechanical Translation and Computational Linguistics, 11(1–2), 22–31.

Manning, C. D., Raghavan, P., & Schütze, H. (2008). Introduction to information retrieval. Cambridge University Press.

Artificial Vision and Language Processing for Robotics By Álvaro Morena Alberola , Gonzalo Molina Gallego , Unai Garay Maestre (April 2019) Packt Publishing
ISBN: 9781838552268

Porter, M. F. (1980). An algorithm for suffix stripping. Program, 14(3), 130–137.

Merriam-Webster. (1934). Webster’s new international dictionary of the English language (2nd ed.). G. & C. Merriam Company.

Porter, M. F. (2001). Snowball: A language for stemming algorithms. http://snowballstem.org/texts/introduction.html



