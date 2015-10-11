from scrapy.item import Item, Field

        class JabongItem(Item):
		    # define the fields for your item here like:
		    name = Field()
		    link = Field()
		    sku = Field()
		    brand = Field()
		    img = Field()

