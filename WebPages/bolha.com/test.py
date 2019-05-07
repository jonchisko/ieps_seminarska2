import urllib
import codecs
from bs4 import BeautifulSoup

class Text:

    def __init__(self, text):
        self.type = "text"
        self.text = text

    def __str__(self):
        return self.text

class Tag:

    def __init__(self, text):
        self.type = "tag"
        self.text = text

    def __str__(self):
        return self.text

def is_tag(line):
    return line[0] == "<"

def preprocessing(filename):
    page = codecs.open(filename, "r", encoding="utf8")
    document = BeautifulSoup(page.read(), features="lxml")

    removed_comments = []
    semafor = False

    for line in document.prettify().split("\n"):
        if "<!--" in line:
            semafor = True
        if " -->" in line:
            semafor = False
            continue

        if not semafor:
            removed_comments.append(line)

    final = []
    buffer = ""

    for line in removed_comments:
        if len(line.strip()) > 0:
            if line.strip()[0] != "<":
                buffer += str(line.strip())
                continue
            if buffer:
                final.append(buffer)
                buffer = ""
            final.append(line.strip())


    true_final = []

    for line in final:
        if is_tag(line):
            true_final.append(Tag(line))
        else:
            true_final.append(Text(line))

    return true_final

def tag_match(line1, line2):
    tag1_split = line1.text.split()
    tag2_split = line2.text.split()

    return tag1_split[0] == tag2_split[0]

def text_match(line1, line2):
    return line1.text == line2.text

def compare_line(line1, line2):
    if line1.type == line2.type:
        if line1.type == "tag":
            return ("tag match", tag_match(line1, line2))
        else:
            return ("text match", text_match(line1, line2))
    else:
        return ("type match", False)


wrapper = preprocessing("ps4_bolha.html")
sample = preprocessing("xbox_bolha.html")


def find_optional(index_wrapper, index_sample):
    tag1 = wrapper[index_wrapper]
    tag2 = sample[index_sample]

    optional1 = 0
    for i in range(index_wrapper, len(wrapper)):
        if wrapper[i].text == tag2.text:
            optional1 = i
            break

    optional2 = 0
    for i in range(index_sample, len(sample)):
        if sample[i].text == tag1.text:
            optional2 = i
            break

    if optional2 - index_sample < optional1 - index_wrapper:
        return "sample", index_sample, optional2
    else:
        return "wrapper", index_wrapper, optional1


def square_match(square1, square2):
    for line1, line2 in zip(square1, square2):
        type, match = compare_line(line1, line2)

        if type == "tag match" and not match:
            return False
        if type == "type match":
            return False
    return True

def find_iterator(index_wrapper, index_sample):
    terminal_tag1 = wrapper[index_wrapper - 1]
    terminal_tag2 = sample[index_sample - 1]
    if terminal_tag1.text != terminal_tag2.text:
        return None, None, None

    square1 = 0
    square2 = 0

    for i in range(index_wrapper, len(wrapper)):
        if wrapper[i].text == terminal_tag1.text:
            square1 = i
            break

    for i in range(index_sample, len(sample)):
        if sample[i].text == terminal_tag2.text:
            square2 = i
            break

    #okej sepravi zdej mas dva square zdej pa matchas z stvarmi above
    #ce se noben ne ujema pac ni iterator, ce se pa ujema na nasprotnem potem gres naprej na sebi.

    #poglejmo torej ce se square1 matcha z sample
    square1_length = square1 - index_wrapper

    square1_realsquare = square_match(sample[index_sample-square1_length - 1:index_sample - 1], wrapper[index_wrapper:square1])

    #print(square1, index_wrapper, square1_length, square1_realsquare)
    #print("AAAAAAAAAAAAAAAAAAAAAA")
    #for y in wrapper[index_wrapper:square1]:
        #print(y)
    #print("BBBBBBBBBBBBBBBBBBBBBB")
    #for z in sample[index_sample-square1_length-1:index_sample-1]:
        #print(z)
    #print("AAAAAAAAAAAAAAAAAAAAAA")
    #print("****************")

    square2_length = square2 - index_sample
    square2_realsquare = square_match(wrapper[index_wrapper - square2_length - 1:index_wrapper - 1], sample[index_sample:square2])

    #print(square2, index_sample, square2_length, square2_realsquare)
    #print("AAAAAAAAAAAAAAAAAAAAAA")
    #for y in sample[index_sample:square2]:
        #print(y)
    #print("BBBBBBBBBBBBBBBBBBBBBB")
    #for z in wrapper[index_wrapper - square2_length - 1:index_wrapper - 1]:
        #print(z)
    #print("AAAAAAAAAAAAAAAAAAAAAA")
    #for y in sample[index_sample:square2]:
        #print(y)
    #print("----------")

    index_sol = None
    file = None
    the_square = None
    if square1_realsquare:
        if square1_length == 0:
            return None, None, None
        the_square  = wrapper[index_wrapper:square1]
        file = "wrapper"
        for j in range(index_wrapper, len(wrapper), square1_length):
            if square_match(wrapper[j:j+square1_length], the_square):
                index_sol = j+square1_length
        #nadaljujes na wrapperju in ubistvu sam returnas index kje se konca iterator in nek splosn zapis
    else:

        if square2_realsquare:
            if square2_length == 0:
                return None, None, None
            the_square = sample[index_sample:square2]
            file = "sample"
            for j in range(index_sample, len(sample), square2_length):
                if square_match(sample[j:j+square2_length], the_square):
                    index_sol = j + square2_length
            #nadaljujes na sample in ubistvu sam returnas index kje se konca iterator in nek splosn zapis

    return index_sol, the_square, file

def redifine_objects(object):
    solution = []
    for line in object:
        if line.type == "text":
            solution.append("#PCDATA")
        else:
            solution.append(line.text)
    return solution

i = 0
j = 0
result = []
while i < len(wrapper) and j < len(sample):

    match_type, match = compare_line(wrapper[i], sample[j])
    if match_type == "tag match" and match:
        print("A")
        result.append(wrapper[i].text)
    #ce je text mismatch na tokenu appendej #PCDATA
    if match_type == "text match" and not match:
        print("B")
        result.append("#PCDATA")
    if match_type == "type match":
        print("C")
        result.append(wrapper[i])
    #ce je tag mismatch
    if match_type == "tag match" and not match:

        #pogledas za iterator
        index_sol, the_square, file = find_iterator(i, j)

        #ce je
        if file and index_sol and the_square:

            #pogledas kir file je un k ma daljsi del iteratorja
            if file == "wrapper":

                #nastavis index za naprej raziskovanje na tja kjer se zakljuci iterator
                i = index_sol
            if file == "sample":
                j = index_sol


            result.append(("Iterator", redifine_objects(the_square)))

        #ce ni iterator recemo da je optional
        else:

            file, begin_optional, end_optional = find_optional(i, j)
            if file == "wrapper" and end_optional != 0:
                result.append(("Optional", redifine_objects(wrapper[i:end_optional + 1])))
                i = end_optional
            if file == "sample" and end_optional != 0:
                result.append(("Optional", redifine_objects(sample[i:end_optional + 1])))
                j = end_optional


    i += 1
    j += 1


for tag in result:
    print(tag)
