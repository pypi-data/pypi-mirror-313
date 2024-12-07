from enum import Enum


class AssetType(Enum):
    CASH = "cash"
    STOCK = "stock"
    CRYPTO = "crypto"
    ETF = "etf"
    FUND = "fund"
    PROPERTY = "property"
    COMMODITY = "commodity"
    NFT = "nft"
    STOCK_FUTURES = "stock_futures"
    STOCK_OPTION = "stock_option"
    COMMODITY_FUTURES = "commodity_futures"
    COMMODITY_OPTION = "commodity_option"
    CRYPTO_FUTURES = "crypto_futures"
    CRYPTO_INVERSE_FUTURES = "crypto_inverse_futures"
    CRYPTO_OPTION = "crypto_option"
    CRYPTO_PERP = "crypto_perp"
    CRYPTO_INVERSE_PERP = "crypto_inverse_perp"
