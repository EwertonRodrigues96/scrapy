# -*- coding: utf-8 -*-
import scrapy
import json

class IfoodspiderSpider(scrapy.Spider):
    name = 'ifood_spider'
    allowed_domains = ['i.com']
    start_urls = ['http://i.com/']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start_requests(self):
        file_latlong = open('/home/ewerton/Documentos/ifood/ifood/spiders/config/lat_long_municipio_brasil.json')
        file_latlong_json = json.load(file_latlong)
        for dados in file_latlong_json:
            url ='https://marketplace.ifood.com.br/v1/merchants?latitude={}&longitude={}&channel=IFOOD&size=100'.format(dados.get('latitude'),dados.get('longitude'))
            yield scrapy.Request(url=url,callback=self.idlojas,dont_filter=True)
    
    
    def idlojas(self,response):
        jsontex = response.text
        arqjson =json.loads(jsontex)
        urls ='https://www.ifood.com.br/api/restaurants/ '
        for ids in arqjson['merchants'] :
                #ids.get('id')
                urls = 'https://www.ifood.com.br/api/restaurants/{}'.format(ids.get('id'))
                yield scrapy.Request(url=urls,callback = self.parse, dont_filter=True)
        pass 
  
    def parse(self, response):
        jsontex=response.text
        arqjson = json.loads(jsontex)
        dados=arqjson['data']['restaurant']
        restaurant_id=dados.get('id')


        uudi = dados.get('uuid')
        company_group = dados.get('companyGroup')
        descricao = dados.get('description')
        site_url = dados.get('siteUrl')
        phone = dados.get('phoneIf')
        street_number = dados['address'].get('streetNumber')
        zip_code = dados['address']['location'].get('zipCode')
        logradouro = dados['address']['location'].get('address')
        dependent_address = dados['address']['location'].get('dependentAddress')
        district = dados['address']['location'].get('district')
        city = dados['address']['location'].get('city')
        uf = dados['address']['location'].get('state')
        country = dados['address']['location'].get('country')
        lat = dados['address']['location'].get('lat')
        log = dados['address']['location'].get('lon')
        delivery_time = dados['address']['location'].get('deliveryTime')
        main_food_type = dados['mainFoodType'].get('code')
        description = dados['mainFoodType'].get('description')
        name_main_food_type = dados['mainFoodType'].get('name')
        avaliacao_media = dados.get('evaluationAverage')
        yield {
            'Rede': 'Ifood',
            'Url do site': site_url,
            'tipo nome principal': name_main_food_type,
            'Logradouro': logradouro,
            'Numero_local': street_number ,
            'Cidade': city ,
            'uf': uf ,
            'Cep': zip_code ,
            'Pais': country, 
            'latitude': lat ,
            'longitude':  log ,
            'telefone': phone ,
            'idRede': uudi ,
            'Group_companhia' : company_group ,
            'Descriçao' : descricao,
            'dependets endereco': dependent_address,
            'Distrito': district ,            
            'Tempo e entrega': delivery_time,
            'tipo principal': main_food_type,
            'Descrição': description,
            
            'Avaliaçao': avaliacao_media
        }

        pass
