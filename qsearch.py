# immporting bin dictionary
# import ordering
from collections import Counter

cached_keywords = set()
partstobin = {}


class search:
    def __init__(self):
        splitter = '%'
        with open ("resources\\binnumbers.txt") as f:
            for element in f:
                try:
                    partstobin[(element.split(splitter)[0]).strip(" ")] = (element.split(splitter)[1])
                except:
                    print(element.split(splitter))
        # accessing binnumber values
        self.listed_parts = (partstobin).keys()

        for part in self.listed_parts:
            for key_word in (part.split(" ")):
                cached_keywords.add(key_word.strip(" "))
        print("Search Cache Finished, " + str(len(cached_keywords)) +" parts in memory.")

        self.word_count = Counter((" ".join(self.listed_parts)).split(" "))
        #print(" ".join(self.listed_parts).split(" "))
    
    def calculated_difference(self, key_word, part):
        #perfect match
        if key_word == part:
            return False
    
    #code sourced from http://norvig.com/spell-correct.html, generates words that are one letter away from the word
    def firstedits(self, word):
        "All edits that are one edit away from `word`."
        letters    = 'abcdefghijklmnopqrstuvwxyz1234567890' # using alphanumeric numbers
        splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)] #small for loops that create a list of every possible word split, used for the rest of the functions
        deletes    = [L + R[1:]               for L, R in splits if R] #creates list of every possible delete
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1] #transposition in words/misplacements
        replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters] # replaced letters, hitting the wrong key
        inserts    = [L + c + R               for L, R in splits for c in letters] #accidental insertions
        return set(deletes + transposes + replaces + inserts) # creates a set we can use to comapre later

    def secondedits(self, word): 
        "All edits that are two edits away from `word`."
        return (e2 for e1 in self.firstedits(word) for e2 in self.firstedits(e1)) #account for even more errors
    

    def autocorrect(self, word):
        def valid_word(subset_words):
            known = set()
            for word in subset_words:
                if word.upper() in self.word_count or word.lower() in self.word_count or word.title() in self.word_count:
                    known.add(word)
            return set(known)

        def calc_prob(word):
            total = sum(self.word_count.values())
            return (self.word_count[word]/total)

        def possible_candidates(word):
            return valid_word([word]).union(valid_word(self.firstedits(word)).union(valid_word(self.secondedits(word))))  

        #print(calc_prob(word))
        pos = possible_candidates(word)
        top_values = list(sorted(pos, key = calc_prob, reverse = True))

        ans = set()
        max_set_size = 5
        for value in top_values:
            if max_set_size <= 0:
                break
            else:
                ans.add(value.lower())
                max_set_size -= 1

        # if (len(valid_word([word])) != 0):
        #     print(valid_word([word]))
        #     return {word}
        return ans


    #takes primpt
    def generate_close_results(self, PROMPT):
        key_terms = (PROMPT.split(" ")) # Splitting prompt to analyse words
        built = set()
        for term in key_terms:
            print(term)
            print(self.autocorrect(term))
            built = built.union(self.autocorrect(term))
        #now, each word has been converted into a list of 3 probable meanings
        print(built)
        def score_part(PART_NAME):
            score = 0
            for subterm in PART_NAME.split(" "):
                if subterm.lower() in built:
                    score+=1
            return score
        
        #autocorrecting typos in keyterms
        top_ten = sorted(self.listed_parts, key = score_part, reverse = True)
        count = 5
        while(len(top_ten) != 10):
            top_ten.pop(len(top_ten)-1)
        return top_ten


