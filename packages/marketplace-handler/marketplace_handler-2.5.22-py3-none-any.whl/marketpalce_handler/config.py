class Settings:
    # WB
    wb_api_url: str = "https://suppliers-api.wildberries.ru/"
    wb_price_url: str = "https://discounts-prices-api.wb.ru/"
    wb_statistic_url: str = "https://statistics-api.wildberries.ru/"
    wb_commission_url: str = "https://common-api.wildberries.ru/"
    WB_ITEMS_REFRESH_LIMIT: int = 1000
    WB_DISCOUNT = 50

    # OZON
    ozon_api_url: str = "https://api-seller.ozon.ru/"
    OZON_STOCK_LIMIT: int = 100
    OZONE_PRICE_LIMIT: int = 1000

    # YANDEX
    yandex_api_url: str = "https://api.partner.market.yandex.ru"
    YANDEX_STOCK_LIMIT: int = 500

    # OTHER
    MAPPING_LIMIT: int = 100

    # Limiting upper and lower price
    UPPER_LIMIT: float = 1.75
    LOWER_LIMIT: float = 0.15


settings = Settings()
