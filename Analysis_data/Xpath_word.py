class Xpaths:
    def __init__(self):
        self.get_app_urls = "//div[@class='while_apps']//div[@class='item_holder']/a/@href"
        self.categories = "//div[@class='info']//div[1]//a//text()"
        self.version = "//div[@class='info']//div[4]/text()"
        self.os = "//div[@class='info']//div[5]/text()"
        self.internet = "//div[@class='info']//div[6]/text()"
        self.size = "//div[@class='info']//div[7]/text()"
        self.raiting = "//div[@class='info']//div[8]/text()"
        self.russian = "//div[@class='info']//div[9]/text()"
        self.pkg_name = "//h1[@itemprop='name']//text()"
        self.img_urls = "//img/@src"
        self.description = "//div[@itemprop='description']//text()"
        self.icon = "//meta[@property='og:image']/@content | //div[@class='c in_holder']/img/@data-src"
        self.download_first_url = "//a/@href"
        self.download_second_url = "//a[@id='download_up']/@href"
        self.md5 = "//div[@class='c']//strong/text()"
        self.app_url = "//meta[@property='og:type']/@content"
        self.mod_number1 = "//a[@class='google_play round5']/@href"
        self.mod_number2 = "//meta[@property='og:image']/@content"
        self.pkg_download_url = "//a/@href |//div[@class='c']/a[@class='download round30']/@href"