import re
import sys
import json


class Html2Json:



    def html2json(self, site_type, html_path):
        json = None

        if site_type == "over":
            f = open(html_path, "rt", encoding="windows-1252")
        else:
            f = open(html_path, "rt", encoding="utf-8")
        html = "\n".join(f.readlines())

        if site_type == "rtv":
            json = self.rtv2json(html)
        elif site_type == "over":
            json = self.over2json(html)
        elif site_type == "other":
            json = self.sth2json(html)
        else:
            print("Wrong site type! Possible options: 'rtv', 'over' and 'other'.")
            exit(42)
        f.close()
        return json

    def rtv2json(self, html):
        slovar = dict()
        #/gm!!!
        author = '<div class="author-name">([a-z A-ZžčšŽČŠ]*)<\/div>'
        datum = '<div class="publish-meta">\n*[\t]*([\w.: ]*)<br>'
        title = '<header class="article-header">[\n\t\w\-=".,?!:<> \/;#žčšŽŠČ\-\–]*<h1>([\w .,?!:\nžčšŽŠĆ\-\–]*)<\/h1>'
        subtitle = '<div class="subtitle">([\w .,?!:\nžčšŽŠČ\-\–]*)<\/div>'
        lead = '<p class="lead">([\w .,?!:\nžčšŽŠĆ\-\–]*)<\/p>'
        content = '<article class="article">([\w\W]*)<\/article>'

        slovar["Author"] = re.findall(author, html, re.MULTILINE)[0]
        slovar["PublishedTime"] = re.findall(datum, html, re.MULTILINE)[0]
        slovar["Title"] = re.findall(title, html, re.MULTILINE)[0]
        slovar["Subtitle"] = re.findall(subtitle, html, re.MULTILINE)[0]
        slovar["Lead"] = re.findall(lead, html, re.MULTILINE)[0]
        slovar["Content"] = re.findall(content, html, re.MULTILINE)[0]

        slovar = json.dumps(slovar)
        print(slovar)

    def over2json(self, html):
        slovar = dict()
        # /gm!!!
        title = '(?=<a\s+.*?href=".*?".*?><b>([\w\W]+?)<\/b>)(?=^(?!span).*$)'
        content = '<span class="normal">([\w\W]*?)<\/span>'
        price = '<span class="bigred"><b>\$([0-9,\.]*)<\/b><\/span>'
        listPrice = 'nowrap="nowrap"><s>\$([0-9\.,]*)<\/s><\/td>'
        saving = '<span class="littleorange">\$([0-9,\.]*) [\(\)\%0-9\.,]*?<\/span><\/td>'
        savingPercent = '<span class="littleorange">\$[0-9,\.]* \(([0-9]*?)\%\)<\/span><\/td>'

        titles = re.findall(title, html, re.MULTILINE)
        d = re.findall(content, html, re.MULTILINE)
        f = re.findall(price, html, re.MULTILINE)
        p = re.findall(listPrice, html, re.MULTILINE)
        op = re.findall(saving, html, re.MULTILINE)
        op2 = re.findall(savingPercent, html, re.MULTILINE)


        for i in range(len(p)):
            slovar[i] = {"Title": titles[i],
                         "Content": d[i],
                         "Price": f[i],
                         "ListPrice": p[i],
                         "Saving": op[i],
                         "SavingPercent":op2[i]}
        slovar = json.dumps(slovar)
        print(slovar)

    def sth2json(self, html):
        slovar = dict()
        #/gm!!!
        title = '<div class="coloumn content">[\w\W]{0,50}<a title="([\w :,;\-ščžŠČŽ]*)"'
        description = '<div class="coloumn content">[\w\W]*?<\/h3>[\n\t]*([\w\W ,:\-!?;.+ščžŠČŽ]*?)<\/div>'
        featured = '<div class="(ad|ad featured)">'
        price = '<div class="coloumn prices">[\w\W]*?<div class="price">[\W]*?<span>([0-9,]*?) €<\/span>'
        #oldPrice = '<div class="coloumn prices">[\W]*?<div class="oldPrice">[\W]*?<span>([0-9,]*?) €<\/span>'
        titles = re.findall(title, html, re.MULTILINE)
        d = re.findall(description, html, re.MULTILINE)
        f = re.findall(featured, html, re.MULTILINE)
        p = re.findall(price, html, re.MULTILINE)
        #op = re.findall(oldPrice, html, re.MULTILINE)

        for i in range(len(titles)):
            slovar[i] = {"Title": titles[i],
                         "Description": d[i].strip().replace("\t", "").replace("\n", "").replace("<b>", "").replace("</b>", ""),
                         "Price": p[i],
                         "Featured": True if f[i] == "ad featured" else False}
        slovar = json.dumps(slovar)
        print(slovar)


if __name__ == '__main__':
    args = sys.argv
    if len(args) != 3:
        print("Two arguments need to be passed: site type and path to html file!")
        print("Example: rege2json rtv './files/sth.html'")
        exit(41)
    site_type = args[1]
    html_path = args[2]
    h2j = Html2Json()

    h2j.html2json(site_type, html_path)