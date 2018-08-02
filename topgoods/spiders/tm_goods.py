# -*- coding: utf-8 -*-
import scrapy
from topgoods.items import TopgoodsItem

class TmGoodsSpider(scrapy.Spider):
    name = "tm_goods"
    allowed_domains = ["http://www.tmall.com"]
    start_urls = (
        'http://list.tmall.com/search_product.htm?type=pc&totalPage=100&cat=50025135&sort=d&style=g&from=sn_1_cat-qp&active=1&jumpto=10#J_Filter',
    )
    #记录处理的页数
    count=0 
     
    def parse(self, response):

        TmGoodsSpider.count += 1
        text = response.text
        divs1 = response.xpath("//div[@id='J_ItemList']/div[@class='product']/div")
        divs = response.xpath("//*[@id='J_ItemList']/div[1]/div")
        divs2 = response.xpath("//*[@id='J_ItemList']/div")
        if not divs:
            self.log( "List Page error--%s"%response.url )
              
        for div in divs2:
            item=TopgoodsItem()
            #商品价格
            # //*[@id="J_ItemList"]/div[1]/div/p[1]/em
            item["GOODS_PRICE"] = div.xpath("//p[@class='productPrice']/em/@title")[0].extract()
            #商品名称
            item["GOODS_NAME"] = div.xpath("//p[@class='productTitle']/a/@title")[0].extract()
            #商品连接
            pre_goods_url = div.xpath("//p[@class='productTitle']/a/@href")[0].extract()
            item["GOODS_URL"] = pre_goods_url if "http:" in pre_goods_url else ("http:"+pre_goods_url)
            
            yield scrapy.Request(url=item["GOODS_URL"],meta={'item':item},callback=self.parse_detail,
            dont_filter=True)

    def parse_detail(self,response):

        div = response.xpath('//div[@class="extend"]/ul')
        if not div:
            self.log( "Detail Page error--%s"%response.url )
            
        item = response.meta['item']
        div=div[0]
        #店铺名称
        item["SHOP_NAME"] = div.xpath("li[1]/div/a/text()")[0].extract()
        #店铺连接
        item["SHOP_URL"] = div.xpath("li[1]/div/a/@href")[0].extract()
        #公司名称
        item["COMPANY_NAME"] = div.xpath("li[3]/div/text()")[0].extract().strip()
        #公司所在地
        item["COMPANY_ADDRESS"] = div.xpath("li[4]/div/text()")[0].extract().strip()
        print(item)
        yield item