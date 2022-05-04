'''Task 1: Construct a function that given a list of words, returns a dictionary
whose keys are the letters of a word sorted into alphabetical order and whose
values are lists of all the words with that key.'''

keys = ['apple', 'taste', 'state', 'astte', 'leapp', 'eappl']
dictionary = {}

def func(word, keys):
    anagram = []

    for i in keys:
        alphabetical_order = ''.join(sorted(i))
        if sorted(word) == sorted(i):
            anagram.append(i)
            dictionary[alphabetical_order] = anagram
        
    return dictionary

for i in keys:
    func(i,keys)

print(dictionary)