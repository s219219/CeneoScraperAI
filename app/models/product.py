from app import app
from app.utils import extractElement
from app.models.opinion import Opinion
import requests
import json
from bs4 import BeautifulSoup

class Product:

    url_pre = 'https://www.ceneo.pl'
    url_post = '#tab=reviews'

    def __init__(self, productId=None, name=None, opinions=[]):
        self.productId = productId
        self.name = name
        self.opinions = opinions

    def opinionsPageUrl(self):
        return self.url_pre+'/'+self.productId+self.url_post
    
    def extractProduct(self):
        url = self.opinionsPageUrl()
        while url:
            respons = requests.get(url)
            pageDOM = BeautifulSoup(respons.text, 'html.parser')
            opinions = pageDOM.select("div.js_product-review")
            for opinion in opinions:
                self.opinions.append(Opinion().extractOpinion(opinion).transformOpinion())
            try:
                url = self.url_pre + extractElement(pageDOM, 'a.pagination__next', "href") 
            except TypeError:
                url = None

    def exportProduct(self):
        with open("app/opinions/{}.json".format(self.productId), "w", encoding="UTF-8") as jf:
            json.dump(self.toDict(), jf, indent=4, ensure_ascii=False)

    def __str__(self):
        return '''productId: {}<br>
        name: {}<br>'''.format(self.productId, self.name)+"<br>".join(str(opinion) for opinion in self.opinions)

    def toDict(self):
        return {
            "productId": self.productId,
            "name": self.name,
            "opinions": [opinion.toDict() for opinion in self.opinions]
        }
        