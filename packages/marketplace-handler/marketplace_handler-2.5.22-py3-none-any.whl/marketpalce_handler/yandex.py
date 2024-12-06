from datetime import datetime, timedelta
from collections import defaultdict
from time import sleep

import requests

from urllib3 import Retry
from typing import Optional, Dict, List
from requests import HTTPError
from requests.adapters import HTTPAdapter

from marketplace_handler.config import settings
from marketplace_handler.mapping import Mapping
from marketplace_handler.logger import logger
from marketplace_handler.utils import is_too_small_price, is_too_high_price
from marketplace_handler.schemas import YandexItem, YandexAccount, YandexUpdate
from marketplace_handler.marketplace import Marketplace
from marketplace_handler.exceptions import InitialisationException
from marketplace_handler.validators import validate_id_and_value


class Yandex(Marketplace):
    stock_limit = settings.YANDEX_STOCK_LIMIT

    def __init__(
            self,
            account_data: YandexAccount,
            mapping_url: str,
            mapping_token: str,
            session: requests.Session = requests.Session()
    ):
        self._name = account_data.name
        self._campaign_id = account_data.campaign_id
        self._business_id = account_data.business_id
        self._logger = logger

        self._mapping_service = Mapping(mapping_url, mapping_token)

        self._session = session
        retries = Retry(total=3, backoff_factor=0.5)
        self._session.mount("https://", HTTPAdapter(max_retries=retries))

        self._session.headers.update(
            {
                "Authorization": f"Bearer {account_data.token}"
            }
        )

        if not hasattr(self, "_campaign_id") or not hasattr(self, "_business_id"):
            self._logger.error(f"Campaing or Business id not found for account name: {self._name}")
            raise InitialisationException(f"Campaing or Business id not found for account name: {self._name}")

        self._logger.info(f"Yandex account for {self._name} if initialized.")

    def __request(self, url, method, params=None, json=None, retries=3, **kwargs):

        if not retries:
            self._logger.error("Failed to send data to the market after 3 attempts.")
            return False

        response = self._session.request(method=method, url=url, params=params, json=json, **kwargs)

        try:
            response.raise_for_status()
            self._logger.info('Sent data to YANDEX')
            self._logger.info(json)
        except HTTPError:
            if response.status_code == 400:
                self._logger.error("Products are not updated. Get 400 code from Yandex. Check sending products")
                self._logger.warning(response.json())
            elif response.status_code == 420:
                self._logger.warning("Too many requests to market. Get 420 code. Wait a few minutes and try again.")
                sleep(120)
                return self.__request(url=url, method=method, params=params, json=json, retries=retries - 1, **kwargs)

        return response.json()

    def get_stocks(self, page_token: Optional[str] = None):
        request_params = {
            "url": f"{settings.yandex_api_url}/businesses/{self._business_id}/offer-mappings",
            "method": "POST",
            "params": {"page_token": page_token} if page_token else None
        }

        return self.__request(**request_params)

    def get_prices_from_market(self) -> Dict:
        products_from_market = {}
        page_token = None

        while True:
            products = self.get_stocks(page_token=page_token)
            paging = products.get("result").get("paging")

            page_token = paging.get("nextPageToken") if paging else None

            for product in products.get("result").get("offerMappings"):
                barcode = tuple(product.get("offer").get("barcodes"))
                offer_id = product.get("offer").get("offerId")

                try:
                    products_from_market.update(
                        {
                            barcode: (offer_id, product.get("offer", {}).get("basicPrice", {}).get('value', 1))
                        }
                    )
                except AttributeError:
                    self._logger.warning(f"Product with barcode: {barcode} on Yandex Market doesn't have price!")
                    self._logger.warning(product)

            if not page_token:
                return products_from_market

    @validate_id_and_value
    def refresh_stock(self, ms_id: str, value: int):

        ms_items = self._mapping_service.get_mapped_data([ms_id], [value])[0]

        refresh_stock_resp = self._session.post(
            url=f"{settings.yandex_api_url}/businesses/{self._business_id}/offer-mappings/update",
            json={
                "skus": [
                    {
                        "sku": ms_items.barcodes,
                        "items": [
                            {
                                "count": ms_items.value
                            }
                        ]
                    }
                ]
            },
            timeout=5
        )
        try:
            refresh_stock_resp.raise_for_status()
        except HTTPError as exc:
            self._logger.error(f"Yandex {ms_id} stock is not refreshed. Error: {exc}")
            raise exc
        else:
            self._logger.info(f"Yandex {ms_id} stock if refreshed")
            return True

    @validate_id_and_value
    def refresh_price(self, ms_id: str, price_from_market: int):
        product_data = self._mapping_service.get_product_data([ms_id], YandexItem)[0]
        offer_id = product_data.offer_id

        if is_too_small_price(price_from_ms=product_data.price, price_from_market=price_from_market):
            self._logger.warning(f"Price decreased by 50% or more for ms_id: {ms_id}.")
            return {
                product_data.ms_id: {
                    "price_from_ms": product_data.price,
                    "price_from_market": product_data.market_price
                }
            }

        response = self._session.post(
            url=f"{settings.yandex_api_url}/businesses/{self._business_id}/offer-prices/updates",
            json={
                "offers": [
                    {
                        "offerId": offer_id,
                        "price": {
                            "value": int(product_data.price),
                            "currencyId": "RUR",
                            "discountBase": int(product_data.discount_base)
                        }
                    }
                ]
            },
            timeout=5
        )
        return response.json()

    def refresh_stocks(self, products_data: list[YandexUpdate]):

        for _range in range(0, len(products_data), 10):
            body = {
                    "skus": [
                        {
                            "sku": item.code,
                            "items": [{"count": item.stock}]
                        } for item in products_data[_range: _range + self.stock_limit] if item.yandex_barcodes
                    ]
                }

            response = self.__request(
                url=f'{settings.yandex_api_url}/campaigns/{self._campaign_id}/offers/stocks',
                method='PUT',
                json=body
            )
            logger.info(response)

    def refresh_prices(self, products_data: List[YandexItem]):

        suspicious_products = {1: defaultdict(), 2: defaultdict(), 3: defaultdict()}

        valid_products = []
        count_to_wait = 0

        for product in products_data:

            if product.market_price == 1:
                self._logger.warning(f'Код продукта у которого не было цены на маркете яндекс {product.code} - {product.yandex_barcodes}')
                product.market_price = product.price

            elif is_too_small_price(
                    price_from_ms=product.price,
                    price_from_market=product.market_price
            ):
                suspicious_products[2][product.ms_id] = {
                    "price_1": product.price,
                    "price_2": product.market_price,
                    "code": product.code
                }
                continue
            elif is_too_high_price(
                price_from_ms=product.price,
                price_from_market=product.market_price
            ):
                suspicious_products[3][product.ms_id] = {
                    "price_1": product.price,
                    "price_2": product.market_price,
                    "code": product.code
                }
                continue
            if product.min_price > product.price:
                suspicious_products[1][product.ms_id] = {
                    "price_1": product.min_price,
                    "price_2": product.ozon_after_discount,
                    "code": product.code
                }
                continue

            valid_products.append(product)

            if len(valid_products) == self.stock_limit:

                url = f"{settings.yandex_api_url}/businesses/{self._business_id}/offer-prices/updates"
                json = {
                    "offers": [
                        {
                            "offerId": item.offer_id,
                            "price": {
                                "value": int(item.price),
                                "currencyId": "RUR",
                                "discountBase": int(item.discount_base)
                            }
                        } for item in valid_products
                    ]
                }

                resp = self.__request(url=url, method='POST', json=json)
                if resp:
                    count_to_wait += 1
                    self._logger.info("Many updates stocks for yandex is completed.")

                if count_to_wait == 5:
                    self._logger.info('Sleep 30 sec to avoid ban')
                    sleep(30)
                    count_to_wait = 0

                valid_products.clear()

        return suspicious_products

    def get_all_products(self):
        products_from_market = []
        request_params = {
            "url": f"{settings.yandex_api_url}/campaigns/{self._campaign_id}/offers",
            "method": "POST",
            "params": {"page_token": '', 'limit': 200},
            "json":  {"statuses": ["PUBLISHED"]}
        }

        while True:
            response = self.__request(**request_params)

            if not response['result']['offers']:
                break

            products_from_market.extend([item['offerId'].replace('GGD', 'GGD_')
                                         for item in response['result']['offers']
                                         ])

            request_params['params']['page_token'] = response['result'].get('paging', {}).get('nextPageToken', None)
            if not request_params['params']['page_token']:
                break

        return products_from_market

    def refresh_status(self, ms_id, value):
        raise NotImplementedError

    def refresh_statuses(self, ids: list[int], values: list[str]):
        raise NotImplementedError
