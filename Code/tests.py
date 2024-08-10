import re

def has_more_than_five_words(text):
    # Remove symbols and keep only alphanumeric characters and spaces
    cleaned_text = re.sub(r'[^\w\s]', '', text)
    
    # Split the cleaned text into words based on whitespace
    words = cleaned_text.split()
    
    # Check if the number of words is greater than 5
    return len(words) > 5
  
print(re.sub(r'[^\w\s]', '', "This is -- a self-explained example").split())

a = 1
b = None
print((1, "aaa", a if a == 0 else "joder", "hola" if b == None else b))
