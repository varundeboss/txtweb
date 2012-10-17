import sys,os
import mimetypes

class WordsInFile:
    def __init__(self,op):
        self.option = op
        self.outfile = "/home/varun/Varun/Python/words.txt"
        self.final_words_list = []

    def append_words(self,final_list):
        self.final_words_list.extend(final_list)
        self.final_words_list = list(set(self.final_words_list))

    def put_in_file(self):
        final_words_list_copy = [word for word in self.final_words_list]
        robj = open(self.outfile,'r')
        old_list = [word.strip().lower().replace('\n','') for word in robj.read().split('\n') if word]
        robj.close()

        self.final_words_list = list(set.difference(set(self.final_words_list),set(old_list)))
        if '' in self.final_words_list:self.final_words_list.remove('')
        fobj = open(self.outfile,'a')
        for word in self.final_words_list:
            fobj.write(word+'\n')
        fobj.close()

    def read_file(self,file_name):
        fobj = open(file_name,'r')
        fstr = fobj.read()
        fobj.close()
        spl_char_list = list(set([letter for letter in fstr if not letter.isalpha()]))
        for spl_char in spl_char_list:
            fstr = fstr.replace(spl_char,' ')
        final_list = list(set(fstr.lower().split(' ')))
        self.append_words(final_list)

    def read_dir(self,dir_name):
        self.files_list = []
        for full_tpl in os.walk(dir_name):
            self.files_list.extend(full_tpl[0]+'/'+file_name for file_name in full_tpl[2] if full_tpl[2] and 'text' in str(mimetypes.guess_type(file_name)[0]).lower())

        #import pdb;pdb.set_trace()
        for file_name in self.files_list:
            print file_name
            self.read_file(file_name)

if __name__ == "__main__":
    op = raw_input("File or Directory(f/d) : ")
    if op.lower() == 'f':
        filename = raw_input("File Name with full path : ")
        CObj = WordsInFile(op.lower())

        CObj.read_file(filename)
        CObj.put_in_file()

    elif op.lower() == 'd':
        dirname = raw_input("Directory's full path : ")
        CObj = WordsInFile(op.lower())

        CObj.read_dir(dirname)
        CObj.put_in_file()
    else:
        print "Dude do u know where the letters f and d are?? Yeah f is in f**k and d is in ur d**k"
        sys.exit(1)
