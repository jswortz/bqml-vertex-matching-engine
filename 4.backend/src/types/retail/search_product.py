from datetime import datetime, timedelta
import math

class SearchProduct:
    """SearchProduct type for standardization between different data models."""

    __ELASTIC_FIELD_MAP = {
        'AVAILABILITY': 'availability',
        'BRAND': 'brand',
        'CATEGORY': 'category',
        'COLOR': 'color',
        'ESTIMATED_DELIVERY_DAY': 'days_to_deliver',
        'ID': 'product_id',
        'image_link': 'image_url',
        'NAME': 'name',
        'RETAIL_PRICE': 'price',
        #'review' field not joined with 'products' table in
        # elasticsearch because 'review' table is empty
        #'REVIEW': 'review',
        'SIZE': 'size',
        'SUB_CATEGORY': 'sub_category'
    }

    def __init__(self, product_id=None, name=None, availability=None, brand=None, 
    category=None, sub_category=None, color=None, days_to_deliver=None,
    image_url=None, price=None, review=None, size=None):
        self.availability = availability
        self.brand = brand
        self.category = category
        self.sub_category = sub_category
        self.color = color
        self.days_to_deliver = days_to_deliver
        self.product_id = product_id
        self.image_url = image_url
        self.name = name
        self.price = price
        self.review = review
        self.size = size

    @classmethod
    def from_retail(cls):
        raise NotImplementedError

    @classmethod
    def from_elastic(cls, elastic_dict):
        params = {}
        for field, arg_name in cls.__ELASTIC_FIELD_MAP.items():
            params[arg_name] = elastic_dict[field]
        return cls(**params)

    @property
    def json(self):
        res = {
            'AVAILABILITY': self.availability,
            'CATEGORY': self.category,
            'COLOR': self.color,
            'COMPANY': self.brand,
            'ID': self.product_id,
            'IMAGE LINK': self.image_url,
            'NAME': self.name,
            'PRICE': self.price,
            'REVIEW': self.review,
            'SIZE': self.size,
            'SUB_CATEGORY': self.sub_category
        }

        dt = datetime.utcnow() + timedelta(days=self.days_to_deliver)
        dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
        res['ESTIMATE_DELIVERY_AT'] = math.floor(dt.timestamp() * 1000)

        return res
