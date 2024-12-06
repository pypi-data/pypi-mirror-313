import os
import sqlalchemy as sa

from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey, VARCHAR, func, Boolean, FLOAT,\
    UniqueConstraint, BigInteger
from sqlalchemy.orm import Session, DeclarativeBase

engine = sa.create_engine(f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}")
conn = engine.connect()
session = Session(engine)


class Base(DeclarativeBase):
    pass



class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    created_at = Column(TIMESTAMP, nullable=False, default=sa.sql.func.now())
    updated_at = Column(TIMESTAMP, nullable=False, default=func.now(), onupdate=sa.sql.func.current_timestamp())

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)


class CoinInTx(BaseModel):
    __tablename__ = 'coin_in_tx'
    address = Column(VARCHAR(192), nullable=False)
    wallet = Column(ForeignKey('wallet.id', ondelete='CASCADE'), nullable=False, index=True)
    description = Column(VARCHAR(194), nullable=True)
    name = Column(VARCHAR(512), nullable=True)
    symbol = Column(VARCHAR(256), nullable=True)
    UniqueConstraint("address", "wallet", name="adr_wid")


class SecondWallet(BaseModel):
    __tablename__ = 'second_wallet'
    address = Column(VARCHAR(192), nullable=False)
    primary_wallet = Column(ForeignKey('wallet.id', ondelete='CASCADE'), nullable=False, index=True)
    status = Column(Boolean, default=True, index=True)
    description = Column(VARCHAR(194), nullable=True)
    UniqueConstraint("address", "primary_wallet", name="adr_pwid")


class Wallet(BaseModel):
    __tablename__ = 'wallet'
    address = Column(VARCHAR(192), nullable=False)
    status = Column(Boolean, default=True, index=True)
    description = Column(VARCHAR(192), nullable=True)
    group_id = Column(ForeignKey('wallet_group.id', ondelete='CASCADE'), nullable=False, index=True)
    UniqueConstraint("address", "group_id", name="adr_tgid")


class WallepGroup(BaseModel):
    __tablename__ = 'wallet_group'
    name = Column(VARCHAR(128), nullable=True)
    telegram_id = Column(VARCHAR(128), nullable=False, index=True)
    UniqueConstraint("name", "telegram_id", name="grname_tgid")

class Transaction(BaseModel):
    __tablename__ = 'wallet_transaction'
    wallet_address = Column(VARCHAR(192), nullable=False, index=True)
    method_id = Column(VARCHAR(192), nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False, index=True)
    value = Column(FLOAT, nullable=True)
    hash = Column(VARCHAR(256), nullable=True, unique=True)
    block_number = Column(Integer, nullable=False)
    block_hash = Column(VARCHAR(254), nullable=True)
    contract_address = Column(VARCHAR(196), nullable=True)
    to_adr = Column(VARCHAR(196), nullable=True)
    from_adr = Column(VARCHAR(198), nullable=True, index=True)
    gas = Column(FLOAT, nullable=True)
    gasPrice = Column(FLOAT, nullable=True)
    gasUsed = Column(FLOAT, nullable=True)
    сumulativeGasUsed = Column(FLOAT, nullable=True)
    functionName = Column(VARCHAR(258), nullable=True)


class CoinNet(BaseModel):
    __tablename__ = 'coin_net'

    net_symbol = Column(VARCHAR(92), nullable=False)
    chain_id = Column(Integer)
    currency = Column(VARCHAR(48), nullable=True)
    UniqueConstraint("net_symbol", "chain_id", name="net_chain")


class CoinPair(BaseModel):
    __tablename__ = 'coin_pair'

    pair_id = Column(Integer, nullable=False, unique=True)
    chain_id = Column(Integer)
    exchange_id = Column(Integer)
    address = Column(VARCHAR(196), nullable=True)
    token0_address = Column(VARCHAR(192), nullable=True)
    token1_address = Column(VARCHAR(193), nullable=True)
    token0_symbol = Column(VARCHAR(60), nullable=True)
    token1_symbol = Column(VARCHAR(61), nullable=True)
    dex_type = Column(VARCHAR(30), nullable=True)
    base_token_symbol = Column(VARCHAR(62), nullable=True)
    quote_token_symbol = Column(VARCHAR(63), nullable=True)
    token0_decimals = Column(Integer, nullable=True)
    token1_decimals = Column(Integer, nullable=True)
    exchange_slug = Column(VARCHAR(59), nullable=True)
    exchange_address = Column(VARCHAR(192), nullable=True)
    pair_slug = Column(VARCHAR(32), nullable=True)
    first_swap_at_block_number = Column(VARCHAR(33), nullable=True)
    last_swap_at_block_number = Column(VARCHAR(34), nullable=True)
    first_swap_at = Column(VARCHAR(34), nullable=True)
    last_swap_at = Column(VARCHAR(35), nullable=True)
    flag_inactive = Column(VARCHAR(36), nullable=True)
    flag_blacklisted_manually = Column(VARCHAR(37), nullable=True)
    flag_unsupported_quote_token = Column(VARCHAR(38), nullable=True)
    flag_unknown_exchange = Column(VARCHAR(39), nullable=True)
    fee = Column(Integer, nullable=True)
    buy_count_all_time = Column(BigInteger, nullable=True)
    sell_count_all_time = Column(BigInteger, nullable=True)
    buy_volume_all_time = Column(BigInteger, nullable=True)
    sell_volume_all_time = Column(BigInteger, nullable=True)
    buy_count_30d = Column(FLOAT, nullable=True)
    sell_count_30d = Column(FLOAT, nullable=True)
    buy_volume_30d = Column(FLOAT, nullable=True)
    sell_volume_30d = Column(FLOAT, nullable=True)
    buy_tax = Column(VARCHAR(40), nullable=True)
    transfer_tax = Column(VARCHAR(41), nullable=True)
    sell_tax = Column(VARCHAR(42), nullable=True)
    update_candles_1h = Column(Boolean, nullable=True, default=False)
    update_liquidity_1h = Column(Boolean, nullable=True, default=False)


class Candle(BaseModel):
    __tablename__ = 'candle'

    hash = Column(ForeignKey('coin_article.hash', ondelete='CASCADE'), index=True, nullable=False)
    received_symbol = Column(VARCHAR(60), nullable=False, index=True)
    sell_symbol = Column(VARCHAR(60), nullable=False, index=True)
    avg = Column(VARCHAR(36), nullable=True)
    buy_volume = Column(FLOAT, nullable=True)
    buys = Column(FLOAT, nullable=True)
    close = Column(FLOAT, nullable=True)
    end_block = Column(BigInteger, nullable=True)
    exchange_rate = Column(FLOAT, nullable=True)
    high = Column(FLOAT, nullable=True)
    low = Column(FLOAT, nullable=True)
    open = Column(FLOAT, nullable=True)
    pair_id = Column(BigInteger, nullable=True)
    sell_volume = Column(FLOAT, nullable=True)
    sells = Column(FLOAT, nullable=True)
    start_block = Column(BigInteger, nullable=True)
    timestamp = Column(TIMESTAMP, nullable=False, index=True)
    volume = Column(FLOAT, nullable=True)
    exchange = Column(VARCHAR(64), nullable=True)
    UniqueConstraint("hash", "timestamp", "received_symbol", name="coin_date")


class HourCandle(BaseModel):
    __tablename__ = 'hour_candle'

    hash = Column(ForeignKey('coin_article.hash', ondelete='CASCADE'), index=True, nullable=False)
    received_symbol = Column(VARCHAR(60), nullable=False, index=True)
    sell_symbol = Column(VARCHAR(60), nullable=False, index=True)
    avg = Column(VARCHAR(36), nullable=True)
    buy_volume = Column(FLOAT, nullable=True)
    buys = Column(FLOAT, nullable=True)
    close = Column(FLOAT, nullable=True)
    end_block = Column(BigInteger, nullable=True)
    exchange_rate = Column(FLOAT, nullable=True)
    high = Column(FLOAT, nullable=True)
    low = Column(FLOAT, nullable=True)
    open = Column(FLOAT, nullable=True)
    pair_id = Column(BigInteger, nullable=True)
    sell_volume = Column(FLOAT, nullable=True)
    sells = Column(FLOAT, nullable=True)
    start_block = Column(BigInteger, nullable=True)
    timestamp = Column(TIMESTAMP, nullable=False, index=True)
    volume = Column(FLOAT, nullable=True)
    exchange = Column(VARCHAR(64), nullable=True)
    UniqueConstraint("hash", "timestamp", "received_symbol", name="coin_date")



class CoinArticle(BaseModel):
    __tablename__ = 'coin_info'

    description = Column(VARCHAR(36), nullable=True)
    common_url = Column(VARCHAR(255), nullable=False)
    detail_url = Column(VARCHAR(255), nullable=True)
    hash = Column(ForeignKey('coin_article.hash', ondelete='CASCADE'), nullable=False, index=True)
    name = Column(VARCHAR(64), nullable=True)
    symbol = Column(VARCHAR(60), nullable=True)
    chain_raw = Column(VARCHAR(92), nullable=True)
    chain = Column(VARCHAR(90), nullable=True)
    website = Column(VARCHAR(256), nullable=True)
    whitepaper = Column(VARCHAR(512), nullable=True)
    telegram = Column(VARCHAR(256), nullable=True)
    twitter = Column(VARCHAR(256), nullable=True)
    explorer = Column(VARCHAR(256), nullable=True)
    explorer_title = Column(VARCHAR(256), nullable=True)
    address = Column(VARCHAR(192), nullable=True)
    deposit_datetime_raw = Column(VARCHAR(94))
    trading_datetime_raw = Column(VARCHAR(96))
    withdrawal_datetime_raw = Column(VARCHAR(98))
    deposit_datetime = Column(TIMESTAMP, nullable=True)
    trading_datetime = Column(TIMESTAMP, nullable=True)
    withdrawal_datetime = Column(TIMESTAMP, nullable=True)
    has_history = Column(Boolean, default=False)


class LiquidityDayCandle(BaseModel):
    __tablename__ = 'liquidity_day'
    timestamp = Column(TIMESTAMP, nullable=False, index=True)
    pair_id = Column(ForeignKey('coin_pair.pair_id', ondelete='CASCADE'), index=True, nullable=False)
    exchange_rate = Column(FLOAT, nullable=True)
    open = Column(FLOAT, nullable=True)
    close = Column(FLOAT, nullable=True)
    high = Column(FLOAT, nullable=True)
    low = Column(FLOAT, nullable=True)
    adds = Column(FLOAT, nullable=True)
    removes = Column(FLOAT, nullable=True)
    syncs = Column(FLOAT, nullable=True)
    add_volume = Column(FLOAT, nullable=True)
    remove_volume = Column(FLOAT, nullable=True)
    start_block = Column(BigInteger, nullable=True)
    end_block = Column(BigInteger, nullable=True)
    liquidity_type = Column(VARCHAR(64), nullable=True)
    UniqueConstraint("pair_id", "timestamp", name="pair_date")


class CoinPased(BaseModel):
    __tablename__ = 'coin_article'

    hash = Column(VARCHAR(48), nullable=False, unique=True, index=True)
    is_parsed = Column(Boolean, nullable=False, default=False)
