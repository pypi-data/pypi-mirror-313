import time
from collections import defaultdict
from time import sleep
from datetime import datetime
from typing import List

from requests import HTTPError

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from .exceptions import InitialisationException, InvalidStatusException
from .logger import logger
from .config import settings
from .mapping import Mapping
from .marketplace import Marketplace
from .schemas import WbAccount, WbItem, WbUpdate
from .utils import is_too_small_price, is_too_high_price
from .validators import (
    validate_id_and_value,
    validate_statuses,
    validate_date_string,
)


class Wildberries(Marketplace):
    def __init__(
        self,
        account_data: WbAccount,
        mapping_url,
        mapping_token,
        max_price_requests: int = 5,
        session: requests.Session = requests.Session(),
    ):
        self._logger = logger
        self._session = session
        self._mapping_service = Mapping(mapping_url, mapping_token)
        self._max_price_requests = max_price_requests
        retries = Retry(
            total=3,
            backoff_factor=0.5,
        )
        self._session.mount("https://", HTTPAdapter(max_retries=retries))

        self.warehouse_id = account_data.warehouse_id
        self._session.headers.update(
            {
                "Authorization": f"{account_data.common_token}",
            }
        )

        if not hasattr(self, "warehouse_id"):
            self._logger.error("Warehouse id is not found")
            raise InitialisationException("Warehouse id is not found")

        self._logger.debug("Wildberries is initialized")

    def __request(self, url, method, params=None, json=None, retries=3, **kwargs):

        if not retries:
            self._logger.error("Failed to send data to the market after 3 attempts.")
            raise HTTPError

        response = self._session.request(method=method, url=url, params=params, json=json, **kwargs)

        try:
            response.raise_for_status()
            return response
        except HTTPError as exc:
            if response.status_code == 400:
                text = response.json()
                if text.get('errorText') == "No goods for process":
                    self._logger.warning(
                        f"Wildberries: The price and discount that we are"
                        f" trying to put coincides with the current one on the market"
                    )
                else:
                    self._logger.error("Products are not updated. Get 400 code from WB. Check sending products")
                    self._logger.warning(response.json())
                    raise exc
            elif response.status_code == 429:
                self._logger.warning("Too many requests to market. Get 429 code. Wait a few minutes and try again.")
                sleep(120)
                self.__request(url=url, method=method, params=params, json=json, retries=retries - 1, **kwargs)

    def get_stock(self, ms_id: str):
        try:
            assert isinstance(ms_id, str)
            ms_items = self._mapping_service.get_mapped_data([ms_id], [0])[0]
            stocks = self._session.post(
                f"{settings.wb_api_url}api/v3/stocks/{self.warehouse_id}",
                json={
                    "skus": [ms_items.barcodes],
                },
                timeout=5,
            )
            stocks.raise_for_status()
            return stocks.json()
        except HTTPError as e:
            self._logger.error(
                f"Wildberries: {ms_id} stock is not refreshed. Error: {e}"
            )
            raise e

    def get_stocks(
        self, date: str = datetime.now().strftime("%Y-%m-%d")
    ):
        """
        Get stocks updated for a specific date or datetime.
        To obtain the full stocks' quantity, the earliest possible value should be specified.

        Args:
            date (str, optional): The date or datetime string in "YYYY-MM-DD" or "YYYY-MM-DDTHH:MM:SS" format.
                Defaults to the current date in "YYYY-MM-DD" format.

        Raises:
            ValueError: If the input string is not in either date or datetime format.
            HTTPError: If the method is called more than once in a minute.
        """
        try:
            validate_date_string(date)
            url = f"{settings.wb_statistic_url}api/v1/supplier/stocks?dateFrom={date}"

            stocks_response = self._session.get(url)
            stocks_response.raise_for_status()
            stocks_data = {}
            if stocks_response.json():
                for stock in stocks_response.json():
                    stocks_data[str(stock["nmId"])] = {
                        "barcode": stock["barcode"],
                        "quantity": stock["quantity"],
                    }
            return stocks_data
        except HTTPError as e:
            self._logger.error(f"Wildberries: too many responses. Error: {e}")
            raise e
        except Exception as e:
            self._logger.error(f"Wildberries: error while getting stocks. Error: {e}")
            raise e

    @validate_id_and_value
    def refresh_stock(self, ms_id: str, value: int):
        try:
            ms_items = self._mapping_service.get_mapped_data([ms_id], [value])[0]
            refresh_stock_resp = self._session.put(
                f"{settings.wb_api_url}api/v3/stocks/{self.warehouse_id}",
                json={
                    "stocks": [
                        {
                            "sku": ms_items.barcodes,
                            "amount": value,
                        },
                    ]
                },
                timeout=5,
            )
            refresh_stock_resp.raise_for_status()
            self._logger.info(f"Wildberries: {ms_id} stock is refreshed")
            return True
        except HTTPError as e:
            self._logger.error(
                f"Wildberries: {ms_id} stock is not refreshed. Error: {e}"
            )
            raise e

    def refresh_stocks(self, products_data: list[WbUpdate]) -> None:
        for _range in range(0, len(products_data), settings.WB_ITEMS_REFRESH_LIMIT):

            body = {
                "stocks": [
                    {
                        "sku": product.wb_barcodes,
                        "amount": product.stock
                    }
                    for product in products_data[_range: _range + settings.WB_ITEMS_REFRESH_LIMIT]
                ]
            }

            refresh_stocks_resp = self._session.put(
                f"{settings.wb_api_url}api/v3/stocks/{self.warehouse_id}",
                json=body,
                timeout=5,
            )
            try:
                refresh_stocks_resp.raise_for_status()
                self._logger.info('Sent data to WB')
                self._logger.info(body)
            except HTTPError as e:
                response = refresh_stocks_resp.json()[0]
                if refresh_stocks_resp.status_code == 409 and response['code'] == 'CargoWarehouseRestriction':
                    failed_nm_id = [data['sku'] for data in response['data']]
                    self._logger.error(f'Bad products: {failed_nm_id}')

                    new_body = self.remove_bad_product(failed_nm_id, body['stocks'])
                    new_update_response = self._session.put(
                        f"{settings.wb_api_url}api/v3/stocks/{self.warehouse_id}",
                        json=new_body,
                        timeout=5,
                    )
                    try:
                        new_update_response.raise_for_status()
                        continue
                    except HTTPError as e:
                        self._logger.error(f"Wildberries: stocks is not refreshed. Error: {e}")
                        self._logger.error(new_update_response.json())
                        continue

                self._logger.error(f"Wildberries: stocks is not refreshed. Error: {e}")
                self._logger.error(refresh_stocks_resp.json())

    @staticmethod
    def remove_bad_product(bad_sku, product_for_update):
        new_body = {'stocks': []}
        for product in product_for_update:
            if product['sku'] not in bad_sku:
                new_body['stocks'].append(product)
        return new_body

    def get_prices_from_market(self) -> dict:
        products = dict()
        default_offset = 0

        while True:
            url = f"{settings.wb_price_url}api/v2/list/goods/filter"
            params = {
                "limit": settings.WB_ITEMS_REFRESH_LIMIT,
                "offset": default_offset,
            }

            try:
                resp = self.__request(url=url, method='GET', params=params)
            except HTTPError:
                break

            if resp:

                list_goods = resp.json().get('data').get('listGoods')

                if not list_goods:
                    break

                for product in list_goods:
                    price = product['sizes'][0]['price']
                    discount = product["discount"]

                    products.update({((str(product["nmID"]), )): (price, discount)})

                default_offset += + settings.WB_ITEMS_REFRESH_LIMIT

        return products

    def get_all_products(self) -> list[str]:
        products = list()
        default_offset = 0

        while True:
            url = f"{settings.wb_price_url}api/v2/list/goods/filter"
            params = {
                "limit": settings.WB_ITEMS_REFRESH_LIMIT,
                "offset": default_offset
            }

            try:
                resp = self.__request(url=url, method='GET', params=params)
            except HTTPError as exc:
                self._logger.error(f"Get error from WB request: {exc}")
                break

            list_goods = resp.json().get('data').get('listGoods')

            if not list_goods:
                break

            products.extend([str(product.get('nmID')) for product in list_goods])

            default_offset += settings.WB_ITEMS_REFRESH_LIMIT

        return products

    @validate_id_and_value
    def refresh_price(self, product_data: WbItem):
        try:

            if is_too_small_price(price_from_ms=product_data.final_price, price_from_market=product_data.market_price):
                self._logger.warning(f"Price decreased by 30% or more for ms_id: {product_data.ms_id}.")
                return {
                    product_data.ms_id: {
                        "price_from_ms": product_data.price,
                        "price_from_market": product_data.market_price
                    }
                }

            self._update_prices([product_data])
        except HTTPError as e:
            self._logger.error(
                f"Wildberries: {product_data.ms_id} price is not refreshed. Error: {e}"
            )
            raise e

    def refresh_prices(self, products_data: List[WbItem]):

        suspicious_products = {1: defaultdict(), 2: defaultdict(), 3: defaultdict()}

        valid_products = []
        for product in products_data:
            if is_too_small_price(price_from_ms=product.final_price, price_from_market=product.market_price):
                suspicious_products[2][product.ms_id] = {
                    "price_1": product.final_price,
                    "price_2": product.market_price,
                    "code": f'{product.code} / nm_id: {product.nm_id}'
                }
                continue
            elif is_too_high_price(
                price_from_ms=product.final_price,
                price_from_market=product.market_price
            ):
                suspicious_products[3][product.ms_id] = {
                    "price_1": product.final_price,
                    "price_2": product.market_price,
                    "code": f'{product.code} / nm_id: {product.nm_id}'
                }
                continue
            if product.min_price > product.final_price:
                suspicious_products[1][product.ms_id] = {
                    "price_1": product.min_price,
                    "price_2": product.final_price,
                    "code": f'{product.code} / nm_id: {product.nm_id}'
                }
                continue
            if product.market_discount != settings.WB_DISCOUNT:
                product.market_discount = settings.WB_DISCOUNT

            valid_products.append(product)

        self._update_prices(valid_products)

        return suspicious_products

    def _update_prices(self, items: List[WbItem]):
        for i in range(0, len(items), settings.WB_ITEMS_REFRESH_LIMIT):
            prepare_data = {
                int(item.nm_id): {
                    "price": int(item.origin_price),
                    "discount": int(item.market_discount)}
                for item in items[i: i + settings.WB_ITEMS_REFRESH_LIMIT]
                }

            url = f"{settings.wb_price_url}api/v2/upload/task"
            data = {"data": [
                {"nmID": key, "price": value.get("price"), "discount": value.get("discount")}
                for key, value in prepare_data.items()
            ]}

            resp = self.__request(url=url, method='POST', json=data)
            time.sleep(3)

            if resp:
                self._logger.info(f"response: {resp.status_code} {resp.json()}")

    def refresh_status(self, wb_order_id: int, status_name: str, supply_id: str = None):
        assert isinstance(wb_order_id, int)
        assert isinstance(status_name, str)
        try:
            match status_name:
                case "confirm":
                    supply_id = supply_id or self._session.post(
                        f"{settings.wb_api_url}api/v3/supplies",
                        json={"name": f"supply_order{wb_order_id}"},
                        timeout=5,
                    ).json().get("id")
                    add_order_to_supply_resp = requests.patch(
                        f"{settings.wb_api_url}api/v3/supplies/{supply_id}/orders/{wb_order_id}",
                    )
                    add_order_to_supply_resp.raise_for_status()
                case "cancel":
                    cancel_order_resp = requests.patch(
                        f"{settings.wb_api_url}api/v3/orders/{wb_order_id}/cancel"
                    )
                    cancel_order_resp.raise_for_status()
                case _:
                    raise InvalidStatusException(
                        f"{status_name} is not valid status name"
                    )
            return True
        except HTTPError as e:
            self._logger.error(
                f"Wildberries: {wb_order_id} status is not refreshed. Error: {e}"
            )
            raise e

    @validate_statuses
    def refresh_statuses(self, wb_order_ids: List[int], statuses: List[str]):
        try:
            new_supply = self._session.post(
                f"{settings.wb_api_url}api/v3/supplies",
                json={"name": "supply_orders"},
                timeout=5,
            ).json()

            for wb_order_id, status in zip(wb_order_ids, statuses):
                self.refresh_status(
                    wb_order_id=wb_order_id,
                    status_name=status,
                    supply_id=new_supply.get("id"),
                )
            return True
        except HTTPError as e:
            self._logger.error(f"Wildberries: can't create new supply. Error: {e}")
            raise e

    def get_commissions(self) -> List[dict]:
        url = f"{settings.wb_commission_url}api/v1/tariffs/commission"
        subjects = self._session.get(url).json()
        return [
            {
                "subject_id": subject['subjectID'],
                "subject_name": subject['subjectName'],
                "commission": subject['paidStorageKgvp'],
            }
            for subject in subjects['report']
        ]
