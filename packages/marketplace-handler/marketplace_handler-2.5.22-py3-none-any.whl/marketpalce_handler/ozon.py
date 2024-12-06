from collections import defaultdict
from typing import List

import requests
from requests import Session, HTTPError
from requests.adapters import HTTPAdapter, Retry

from .schemas import OzonItem, OzonAccount, OzonUpdate
from .exceptions import InitialisationException
from .mapping import Mapping
from .marketplace import Marketplace
from .logger import logger
from .config import settings
from .utils import get_chunks, is_too_small_price, is_too_high_price
from .validators import validate_id_and_value, validate_ids_and_values


class Ozon(Marketplace):
    def __init__(
        self,
        account_data: OzonAccount,
        mapping_url: str,
        mapping_token: str,
        session: Session = requests.Session(),
    ):
        self._name = account_data.name
        self.warehouse_id = account_data.warehouse_id
        self._mapping_service = Mapping(mapping_url, mapping_token)
        self._logger = logger
        self._session = session
        self._ozon_item_schema = OzonItem
        retries = Retry(
            total=3,
            backoff_factor=0.5,
        )
        self._session.mount("https://", HTTPAdapter(max_retries=retries))

        self._session.headers.update(
            {
                "Client-Id": account_data.client_id,
                "Api-Key": account_data.api_key,
            }
        )

        if not hasattr(self, "warehouse_id"):
            self._logger.error(f"Warehouse ID not found for account name: {self._name}")
            raise InitialisationException(f"Warehouse ID not found for account name: {self._name}")

        self._logger.info("Ozon marketplace is initialised")

    def __request(self, url, method, params=None, json=None, **kwargs):

        response = self._session.request(method=method, url=url, params=params, json=json, **kwargs)

        try:
            response.raise_for_status()
            self._logger.info('Sent data to OZON')
            self._logger.info(json)
        except HTTPError as exc:
            if response.status_code == 400:
                self._logger.error("Products are not updated. Get 400 code from Ozon. Check sending products")
                self._logger.warning(response.json())
                raise exc

        return response.json()

    def get_prices_from_market(self) -> dict:
        products_from_market = {}
        last_id = ''

        while True:

            url = f"{settings.ozon_api_url}v4/product/info/prices"
            json = {
                "filter": {"visibility": "ALL"},
                "limit": "1000",
                "last_id": last_id
            }

            resp = self.__request(url=url, method='POST', json=json)

            if resp.get('code'):
                break

            products_from_market.update(
                {
                    ((item['offer_id'], )): float(item['price']['price']) for item in resp['result']['items']
                }
            )

            last_id = resp.get('result').get('last_id')

            if not last_id:
                break

        return products_from_market

    def refresh_prices(self, products_data: List[OzonItem]):
        suspicious_products = {1: defaultdict(), 2: defaultdict(), 3: defaultdict()}
        valid_products = []

        for product in products_data:

            if product.min_price > product.ozon_after_discount:
                suspicious_products[1][product.ms_id] = {
                    "price_1": product.min_price,
                    "price_2": product.ozon_after_discount,
                    "code": product.code
                }
                continue
            elif is_too_small_price(
                    price_from_ms=product.ozon_after_discount,
                    price_from_market=product.market_price
                    ):
                suspicious_products[2][product.ms_id] = {
                    "price_1": product.ozon_after_discount,
                    "price_2": product.market_price,
                    "code": product.code
                }
                continue
            elif is_too_high_price(
                price_from_ms=product.ozon_after_discount,
                price_from_market=product.market_price
            ):
                suspicious_products[3][product.ms_id] = {
                    "price_1": product.ozon_after_discount,
                    "price_2": product.market_price,
                    "code": product.code
                }
                continue

            valid_products.append(product)

        for i in range(0, len(valid_products), settings.OZONE_PRICE_LIMIT):

            url = f"{settings.ozon_api_url}v1/product/import/prices"
            json = {"prices": [
                {"offer_id": item.code,
                 "price": str(item.ozon_after_discount),
                 "min_price": str(item.ozon_after_discount),
                 "old_price": str(item.old_price)
                 }
                for item in valid_products[i: i + settings.OZONE_PRICE_LIMIT]
            ]}

            self.__request(url=url, method='POST', json=json)
            self._logger.info("Many updates stocks for ozon is completed.")

        return suspicious_products

    @validate_id_and_value
    def refresh_price(self, ms_id: str, value: int):
        mapped_data = self._mapping_service.get_product_data([ms_id], self._ozon_item_schema)
        offer_id = mapped_data[0].offer_id
        resp = self._session.post(
            f"{settings.ozon_api_url}v1/product/import/prices",
            json={"prices": [{"offer_id": offer_id, "price": str(value)}]},
        )
        return resp.json()

    @validate_id_and_value
    def refresh_stock(self, ms_id: str, value: int):
        mapped_data = self._mapping_service.get_product_data([ms_id], self._ozon_item_schema)
        offer_id = mapped_data[0].offer_id
        resp = self._session.post(
            f"{settings.ozon_api_url}v1/product/import/stocks",
            json={"stocks": [{"offer_id": offer_id, "stock": value}]},
        )
        return resp.json()

    def refresh_stocks(self, products_data: list[OzonUpdate]):

        for _range in range(0, len(products_data), settings.OZON_STOCK_LIMIT):

            body = {
                "stocks": [
                    {"offer_id": product.code, "stock": product.stock, "warehouse_id": self.warehouse_id}
                    for product in products_data[_range: _range + settings.OZON_STOCK_LIMIT]
                ]
            }

            response = self.__request(
                url=f'{settings.ozon_api_url}v2/products/stocks',
                method='POST',
                json=body
            )

            logger.info(response)

    @validate_ids_and_values
    def refresh_stocks_by_warehouse(self, ms_ids: List[str], values: List[int]):
        mapped_data = self._mapping_service.get_product_data(ms_ids, self._ozon_item_schema)
        ids_map = {item.ms_id: item.offer_id for item in mapped_data}
        stocks = []
        for ms_id, value, warehouse in zip(ms_ids, values):
            stocks.append(
                {"offer_id": ids_map[ms_id], "stock": value, "warehouse_id": self.warehouse_id}
            )
        return self._session.post(
            f"{settings.ozon_api_url}v2/products/stocks", json={"stocks": stocks}
        ).json()

    def get_all_products(self):
        products_from_market = []
        json = {
            "filter": {"visibility": "ALL"},
            "limit": "1000",
            "last_id": ''
        }

        while True:

            url = f"{settings.ozon_api_url}v2/product/list"

            resp = self.__request(url=url, method='POST', json=json)

            if not resp.get('result').get('items'):
                break

            products_from_market.extend([item['offer_id'] for item in resp['result']['items']])

            json['last_id'] = resp.get('result').get('last_id', '')

            if not json['last_id']:
                break

        return products_from_market


    def refresh_status(self, wb_order_id, status):
        raise NotImplementedError

    def refresh_statuses(self, wb_order_ids, statuses):
        raise NotImplementedError
