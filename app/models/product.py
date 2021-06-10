from app import app
from app.models.opinion import Opinion
from app.utils import extractElement
from bs4 import BeautifulSoup
import pandas as pd
import requests
import json



class Product:

    url_pre = 'https://www.ceneo.pl'
    url_post = '#tab=reviews'

    def __init__(self, productId=None, name=None, opinions=[], avarageScore=None, opinionsCount=None, prosCount=None, consCount=None):
        self.productId = productId
        self.name = name
        self.opinions = opinions.copy()
        self.avarageScore = avarageScore
        self.opinionsCount = opinionsCount
        self.prosCount = prosCount
        self.consCount = consCount

    def opinionsPageUrl(self):
        return self.url_pre+'/'+self.productId+self.url_post
    
    def extractName(self):
        respons = requests.get(self.opinionsPageUrl())
        if respons.status_code == 200:
            pageDOM = BeautifulSoup(respons.text, 'html.parser')
            self.name = extractElement(
                pageDOM, 'h1.product-top__product-info__name')
        return self.name

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

    def countProductStatistics(self):
        opinions = self.opinionsToDataFrame()
        self.avarageScore = float(opinions['stars'].mean())
        self.opinionsCount = len(self.opinions)
        self.prosCount = int(opinions['advantages'].count())
        self.consCount = int(opinions['disadvantages'].count())

    def exportProduct(self):
        with open("app/products/{}.json".format(self.productId), "w", encoding="UTF-8") as jf:
            json.dump(self.productToDict(), jf, indent=4, ensure_ascii=False)
        with open("app/opinions/{}.json".format(self.productId), "w", encoding="UTF-8") as jf:
            json.dump(self.opinionsToDictsList(), jf, indent=4, ensure_ascii=False)

    def importProduct(self):
        with open("app/products/{}.json".format(self.productId), "r", encoding="UTF-8") as jf:
            product = json.load(jf)
            self.__init__(**product)
        with open("app/opinions/{}.json".format(self.productId), "r", encoding="UTF-8") as jf:
            opinions = json.load(jf)
            for opinion in opinions:
                self.opinions.append(Opinion(**opinion))
            return self

    def __str__(self):
        return '''productId: {}<br>
        name: {}<br>'''.format(self.productId, self.name)+"<br>".join(str(opinion) for opinion in self.opinions)

    def toDict(self):
        return self.productToDict()|{"opinions": self.opinionsToDictsList()}
        

    def productToDict(self):
        return {
            "productId": self.productId,
            "name": self.name,
            "avarageScore": self.avarageScore,
            "opinionsCount": self.opinionsCount,
            "prosCount": self.prosCount,
            "consCount": self.consCount

        }

    def opinionsToDictsList(self):
        return [opinion.toDict() for opinion in self.opinions]

    def opinionsToDataFrame(self):
        #opinions = pd.DataFrame.from_records(
            #[opinion.toDict() for opinion in self.opinions])
        opinions = pd.json_normalize([opinion.toDict() for opinion in self.opinions])
        return opinions

    def jsonToCsv(self):
        #df = pd.read_json(r'opinions\{product}.json')
        #df.to_csv(r'opinions_csv\product.csv', index = None)
        pass