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
    name='tm'
    allowed_domains=['tmall.com']
    download_delay=0
    start_urls=['//nvzhuang.tmall.com/?spm=875.7931836.category2016010.1.ZxCttc&acm=lb-zebra-148799-667863.1003.8.708026&scm=1003.8.lb-zebra-148799-667863.ITEM_14561681423980_708026','//neiyi.tmall.com/?spm=875.7931836.category2016010.2.ZxCttc&acm=lb-zebra-148799-667863.1003.8.708026&scm=1003.8.lb-zebra-148799-667863.ITEM_14561681423980_708026','//nanzhuang.tmall.com/?acm=lb-zebra-148799-667863.1003.8.708026&scm=1003.8.lb-zebra-148799-667863.ITEM_14561677576501_708026','//sports.tmall.com/?acm=lb-zebra-148799-667863.1003.8.708026&scm=1003.8.lb-zebra-148799-667863.ITEM_14561677576501_708026','//nvxie.tmall.com/?acm=lb-zebra-148799-667863.1003.8.708026&scm=1003.8.lb-zebra-148799-667863.ITEM_14561689118972_708026','//nanxie.tmall.com/?acm=lb-zebra-148799-667863.1003.8.708026&scm=1003.8.lb-zebra-148799-667863.ITEM_14561689118972_708026','//bag.tmall.com/?acm=lb-zebra-148799-667863.1003.8.708026&scm=1003.8.lb-zebra-148799-667863.ITEM_14561689118972_708026','//mei.tmall.com/?acm=lb-zebra-148799-667863.1003.8.708026&scm=1003.8.lb-zebra-148799-667863.ITEM_14561685271493_708026','//list.tmall.com/search_product.htm?cat=50043479&sort=s&style=g&acm=lb-zebra-148799-667863.1003.8.708026&search_condition=7&industryCatId=50026415&active=1&spm=3.7396704.20000007.9.7CvfAH&uuid=76018&from=sn_1_rightnav&abtest=&scm=1003.8.lb-zebra-148799-667863.ITEM_14561685271493_708026&pos=2#J_crumbs','//watch.tmall.com/?acm=lb-zebra-148799-667863.1003.8.708026&scm=1003.8.lb-zebra-148799-667863.ITEM_14561666034064_708026','//dai.tmall.com/?acm=lb-zebra-148799-667863.1003.8.708026&scm=1003.8.lb-zebra-148799-667863.ITEM_14561666034064_708026','//list.tmall.com/search_product.htm?abbucket=&cat=50023064&sort=s&style=g&acm=lb-zebra-148799-667863.1003.8.708026&search_condition=7&aldid=75994&theme=469&active=1&spm=3.7396704.20000007.22.7CvfAH&from=sn_1_rightnav&abtest=&scm=1003.8.lb-zebra-148799-667863.ITEM_14561666034064_708026&pos=3#J_crumbs','//shouji.tmall.com/?acm=lb-zebra-148799-667863.1003.8.708026&scm=1003.8.lb-zebra-148799-667863.ITEM_14561662186585_708026','//3c.tmall.com?acm=lb-zebra-148799-667863.1003.8.708026&scm=1003.8.lb-zebra-148799-667863.ITEM_14561662186585_708026&go=act','//3c.tmall.com/?acm=lb-zebra-148799-667863.1003.8.708026&scm=1003.8.lb-zebra-148799-667863.ITEM_14561662186585_708026&go=digt','//baby.tmall.com/?acm=lb-zebra-148799-667863.1003.8.708026&scm=1003.8.lb-zebra-148799-667863.ITEM_14561673729066_708026','//food.tmall.com/?abbucket=&acm=lb-zebra-148799-667863.1003.8.708026&aldid=75999&spm=3.7396704.20000007.14.7CvfAH&abtest=&scm=1003.8.lb-zebra-148799-667863.ITEM_14561669881597_708026&pos=1','//food.tmall.com/?abbucket=&acm=lb-zebra-148799-667863.1003.8.708026&aldid=75999&spm=3.7396704.20000007.15.7CvfAH&abtest=&scm=1003.8.lb-zebra-148799-667863.ITEM_14561669881597_708026&pos=2#J_MuiLiftPannel1','//food.tmall.com/?abbucket=&acm=lb-zebra-148799-667863.1003.8.708026&aldid=75999&spm=3.7396704.20000007.16.7CvfAH&abtest=&scm=1003.8.lb-zebra-148799-667863.ITEM_14561669881597_708026&pos=3#J_MuiLiftPannel4','//miao.tmall.com?acm=lb-zebra-148799-667863.1003.8.708026&scm=1003.8.lb-zebra-148799-667863.OTHER_14593834779268_708026','//big.tmall.com?acm=lb-zebra-148799-667863.1003.8.708026&scm=1003.8.lb-zebra-148799-667863.ITEM_14561650644158_708026','//3c.tmall.com?acm=lb-zebra-148799-667863.1003.8.708026&scm=1003.8.lb-zebra-148799-667863.ITEM_14561650644158_708026&go=kich','//jia.tmall.com/?acm=lb-zebra-148799-667863.1003.8.708026&scm=1003.8.lb-zebra-148799-667863.ITEM_14561646796679_708026','//car.tmall.com/?acm=lb-zebra-148799-667863.1003.8.708026&scm=1003.8.lb-zebra-148799-667863.ITEM_145616583391510_708026','//list.tmall.com/search_product.htm?abbucket=&cat=56772006&acm=lb-zebra-148799-667863.1003.8.708026&style=g&aldid=431510&search_condition=55&industryCatId=50660004&active=1&spm=875.7789098.20150017.3.pPRs0I&from=sn_1_rightnav&uuid=75987&abtest=&scm=1003.8.lb-zebra-148799-667863.ITEM_145616583391510_708026&pos=11#J_crumbs','//list.tmall.com/search_product.htm?abbucket=&cat=56838011&acm=lb-zebra-148799-667863.1003.8.708026&style=g&aldid=431510&search_condition=55&industryCatId=50660004&active=1&spm=875.7789098.20150017.3.P1jZNx&from=sn_1_rightnav&uuid=75987&abtest=&scm=1003.8.lb-zebra-148799-667863.ITEM_145616583391510_708026&pos=11#J_crumbs','//myhome.tmall.com/?acm=lb-zebra-148799-667863.1003.8.708026&scm=1003.8.lb-zebra-148799-667863.ITEM_145616544916711_708026','//myhome.tmall.com/?abbucket=&acm=lb-zebra-148799-667863.1003.8.708026&aldid=74660&spm=3.7396704.20000007.27.7CvfAH&act=4,2&abtest=&scm=1003.8.lb-zebra-148799-667863.ITEM_145616544916711_708026&pos=2','//hua.tmall.com/?acm=lb-zebra-148799-667863.1003.8.708026&scm=1003.8.lb-zebra-148799-667863.ITEM_145616544916711_708026','//yao.tmall.com/?acm=lb-zebra-148799-667863.1003.8.708026&scm=1003.8.lb-zebra-148799-667863.ITEM_145616352542412_708026','//list.tmall.com/search_product.htm?cat=50036640&sort=s&acm=lb-zebra-148799-667863.1003.8.708026&style=g&search_condition=23&industryCatId=50036640&active=1&spm=a220m.1000858.0.0.v7yFGa&from=sn_1_rightnav&smAreaId=330100&scm=1003.8.lb-zebra-148799-667863.ITEM_145616314067613_708026&tmhkmain=0#J_crumbs','//list.tmall.com/search_product.htm?cat=50071786&abbucket=&sort=s&style=g&acm=lb-zebra-148799-667863.1003.8.708026&search_condition=7&aldid=75975&industryCatId=50071816&active=1&spm=3.7396704.20000007.31.7CvfAH&from=sn_1_rightnav&abtest=&scm=1003.8.lb-zebra-148799-667863.ITEM_145616314067613_708026&pos=2#J_crumbs','//list.tmall.com/search_product.htm?abbucket=&cat=50034368&sort=s&acm=lb-zebra-148799-667863.1003.8.708026&aldid=75975&spm=3.7396704.20000007.32.7CvfAH&from=sn_1_rightnav&pos=3&style=g&search_condition=7&industryCatId=50043495&active=1&uuid=92196&abtest=&scm=1003.8.lb-zebra-148799-667863.ITEM_145616314067613_708026#J_crumbs','//book.tmall.com/?spm=875.7931836.category2016025.1.ZxCttc&acm=lb-zebra-148799-667863.1003.8.708026&scm=1003.8.lb-zebra-148799-667863.ITEM_145616429492414_708026']
    normal_url_pattern=[r'.*list\.tmall\.com/.*']
    normal_url_extractor=LxmlLinkExtractor(allow=normal_url_pattern)
    needed_url_pattern=[r'.*//list\.tmall\.com.*sort=d']
    needed_url_extractor=LxmlLinkExtractor(allow=needed_url_pattern)

    """
    types= {('手机', '家用电器', '数码', '电脑', '办公', '电报、办公', '大家电', '电报办公'): 'TR_SM',
         ('母婴', '母婴玩具'): 'TR_MY',
         ('食品', '酒类', '生鲜', '特产', '营养保健', '食品饮料','零食','进口食品','茶酒'): 'TR_SP',
         ('玩具乐器', '运动户外'): 'TR_WT',
         ('服饰', '鞋靴', '箱包', '珠宝', '奢侈品', '男装',
          '女装', '童装', '内衣', '珠宝首饰', '礼品箱包', '服饰内衣'
          '女鞋','男鞋','腕表','珠宝饰品','眼睛'): 'TR_FS',
         ('个护化妆', '清洁用品','化妆品','个人护理'): 'TR_HZP',
         ('汽车', '汽车用品', '宠物', '宠物生活'): 'TR_ZH',
         ('家居', '家具', '厨具', '家居家装', '家装',
          '家装建材','家纺','家饰','鲜花'): 'TR_JJ'
         }
    """

    def start_requests(self):
        for url in self.start_urls:
            url='https:'+url
            yield SplashRequest(url,callback=self.parse,args={
                'wait':0.5,'html':1,})

    def parse(self,response):
        for link in self.normal_url_extractor.extract_links(response):
            yield SplashRequest(link.url,callback=self.parse_url,args={'wait':0.5,'html':1,})

    def parse_url(self,response):
        for link in self.needed_url_extractor.extract_links(response):
            if 'industryCatId' and 'cat' in link.url and 'post_fee' and 'brand' not in link.url:
                url=re.sub(r'sort=.*&','sort=d&',link.url)
                #url=re.sub(r'search_condition=.*&','search_condition=7',url)
                url=re.sub(r'miaosha=.*&','miaosha=0&',url)
                url=re.sub(r'wwonline=.*&','wwonline=0&',url)
                yield SplashRequest(url,callback=self.parse_item,args={'wait':0.5,'html':1,})

    def parse_item(self,response):
        hxs=Selector(response)
        search_condition=extract_one(hxs,'//*[@id="J_CrumbSearchInuput"]/@value')
        item_titles=extract(hxs,"//div[@id='J_ItemList']//p[@class='productTitle']/a/text()")
        top_id=extract_one(hxs,'//*[@id="J_CrumbSlideCon"]/li[2]/a/text()')
        type_id1=extract_one(hxs,'//*[@id="J_CrumbSlideCon"]//div[@class="crumbDrop j_CrumbDrop"]/a/text()')
        if type_id1 is not None and search_condition is not None:
            type_id1=type_id1.split('/n')[0]
            titles=[]
            title=''
            for t in item_titles:
                if not t.endswith('\n'):
                    title+=t.strip()
                elif t.endswith('\n'):
                    title+=t.strip()
                    if len(title)>5:
                        titles.append(title.strip())
                    title=''

            if len(titles)>19 and search_condition!=type_id1:
                for i,t in enumerate(titles):
                    if i<20:
                        good={
                            'mall': '1',
                            'rank': str(i+1),
                            'title': t.strip(),
                            'price': '0',
                            'turnover_index':'0',
                            'top_id': top_id.strip(),
                            'type_id1': type_id1.strip(),
                            'type_id2': search_condition.strip(),
                            'url': response.url
                        }

                        yield Good(good)

        for link in self.needed_url_extractor.extract_links(response):
            if 'industryCatId' and 'cat' in link.url and 'post_fee' and 'brand' not in link.url:
                url = re.sub(r'sort=.*&', 'sort=d&', link.url)
                url = re.sub(r'search_condition=.*&', 'search_condition=7', url)
                url=re.sub(r'miaosha=.*&','miaosha=0&',url)
                url=re.sub(r'wwonline=.*&','wwonline=0&',url)
                yield SplashRequest(url, callback=self.parse_item, args={'wait': 0.5, 'html': 1,})




