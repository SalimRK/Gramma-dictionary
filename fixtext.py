import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from spellchecker import SpellChecker
import re
import string
from gingerit.gingerit import GingerIt

# import enchant

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


# def fix_grammar(paragraph):
#
#     # Split the paragraph into words
#     words = paragraph.split()
#
#     # Create a dictionary for English language
#     d = enchant.Dict("en_US")
#
#     # Loop through the words and check for spelling errors
#     for i in range(len(words)):
#         if not d.check(words[i]):
#             suggestions = d.suggest(words[i])
#             if len(suggestions) > 0:
#                 words[i] = suggestions[0]
#
#     # Join the corrected words back into a sentence
#     corrected_paragraph = ' '.join(words)
#
#     return corrected_paragraph

def fix_grammar(text):
    # Initialize grammar checker
    parser = GingerIt()

    pattern = r"([^\w\s])"

    # split text into sentences
    sentences = re.split("(?<=[.!?]) +", text)

    # loop through each sentence and correct errors
    for i, sentence in enumerate(sentences):
        # check if the sentence contains punctuation marks
        has_punctuations = bool(re.search(pattern, sentence))
        # use GingerIt to correct errors
        result = parser.parse(sentence)
        if has_punctuations:
            # if sentence has punctuation marks, include them in the corrected text
            corrected_sentence = re.sub(pattern, r"\g<1> ", result['result'])
        else:
            # otherwise, exclude them
            corrected_sentence = result['result'].strip()
        # check if corrections exist in the result
            if "corrections" in result:
                # convert list to dictionary
                corrections = {c['text']: c['correct'] for c in result['corrections']}
                # loop through each correction and replace the original text with the corrected text
                for original, correction in corrections.items():
                    corrected_sentence = corrected_sentence.replace(original, correction)
            # update the sentences list with the corrected sentence
            sentences[i] = corrected_sentence
        # join the sentences back into a paragraph
        corrected_text = " ".join(sentences)
        return corrected_text