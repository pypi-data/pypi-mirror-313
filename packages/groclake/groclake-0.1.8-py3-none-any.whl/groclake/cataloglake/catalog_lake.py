
from ..groc_default.groc_base import Groc


class GrocCatalog(Groc):

    def __init__(self, cataloglake_id=''):
        super().__init__()
        self.cataloglake_id = cataloglake_id

    def get_payload_from_product_object(self, product_object):
        if type(self) is not CatalogLakeCreate and self.cataloglake_id:
            product_object.update({'cataloglake_id': self.cataloglake_id})
        return product_object


class CatalogLakeFetch(GrocCatalog):
    api_endpoint = '/catalog/fetch'

    def fetch(self, product_object):
        return self.call_api(product_object)


class CatalogLakePush(GrocCatalog):
    api_endpoint = '/catalog/push'

    def push(self, product_object):
        return self.call_api(product_object)


class CatalogLakeGen(GrocCatalog):
    api_endpoint = '/catalog/gen'

    def gen(self, product_object):
        return self.call_api(product_object)


class CatalogLakeRecommender(GrocCatalog):
    api_endpoint = '/catalog/recommender/fetch'

    def recommend(self, payload):
        return self.call_api(payload)


class CatalogLakeSearch(GrocCatalog):
    api_endpoint = '/catalog/search/fetch'

    def search(self, payload):
        return self.call_api(payload)


class CatalogLakeUpdate(GrocCatalog):
    api_endpoint = '/catalog/update'

    def update(self, product_object):
        return self.call_api(product_object)


class CatalogLakeInventoryUpdate(GrocCatalog):
    api_endpoint = '/catalog/inventoryUpdate'

    def update(self, inventory_object):
        return self.call_api(inventory_object)


class CatalogLakeInventoryFetch(GrocCatalog):
    api_endpoint = '/catalog/inventoryFetch'

    def fetch(self, inventory_object):
        return self.call_api(inventory_object)


class CatalogLakePriceUpdate(GrocCatalog):
    api_endpoint = '/catalog/priceUpdate'

    def update(self, price_object):
        return self.call_api(price_object)


class CatalogLakePriceFetch(GrocCatalog):
    api_endpoint = '/catalog/priceFetch'

    def fetch(self, price_object):
        return self.call_api(price_object)


class CatalogLakeImageCache(GrocCatalog):
    api_endpoint = '/catalog/imageCache'

    def cache_image(self, image_object):
        return self.call_api(image_object)


class CatalogLakeCreate(GrocCatalog):
    api_endpoint = '/catalog/create'

    def create(self):
        return self.call_api({})


class CatalogLakeCache(GrocCatalog):
    api_endpoint = '/catalog/cache'

    def cache(self, payload):
        return self.call_api(payload)


class CatalogLakeSend(GrocCatalog):
    api_endpoint = '/catalog/send'

    def send(self, payload):
        return self.call_api(payload)


class CatalogLakeDelete(GrocCatalog):
    api_endpoint = '/catalog/delete'

    def delete(self, payload):
        return self.call_api(payload)


class CatalogLakeSearchIntentFetch(GrocCatalog):
    api_endpoint = '/search/intent/fetch'

    def search_intent_fetch(self, payload):
        return self.call_api(payload)


class CatalogLakeAddressIntentFetch(GrocCatalog):
    api_endpoint = '/address/intent/fetch'

    def address_intent_fetch(self, payload):
        return self.call_api(payload)


class CatalogLake:
    def __init__(self, cataloglake_id=''):
        self.cataloglake_id = cataloglake_id
        self._fetcher = None
        self._pusher = None
        self._generator = None
        self._recommender = None
        self._searcher = None
        self._updater = None
        self._inventory_updater = None
        self._inventory_fetcher = None
        self._price_updater = None
        self._price_fetcher = None
        self._image_cache = None
        self._cache = None
        self._send = None
        self._delete = None
        self._creator = None
        self._search_intent_fetcher = None
        self._address_intent_fetcher = None

    def _get_fetcher(self):
        if self._fetcher is None:
            self._fetcher = CatalogLakeFetch(self.cataloglake_id)
        return self._fetcher

    def _get_pusher(self):
        if self._pusher is None:
            self._pusher = CatalogLakePush(self.cataloglake_id)
        return self._pusher

    def _get_generator(self):
        if self._generator is None:
            self._generator = CatalogLakeGen(self.cataloglake_id)
        return self._generator

    def _get_recommender(self):
        if self._recommender is None:
            self._recommender = CatalogLakeRecommender(self.cataloglake_id)
        return self._recommender

    def _get_searcher(self):
        if self._searcher is None:
            self._searcher = CatalogLakeSearch(self.cataloglake_id)
        return self._searcher

    def _get_updater(self):
        if self._updater is None:
            self._updater = CatalogLakeUpdate(self.cataloglake_id)
        return self._updater

    def _get_inventory_updater(self):
        if self._inventory_updater is None:
            self._inventory_updater = CatalogLakeInventoryUpdate(self.cataloglake_id)
        return self._inventory_updater

    def _get_inventory_fetcher(self):
        if self._inventory_fetcher is None:
            self._inventory_fetcher = CatalogLakeInventoryFetch(self.cataloglake_id)
        return self._inventory_fetcher

    def _get_price_updater(self):
        if self._price_updater is None:
            self._price_updater = CatalogLakePriceUpdate(self.cataloglake_id)
        return self._price_updater

    def _get_price_fetcher(self):
        if self._price_fetcher is None:
            self._price_fetcher = CatalogLakePriceFetch(self.cataloglake_id)
        return self._price_fetcher

    def _get_creator(self):
        if self._creator is None:
            self._creator = CatalogLakeCreate()
        return self._creator

    def _get_image_cache(self):
        if self._image_cache is None:
            self._image_cache = CatalogLakeImageCache(self.cataloglake_id)
        return self._image_cache

    def _get_cache(self):
        if self._cache is None:
            self._cache = CatalogLakeCache(self.cataloglake_id)
        return self._cache

    def _get_send(self):
        if self._send is None:
            self._send = CatalogLakeSend(self.cataloglake_id)
        return self._send

    def _get_delete(self):
        if self._delete is None:
            self._delete = CatalogLakeDelete(self.cataloglake_id)
        return self._delete

    def _get_search_intent_fetcher(self):
        if self._search_intent_fetcher is None:
            self._search_intent_fetcher = CatalogLakeSearchIntentFetch(self.cataloglake_id)
        return self._search_intent_fetcher

    def _get_address_intent_fetcher(self):
        if self._address_intent_fetcher is None:
            self._address_intent_fetcher = CatalogLakeAddressIntentFetch(self.cataloglake_id)
        return self._address_intent_fetcher

    def create(self):
        create_response = self._get_creator().create()
        if create_response.get('cataloglake_id'):
            self.cataloglake_id = create_response.get('cataloglake_id')
        return create_response

    def fetch(self, product_object):
        return self._get_fetcher().fetch(product_object)

    def push(self, product_object):
        return self._get_pusher().push(product_object)

    def gen(self, product_object):
        return self._get_generator().gen(product_object)

    def recommend(self, payload):
        return self._get_recommender().recommend(payload)

    def search(self, payload):
        return self._get_searcher().search(payload)

    def update(self, product_object):
        return self._get_updater().update(product_object)

    def update_inventory(self, inventory_object):
        return self._get_inventory_updater().update(inventory_object)

    def fetch_inventory(self, inventory_object):
        return self._get_inventory_fetcher().fetch(inventory_object)

    def update_price(self, price_object):
        return self._get_price_updater().update(price_object)

    def fetch_price(self, price_object):
        return self._get_price_fetcher().fetch(price_object)

    def cache_image(self, image_object):
        return self._get_image_cache().cache_image(image_object)

    def cache(self, payload):
        return self._get_cache().cache(payload)

    def send(self, payload):
        return self._get_send().send(payload)

    def delete(self, payload):
        return self._get_delete().delete(payload)

    def search_intent_fetch(self, payload):
        return self._get_search_intent_fetcher().search_intent_fetch(payload)

    def address_intent_fetch(self, payload):
        return self._get_address_intent_fetcher().address_intent_fetch(payload)
