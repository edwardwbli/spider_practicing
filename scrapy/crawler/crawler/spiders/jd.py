# -*- coding: utf-8 -*-

from scrapy import Spider
from scrapy import Request
from utils import extract,extract_one
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import Selector
from scrapy_splash import SplashRequest
from crawler.items import Good
import re

class JDSpider(Spider):
    name='jd'
    download_delay = 0
    allowed_domains=['jd.com']
#    start_urls=['http://www.jd.com/']
    start_urls=['http://www.jd.com/allSort.aspx','http://jiadian.jd.com','http://shouji.jd.com/','http://shuma.jd.com/','http://mobile.jd.com/','http://diannao.jd.com/','http://channel.jd.com/home.html','http://channel.jd.com/furniture.html','http://channel.jd.com/decoration.html','http://channel.jd.com/kitchenware.html','http://channel.jd.com/1315-1342.html','http://channel.jd.com/1315-1343.html','http://channel.jd.com/children.html','http://channel.jd.com/1315-1345.html','http://channel.jd.com/beauty.html','http://channel.jd.com/1620-1625.html','http://channel.jd.com/pet.html','http://channel.jd.com/shoes.html','http://channel.jd.com/bag.html','http://channel.jd.com/jewellery.html','http://channel.jd.com/1672-2615.html','http://channel.jd.com/sports.html','http://channel.jd.com/watch.html','http://car.jd.com/','http://che.jd.com','http://baby.jd.com','http://channel.jd.com/toys.html','http://channel.jd.com/food.html','http://channel.jd.com/wine.html','http://fresh.jd.com','http://china.jd.com','http://channel.jd.com/health.html','http://book.jd.com/','http://mvd.jd.com/','http://e.jd.com/ebook.html']
    #//list.jd.com/list.html?cat=737,794,870
    normal_url_pattern=[r'.*list\.jd\.com/list\.html']
    normal_url_extractor=LxmlLinkExtractor(allow=normal_url_pattern)
    #http://list.jd.com/list.html?cat=1672,2615,9186&page=1&sort=sort_totalsales15_desc&go=0&JL=4_2_0
    needed_url_pattern=[r'.*list\.jd\.com/list\.html.*&sort=sort_totalsale.*']
    needed_url_extractor=LxmlLinkExtractor(allow=needed_url_pattern)
    count_url=[]
    """
    types= {('手机', '家用电器', '数码', '电脑', '办公', '电脑、办公',
             '大 家 电','电脑办公','大家电'): 'TR_SM',
         ('母婴','母婴玩具'): 'TR_MY',
         ('进口食品','食品', '酒类', '生鲜', '特产', '营养保健', '食品饮料'): 'TR_SP',
         ('玩具乐器', '运动户外'): 'TR_WT',
         ('服饰', '鞋靴', '箱包', '珠宝', '奢侈品', '男装',
          '女装', '童装', '内衣', '珠宝首饰', '礼品箱包', '服饰内衣','腕表','钟表'): 'TR_FS',
         ('个护化妆', '清洁用品','化妆品','个人护理'): 'TR_HZP',
         ('汽车', '汽车用品','汽车配件','宠物', '宠物生活'): 'TR_ZH',
         ('家居', '家具', '厨具', '家居家装', '家装', '家装建材','家纺','家饰'): 'TR_JJ'
         }
    """

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url,callback=self.parse,args={
                'wait':4.5,'html':1,})

    def parse(self,response):
        for link in self.normal_url_extractor.extract_links(response):
            yield SplashRequest(link.url,callback=self.parse_url,args={'wait':0.5,'html':1,})

    def parse_url(self,response):
        for link in self.needed_url_extractor.extract_links(response):
            if 'ev' not in link.url:
                url=re.sub(r'page=.*&','page=1&',link.url)
                url=re.sub(r'stock=.*&','stock=0&',url)
                url=re.sub(r'delivery_daofu=.*&','delivery_daofu=0&',url)
                url=re.sub(r'delivery=.*&','delivery=0&',url)
                yield SplashRequest(url,callback=self.parse_item,args={'wait':0.5,'html':1,})

    def parse_item(self,response):
        hxs=Selector(response)
        item_titles=extract(hxs,"//div[@class='gl-i-wrap j-sku-item']//a/em/text()")
        top_id=extract_one(hxs,'//*[@id="J_crumbsBar"]/div/div/div/div[1]/a/text()')
#        type_id=extract_one(hxs,'//*[@id="J_crumbsBar"]/div/div/div/div[3]/div/div[1]/span/text()')
#        type_id=re.findall(r'.*cat=(.*)&',response.url)[0].split('&')[0]
        type_id1=extract(hxs,'//*[@id="J_crumbsBar"]//div[@class="trigger"]/span/text()')[0]
        type_id2=extract(hxs,'//*[@id="J_crumbsBar"]//div[@class="trigger"]/span/text()')[-1]

        if type_id1!=type_id2:
            for i,t in enumerate(item_titles):
                if i<20:
                    good={
                        'mall':'2',
                        'rank':str(i+1),
                        'title':t,
                        'price':'0',
                        'turnover_index':'0',
                        'top_id':top_id,
                        'type_id1':type_id1,
                        'type_id2':type_id2,
                        'url':response.url
                    }

                    yield Good(good)



        for link in self.needed_url_extractor.extract_links(response):
            if 'ev' not in link.url:
                url = re.sub(r'page=.*&', 'page=1&', link.url)
                url = re.sub(r'stock=.*&', 'stock=0&', url)
                url = re.sub(r'delivery_daofu=.*&', 'delivery_daofu=0&', url)
                url = re.sub(r'delivery=.*&', 'delivery=0&', url)
                yield SplashRequest(url, callback=self.parse_item, args={'wait': 0.5, 'html': 1,})







