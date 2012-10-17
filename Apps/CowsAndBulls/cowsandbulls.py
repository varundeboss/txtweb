import sys
import random
from itertools import combinations

class CowsAndBulls():
    def __init__(self,len_word):
        #self.myword = myword
        self.len_word = len_word
        #fObj = open('/usr/share/dict/words','r')
        fObj = open('/home/varun/Varun/Python/words.txt','r')
        self.wordlist = [word.strip().lower().replace('\n','') for word in fObj.read().split('\n') if word and self.check_word_alphabet(word)]
        self.wordlist = [word for word in self.wordlist if len(word) == len(set(word))]
        fObj.close()

        self.wanted_wordlist = [word for word in self.wordlist if len(word) == self.len_word and self.check_word_alphabet(word)]
        self.guesslist = []
        self.guess = ""
        self.possibles = {}
        for index in range(0,self.len_word):self.possibles[str(index)] = []

    def check_word_alphabet(self,word):
        for letter in word:
            if not letter.isalpha():
                return False
        return True
    
    def do_backtrace(self):
        #wanted_wordlist_copy = [i for i in self.wanted_wordlist]
        #guesslist_copy = [j for j in self.guesslist]
        #possibles_copy = self.possibles.copy()

        print "Possibles : ",self.possibles
        print "Length of wanted words list : ",len(self.wanted_wordlist)
        return self.wanted_wordlist[random.randrange(0,len(self.wanted_wordlist))]

    def get_guess_from_engine(self):
        self.wanted_wordlist_len = len(self.wanted_wordlist)
        wanted_wordlist_copy = [i for i in self.wanted_wordlist]
        if not self.guesslist:
            guess = self.wanted_wordlist[random.randrange(0,len(self.wanted_wordlist))]
            self.wanted_wordlist.remove(guess)
            return guess

        if self.guesslist:
            latest_dict = self.guesslist[-1] 
            latest_word = latest_dict.keys()[0]
            cows,bulls = latest_dict[latest_word]
        
        if not cows and not bulls:
            for word in wanted_wordlist_copy:
                my_flag = False
                for latest_letter in latest_word:    
                    if latest_letter in word:
                        my_flag = True
                if my_flag and self.wanted_wordlist:
                    self.wanted_wordlist.remove(word)                      
        else:         
            # Find words with equal number of bulls and cows
            for word in wanted_wordlist_copy:
                mybulls = 0
                mycows = 0
                #if word == "bubble":import pdb;pdb.set_trace()
                for index in range(0,self.len_word):
                    if word[index] == latest_word[index]:mybulls+=1
                    elif word[index] in latest_word and word[index] != latest_word[index]:mycows+=1                    	       	        
                
                #if word == "bubble":import pdb;pdb.set_trace()
                if (bulls != mybulls or cows!=mycows) and word in self.wanted_wordlist:
                    self.wanted_wordlist.remove(word)
        #print "Removal for : ",latest_word,cows,bulls
        # Remove all words with the letters in the above word from the wanted_wordlist when both cows and bulls are 0
        #import pdb;pdb.set_trace()
        '''
        if not cows and not bulls:
            for word in wanted_wordlist_copy:
                my_flag = False
                for latest_letter in latest_word:    
                    if latest_letter in word:
                        my_flag = True
                if my_flag and self.wanted_wordlist:
                    self.wanted_wordlist.remove(word)
            
            for latest_letter in latest_word:
                for index in self.possibles.keys():
                    if latest_letter in self.possibles[index]:
                        self.possibles[index].remove(latest_letter)
            
        #elif bulls > 0 or cows > 0:
        #    for index in self.possibles.keys():
        #        self.possibles[index] = [letter for letter in latest_word]
                
        else:
            
            for index in self.possibles.keys():
                for letter in latest_word:
                    if letter not in self.possibles[index]:
                        self.possibles[index].append(letter)
            for word in wanted_wordlist_copy:
                my_flag = False
                for latest_letter in latest_word:
                    if latest_letter in word:
                        my_flag = True
                if not my_flag and word in self.wanted_wordlist:
                    self.wanted_wordlist.remove(word)
            
            # Find words with equal number of bulls and cows
            for word in wanted_wordlist_copy:
                mybulls = 0
                for index in range(0,self.len_word):
                    if word[index] == latest_word[index]:mybulls+=1
                if bulls != mybulls:
                    self.wanted_wordlist.remove(word)
            import pdb;pdb.set_trace()
            # Get permutations and remove words that doesn't contain the permutation
            comb_gen = combinations(latest_word,cows+bulls)
            for word in wanted_wordlist_copy:
                flag_list = []
                for tpl in comb_gen:
                    my_flag = False
                    for let in tpl:
                        if let not in word:
                            my_flag = True
                    flag_list.append(my_flag)
                if False not in flag_list and word in self.wanted_wordlist:
                    self.wanted_wordlist.remove(word) 
        '''
            
        if latest_word in self.wanted_wordlist:self.wanted_wordlist.remove(latest_word)

        #if self.wanted_wordlist_len - len(self.wanted_wordlist) == 1:
        #    pass
            
        #guess = self.do_backtrace() 
        #print "Gold in list : ", "cold" in self.wanted_wordlist
        #print "Possibles : ",self.possibles
        #print "Length of wanted words list : ",len(self.wanted_wordlist)  
        
        #random_guess = self.wanted_wordlist[random.randrange(0,len(self.wanted_wordlist))]

        if self.wanted_wordlist:return self.wanted_wordlist[random.randrange(0,len(self.wanted_wordlist))]
        else:return False
  
    def start_guessing(self,cows,bulls):
        print "\n"
        if self.guess:self.guesslist.append({self.guess : [cows,bulls]});print "----------> Guesses so far <----------"
        for guess_dict in self.guesslist:
            guess_dict = dict(guess_dict)
            key = guess_dict.keys()[0]
            print str(key) + " has " + str(guess_dict[key][0]) + " cows and " + str(guess_dict[key][1]) + " bulls"
        print "--------------------------------------\n"

        guess = self.get_guess_from_engine()
        return guess

    def cowsandbulls(self,guess,word):
        cows = 0
        bulls = 0
        for index in range(0,self.len_word):
            if guess[index] == word[index]:bulls+=1
            elif guess[index] in word and guess[index] != word[index]:cows+=1
        return cows,bulls


    def check_ans(self,ans):
        length = self.len_word
        guesslist_copy = [j for j in self.guesslist]

        if length != len(ans):
            print "\nHello! When I asked for the length of the word, you said that it is '",length,"' and now you are giving me a '",len(ans),"' letter word"
            sys.exit(1)

        flag = False
        for guess_dict in guesslist_copy:
            anscows,ansbulls = self.cowsandbulls(guess_dict.keys()[0],ans)
            mycows,mybulls   = guess_dict.values()[0]

            if anscows != mycows or ansbulls != mybulls:
                flag = True
                print "\nDude when asked for the word '",guess_dict.keys()[0],"' you said it has '",mycows,"' cows and '",mybulls,"' bulls.\n\
                      But it actually has '",anscows,"' cows and '",ansbulls,"' bulls."

        if not flag:
            if ans in self.wordlist:
                print "\nHey I know this word!!! Don't know how the fu*k I missed it!!!"
            else:
                print "\nWhat the f**k is '",ans,"' ?????!!!!!"
        else:
            print "\nFu**er!!! Just go to kindergardens and start over!!!"
        

if __name__ == "__main__": 
    flag = "ERROR"
    #myword = raw_input("What is the word : ")
    def check_int(length=0,ignore_zero=False):
        try:
            if str(length) == "0" and not ignore_zero:raise
            len_word = int(length)
            return len_word
        except:
            print "Dude I need the length!!! Not some random s**t\n"
            return "ERROR"
    
    while flag=="ERROR":
        length = raw_input("Ok temme the length of the word and I will start guessing the word : ")
	flag = check_int(length)
        
    #cbObj = CowsAndBulls(flag,myword)
    cbObj = CowsAndBulls(flag)
    cows = 0
    bulls = 0
    master_flag = True
    while master_flag:
        if cbObj.len_word == bulls:
            print "\n\nHurray!!! I got the word. It's '" + str(cbObj.guess) + "'"
            sys.exit(1)
        cbObj.guess = cbObj.start_guessing(cows=cows,bulls=bulls)
        master_flag = cbObj.guess
        if cbObj.guess:
            print "My guess : ",cbObj.guess
            #cows,bulls = cbObj.cowsandbulls()
            #print "Cows and Bulls : ",cows,bulls
        
        flag = "ERROR"
        while flag=="ERROR" and master_flag:
            cows = raw_input("So how many cows : ")
            flag = check_int(cows,ignore_zero=True)
        cows = flag

        flag = "ERROR"
        while flag=="ERROR" and master_flag:
            bulls = raw_input("And bulls : ")
            flag = check_int(bulls,ignore_zero=True)
        bulls = flag
   
    ans = raw_input("\nDude I give up. What word did you think of : ") 
    cbObj.check_ans(ans)
