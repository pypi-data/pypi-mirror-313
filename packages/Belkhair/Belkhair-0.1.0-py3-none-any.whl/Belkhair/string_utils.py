def capitalize_each_word(sentence):
    """Capitalize each word in a sentence."""
    return ' '.join(word.capitalize() for word in sentence.split())

def reverse_string(s):
    """Reverse a given string."""
    return s[::-1]
