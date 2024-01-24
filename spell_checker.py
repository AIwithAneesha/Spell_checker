import streamlit as st
import re
from collections import Counter

# Function to tokenize words
def words(document):
    "Convert text to lower case and tokenize the document"
    return re.findall(r'\w+', document.lower())

# Create a frequency table of all the words in the document
all_words = Counter(words(open('big.txt').read()))

def edits_one(word):
    "Create all edits that are one edit away from `word`."
    alphabets = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [left + right[1:] for left, right in splits if right]
    inserts = [left + c + right for left, right in splits for c in alphabets]
    replaces = [left + c + right[1:] for left, right in splits if right for c in alphabets]
    transposes = [left + right[1] + right[0] + right[2:] for left, right in splits if len(right) > 1]
    return set(deletes + inserts + replaces + transposes)

def edits_two(word):
    "Create all edits that are two edits away from `word`."
    return (e2 for e1 in edits_one(word) for e2 in edits_one(e1))

def known(words):
    "The subset of `words` that appear in the `all_words`."
    return set(word for word in words if word in all_words)

def possible_corrections(word):
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits_one(word)) or known(edits_two(word)) or [word])

def prob(word, N=sum(all_words.values())): 
    "Probability of `word`: Number of appearances of 'word' / total number of tokens"
    return all_words[word] / N

def spell_check(word):
    "Return the most probable spelling correction for `word` out of all the `possible_corrections`"
    correct_word = max(possible_corrections(word), key=prob)
    if correct_word != word:
        return "Did you mean " + correct_word + "?"
    else:
        return "Correct spelling."

# Streamlit app
def main():
    st.title("Spell Checker App")
    
    # Input text from the user
    user_input = st.text_area("Enter text for spell checking:", "")
    
    # Button to initiate spell checking
    if st.button("Check Spelling"):
        # Tokenize the input text
        tokens = words(user_input)
        
        # Perform spell check for each token
        suggestions = [spell_check(token) for token in tokens]
        
        # Display the results
        st.markdown("### Spell Check Results:")
        for i, (token, suggestion) in enumerate(zip(tokens, suggestions)):
            st.text(f"{i + 1}. {token}: {suggestion}")

if __name__ == "__main__":
    main()

