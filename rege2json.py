import re
import sys
import json

class Html2Json:



    def html2json(self, site_type, html_path):
        json = None
        with open(html_path, "rt") as f:
            html = "\n".join(f.readlines())
            if site_type == "rtv":
                json = self.rtv2json(html)
            elif site_type == "over":
                json = self.over2json(html)
            elif site_type == "other":
                json = self.over2json(html)
            else:
                print("Wrong site type! Possible options: 'rtv', 'over' and 'other'.")
                exit(42)
        return json

    def rtv2json(self, html):
        #/gm!!!
        author = '<div class="author-name">([a-z A-ZžčšŽČŠ]*)<\/div>'
        datum = '<div class="publish-meta">\n*[\t]*([\w.: ]*)<br>'
        title = '<header class="article-header">[\n\t\w\-=".,?!:<> \/;#žčšŽŠČ\-\–]*<\/h1>'
        subtitle = '<div class="subtitle">[\w .,?!:\nžčšŽŠČ\-\–]*<\/div>'
        lead = '<p class="lead">[\w .,?!:\nžčšŽŠĆ\-\–]*<\/p>'
        content = '<article class="article">[ \n\t<>\w=\/"\-\':;(),.|čšžŠŽČ+\[\]\{\}?!&%\\^\*\–]*<\/article>'
        m = re.findall(datum, html, re.MULTILINE)
        print(m)

    def over2json(self, html):
        pass

    def sth2json(self, html):
        pass


if __name__ == '__main__':
    args = sys.argv
    """if len(args) != 3:
        print("Two arguments need to be passed: site type and path to html file!")
        print("Example: rege2json rtv './files/sth.html'")
        exit(41)
    site_type = args[1]
    html_path = args[2]"""
    h2j = Html2Json()

    #testing
    site_type="rtv"
    html_path = "WebPages/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html"
    result_json = h2j.html2json(site_type, html_path)