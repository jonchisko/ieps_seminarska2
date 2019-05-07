import codecs
from bs4 import BeautifulSoup
import sys

def is_tag(s):
    return "<" in s

def find_body(items):
    body_start = 0
    body_end = 0

    for i in range(len(items)):
        if "<body" in items[i]:
            body_start = i
        if "</body" in items[i]:
            body_end = i

    return body_start, body_end

def process_file(filename):
    page = codecs.open(filename, "r")
    document = BeautifulSoup(page.read(), features="lxml")
    ss = document.prettify()
    ss_split = [x.strip() for x in ss.split("\n") if x]

    processed1 = []
    buffer = " "

    #zdruzi vse stringe v 1 line
    for i in range(len(ss_split)):
        if is_tag(ss_split[i]):
            processed1.append(ss_split[i])
        else:
            if not is_tag(ss_split[i]):
                buffer += ss_split[i].strip() + " "
            if is_tag(ss_split[i + 1]):
                processed1.append(buffer.strip())
                buffer = ""

    #zdej bi hotl se da delamo samo z body
    body_start, body_end = find_body(processed1)
    return processed1[body_start:body_end+1]

class RoadRunner:

    def __init__(self, wrapper, sample):
        self.wrapper = wrapper
        self.sample = sample

    def is_tag(self, token):
        return "<" in token

    def is_string(self, token):
        return not self.is_tag(token)

    def tag_match(self, token1, token2):
        token1_split = token1.split()
        token2_split = token2.split()

        return token1_split[0] == token2_split[0]

    def string_match(self, token1, token2):
        return token1 == token2

    def clean_object(self, object):
        sol = []
        for item in object:
            if self.is_tag(item):
                sol.append(self.clean_token(item))
            else:
                sol.append("#PCDATA")
        return sol

    def clean_token(self, token):
        has_starting_tag = "<" in token
        has_start_ending_tag = "/>" in token
        has_ending_tag = "</" in token

        ss = token.split()
        if len(ss) > 1:
            if has_starting_tag and has_start_ending_tag:
                return ss[0] + "/>"
            else:
                if has_starting_tag and not has_start_ending_tag:
                    return ss[0] + ">"
                if has_ending_tag:
                    return ss[0] + ">"
        else:
            return ss[0]

    def match_square(self,square1, square2):

        for item1, item2 in zip(square1, square2):
            if self.is_tag(item1) and self.is_tag(item2):
                if self.tag_match(item1, item2):
                    continue
                else:
                    return False
            else:
                if self.is_string(item1) and self.is_string(item2):
                    continue
                else:
                    return False
        return True

    def check_optional(self, i, j):
        tag1 = self.wrapper[i]
        tag2 = self.sample[j]

        optional1 = 0
        for ii in range(i, len(self.wrapper)):
            if self.wrapper[ii] == tag2:
                optional1 = ii
                break

        optional2 = 0
        for jj in range(j, len(self.sample)):
            if self.sample[jj] == tag1:
                optional2 = jj
                break
        if optional1 and not optional2:
            return "wrapper", i, optional1
        if optional2 and not optional1:
            return "sample", j, optional2

        if optional2 - j < optional1 - i:
            return "sample", j, optional2
        else:
            return "wrapper", i, optional1

    def check_iterator(self, i, j):
        terminal_tag1 = self.wrapper[i - 1]
        terminal_tag2 = self.sample[j - 1]

        if not self.tag_match(terminal_tag1, terminal_tag2):
            return None

        #find other terminal tags
        lower_terminal_tag1 = None
        lower_terminal_tag2 = None

        try:
            lower_terminal_tag1 = self.wrapper[i:].index(terminal_tag1)
        except:
            pass

        try:
            lower_terminal_tag2 = self.sample[j:].index(terminal_tag2) + j
        except:
            pass

        if not lower_terminal_tag1 and not lower_terminal_tag2:
            return None
        if lower_terminal_tag1 and not lower_terminal_tag2:
            the_terminal_tag = ("wrapper", lower_terminal_tag1)
        if not lower_terminal_tag1 and lower_terminal_tag2:
            the_terminal_tag = ("sample", lower_terminal_tag2)
        if lower_terminal_tag1 and lower_terminal_tag2:
            the_terminal_tag = ("wrapper", lower_terminal_tag1) if lower_terminal_tag1 < lower_terminal_tag2 else ("sample", lower_terminal_tag2)



        #zdej nrdimo square
        if the_terminal_tag[0] == "wrapper":
            the_square = self.wrapper[i:the_terminal_tag[1] + 1]

        else:
            the_square = self.sample[j:the_terminal_tag[1] + 1]

        #okej zdej mam shranjen square zdej je treba pomatchat
        #iteriras cez wrapper navzgor dokler se matcha pa vse zbrises


        #sepravi najprej se sprehodim naprej po unem fajlu k sm najdu iterator in sledim dokler ga se najdm
        #tko dobim kje se konca in premaknem pointer za un file na tisto tocko
        #potem grem na drugi fajl in tam najdem celotn del iteratorja in premaknem njegov pointer na konec
        #potem morem pa se zamenjat vse elemente iteratorja za iterator sepravi backtrackat
        if not the_square:
            return None

        #zdej smo najdl kje se koncata oba iteratorja
        wrapper_end_of_iterator = None
        sample_end_of_iterator = None
        if the_terminal_tag[0] == "wrapper":
            for ii in range(i,len(self.wrapper), len(the_square)):
                second_sqaure = self.wrapper[ii:ii + len(the_square)]
                if self.match_square(the_square, second_sqaure):
                    continue
                else:
                    wrapper_end_of_iterator = ii - 1
                    sample_end_of_iterator = j - 1
                    break

        if the_terminal_tag[0] == "sample":
            for jj in range(j,len(self.sample), len(the_square)):
                second_sqaure = self.sample[jj:jj+len(the_square)]
                if self.match_square(the_square, second_sqaure):
                    continue
                else:
                    sample_end_of_iterator = jj - 1
                    wrapper_end_of_iterator = i - 1
                    break

        #zdej je treba najdt kje se je zacel wrapper iterator
        #uzamemo the square pa gremo gor od tm kje je bil mismatch
        wrapper_start_of_iterator = None

        for ii in range(1, int(i/len(the_square))+1):
            start_of_square = i - (len(the_square)*ii)
            end_of_the_square = start_of_square+len(the_square)
            searching_square = self.wrapper[start_of_square:end_of_the_square+1]

            if not self.match_square(the_square, searching_square):
                wrapper_start_of_iterator = start_of_square + len(the_square)

        return sample_end_of_iterator, wrapper_start_of_iterator, wrapper_end_of_iterator, self.clean_object(the_square)

    def start(self):
        i = 0
        j = 0

        result = []

        while True:
            if i >= len(self.wrapper) or j >= len(self.sample):
                break
            token1 = self.wrapper[i]
            token2 = self.sample[j]

            if self.is_string(token1) and self.is_string(token2):
                if self.string_match(token1, token2):
                    #result.append(token1)
                    self.wrapper[i] = token1
                    i += 1
                    j += 1
                    continue
                else:
                    #result.append("#PCDATA")
                    self.wrapper[i] = "#PCDATA"
                    i += 1
                    j += 1
                    continue

            if self.is_tag(token1) and self.is_tag(token2):
                if self.tag_match(token1, token2):
                    #result.append(self.clean_token(token1))
                    self.wrapper[i] = self.clean_token(token1)
                    i += 1
                    j += 1
                    continue
                else:
                    iterator = self.check_iterator(i, j)

                    if iterator and all(iterator):
                        sample_end_of_iterator, wrapper_start_of_iterator, wrapper_end_of_iterator, iterator_square = iterator
                        prvi_del = self.wrapper[:wrapper_start_of_iterator]
                        drugi_del = self.wrapper[wrapper_end_of_iterator + 1:]
                        self.wrapper = prvi_del + [("Iterator", iterator_square)] + drugi_del
                        i = wrapper_start_of_iterator + 1
                        j = sample_end_of_iterator + 1
                    else:
                        file, start_optional, end_optional = self.check_optional(i, j)
                        if file == "wrapper":
                            if end_optional:
                                #a = t[:i+1] + [4] + t[i+1:]
                                optional = self.wrapper[start_optional:end_optional]
                                self.wrapper = self.wrapper[:i] + [("Optional" ,self.clean_object(optional))] + self.wrapper[i:]
                                i = end_optional + 1
                                continue
                        else:
                            if end_optional:
                                optional = self.sample[start_optional:end_optional]
                                self.wrapper = self.wrapper[:i] + [("Optional", self.clean_object(optional))] + self.wrapper[i:]
                                j = end_optional
                                i += 1
                                continue
            i += 1
            j += 1
        return result

tokens1 = process_file(sys.argv[1])
tokens2 = process_file(sys.argv[2])

rr = RoadRunner(tokens1, tokens2)
rr.start()
counter = 0
buffer = ""
for x in rr.wrapper:
    if "document.write" not in x and "script" not in x and "//" not in x and "<!--" not in x and "-->" not in x:
        buffer += str(x) + " "
        counter += len(x)
    if counter > 100:
        print(buffer)
        buffer = ""
        counter = 0

