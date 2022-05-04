'''Task 2: Write a python script that uses `words.txt` to find and print
the anagram with the largest number of variants. Also find and print the
longest pair of words that are anagrams of each other.'''


from collections import defaultdict
from itertools import chain

d = defaultdict(list)

with open('words.txt', 'r') as f:
    lines = [line.strip() for line in f]
    for line in lines:
        sorted_line = ''.join(sorted(line))
        d[sorted_line].append(line)

anagrams = [d[k] for k in d if len(d[k]) > 1]

print (f'largest number of variants:  {max(anagrams, key=len)}') #largest number of variants

longest_word = max(chain.from_iterable(anagrams), key = len)
list_index = [(i,a.index(longest_word)) for i, a in enumerate(anagrams) if longest_word in a]
print(f'longest pair of words that are anagrams of each other: {anagrams[list_index[0][0]]}') #longest pair of words that are anagrams of each other