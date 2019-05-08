# ieps_seminarska2
Seminarska 2 pri premdetu IEPS.
Ekstrakcija podatkov iz spletnih strani s pomočjo regularnih izrazov, x-patha in RoadRunner-like algoritma.
Vsi programi so napisani v Python 3.7.


# Navodila za uporabo RoadRunner-like algoritma:
0.) Namesti knjiznico bs4  
1.) Prenesi repozitorij  
2.) Premakni se v direktorij "implementation"  
3.) Za izvedbo algoritma nad rtvslo.si stranmi kliči: "test_runner.py ../input/volvox.html ../input/audix.html"  
4.) Za izvedbo algoritma nad overstock.com stranmi kliči: "test_runner.py ../input/jewelry01x.html ../input/jewelry02x.html"  
5.) Za izvedbo algoritma nad bolha.com stranmi kliči: "test_runner.py ../input/ps4_bolhax.html ../input/xbox_bolhax.html"  

# Navodila za uporabo ekstrakcije z XPath:
0.) Namesti lxml
1.) Premakni se v direktorij "implementation"
2.) Kliči "python test_runner.py [ over1 | over2 | rtv1 | rtv2 | other1 | other2 ]"

# Navodila za uporabo Regex funkcije:
0.) Namesti knjiznico re, sys in json (če še niso) 
1.) Prenesi repozitorij  
2.) Premakni se v direktorij "implementation"  
3.) Za izvedbo algoritma nad rtvslo.si stranmi kliči: "rege2json.py rtv ../input/audi.html"  
4.) Za izvedbo algoritma nad overstock.com stranmi kliči: "rege2json.py over ../input/jewelry01.html"  
5.) Za izvedbo algoritma nad bolha.com stranmi kliči: "rege2json.py other ../input/xbox_bolha.html"  
6.) V bistvu v splošnem se algoritem kliče tako: rege2json.py [rtv|over|other] file_path

