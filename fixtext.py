import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from spellchecker import SpellChecker
import language_check

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')


def fix_spelling(paragraph):
    # Tokenize the paragraph into words
    words = word_tokenize(paragraph)

    # Initialize a spell checker
    spell = SpellChecker()

    # Create an empty list to store the corrected words
    corrected_words = []

    # Loop through each word in the list of words
    for i, word in enumerate(words):
        # Check if the word is misspelled or if it is spelled correctly but not in the right form
        if not wordnet.synsets(word) or word != spell.correction(word):
            # Get the previous and next words (if they exist)
            prev_word = words[i - 1] if i > 0 else ""
            next_word = words[i + 1] if i < len(words) - 1 else ""

            # Look up synonyms for the previous and next words
            prev_synonyms = wordnet.synsets(prev_word) if prev_word else []
            next_synonyms = wordnet.synsets(next_word) if next_word else []

            # Look for a synonym of the misspelled word that also appears in the context
            for synset in wordnet.synsets(word):
                for lemma in synset.lemmas():
                    if lemma.name() in [l.name() for l in prev_synonyms + next_synonyms]:
                        corrected_words.append(lemma.name())
                        break
                else:
                    continue
                break
            else:
                # If no suitable synonyms are found, try using the corrected version of the word from the spell checker
                corrected = spell.correction(word)
                if corrected is not None:
                    corrected_words.append(corrected)
        else:
            # If the word is spelled correctly and in the right form, use the original word
            corrected_words.append(word)

    # Join the corrected words back into a paragraph
    corrected_paragraph = ' '.join(corrected_words)
    return corrected_paragraph


def fix_grammar(text):
    tool = language_check.LanguageTool('en-US')
    matches = tool.check(text)
    corrected_text = language_check.correct(text, matches)
    return corrected_text


paragraph = "i really want to went to the store but i dont have no money"
corrected_paragraph = fix_grammar(paragraph)
print(corrected_paragraph)
