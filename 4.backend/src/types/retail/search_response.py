from src.types.retail.search_product import SearchProduct

class SearchResponse:
    """SearchResponse type for service consumption standardization."""

    def __init__(self, results, num_pages, query, was_autocorrected=False):
        for product in results:
            if not isinstance(product, SearchProduct):
                raise TypeError("results must be a list of SearchProduct's")
        self.results = results
        self.num_pages = num_pages
        self.query = query
        self.was_autocorrected = was_autocorrected

    @property
    def json(self):
        res = {
            'numPages': self.num_pages,
            'results': [product.json for product in self.results]
        }
        
        if self.was_autocorrected:
            res['correctedQuery'] = self.query
        
        return res
