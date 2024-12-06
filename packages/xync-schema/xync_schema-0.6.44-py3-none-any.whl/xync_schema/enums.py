from enum import IntEnum


class AdStatus(IntEnum):
    defActive = 0
    active = 1
    two = 2
    old = 3
    four = 4
    notFound = 9


class OrderStatus(IntEnum):
    requested = 1
    request_canceled = 2
    created = 3
    rejected = 4
    paid = 5
    canceled = 6
    completed = 7
    appealed_by_seller = 9
    appealed_by_buyer = 10
    seller_appeal_disputed_by_buyer = 11
    buyer_appeal_disputed_by_seller = 12
    appeal_canceled = 15
    # todo: 8T - один вирт экшн на бездействие обеих сторон, а 12T и 13T - по отдельности?
    # paid_and_canceled = 7
    # COMPLETED, PENDING, TRADING, BUYER_PAYED, DISTRIBUTING, COMPLETED, IN_APPEAL, CANCELLED, CANCELLED_BY_SYSTEM


class ExType(IntEnum):
    p2p = 1
    cex = 2
    main = 3  # p2p+cex
    dex = 4
    futures = 8


class DepType(IntEnum):
    earn = 1
    stake = 2
    beth = 3
    lend = 4


class AssetType(IntEnum):
    spot = 1
    earn = 2
    found = 3


class TradeType(IntEnum):
    BUY = 0
    SELL = 1


class PmType(IntEnum):
    bank = 0
    web_wallet = 1
    cash = 2
    gift_card = 3
    credit_card = 4
    IFSC = 5


class TaskType(IntEnum):
    invite_approve = 1


class ExAction(IntEnum):
    """Order"""

    order_request = 1  # [T] Запрос на старт сделки
    order_request_ask = -1  # [M] - Запрос мейкеру на сделку
    cancel_request = 2  # [T] Отмена запроса на сделку
    request_canceled = -2  # [M] - Уведомление об отмене запроса на сделку
    accept_request = 3  # [M] Одобрить запрос на сделку
    request_accepted = -3  # [T] Уведомление об одобрении запроса на сделку
    reject_request = 4  # [M] Отклонить запрос на сделку
    request_rejected = -4  # [T] Уведомление об отклонении запроса на сделку
    mark_payed = 5  # [B] Перевод сделки в состояние "оплачено", c отправкой чека
    payed = -5  # [S] Уведомиление продавца об оплате
    cancel_order = 6  # [B] Отмена сделки
    order_canceled = -6  # [S] Уведомиление продавцу об отмене оредера покупателем
    confirm = 7  # [S] Подтвердить получение оплаты
    order_completed = -7  # [B] Уведомиление покупателю об успешном завершении продавцом
    appeal_available = -8  # [S,B] Уведомление о наступлении возможности подать аппеляцию
    start_appeal = 9  # ,10 # [S,B] Подать аппеляцию cо скриншотом/видео/файлом
    appeal_started = -9  # ,-10 # [S,B] Уведомление о поданной на меня аппеляци
    dispute_appeal = 11  # ,12 # [S,B] Встречное оспаривание полученной аппеляции cо скриншотом/видео/файлом
    appeal_disputed = -11  # ,-12 # [S,B] Уведомление о встречном оспаривание поданной аппеляции
    order_completed_by_appeal = -13  # [S,B] Уведомление о завершении сделки по аппеляции
    order_canceled_by_appeal = -14  # [B,S] Уведомление об отмене сделки по аппеляции
    cancel_appeal = 15  # [B,S] Отмена аппеляции
    appeal_canceled = -15  # [B,S] Уведомление об отмене аппеляции против меня
    send_order_msg = 16  # Отправка сообщения юзеру в чат по ордеру с приложенным файлом
    get_order_msg = -16  # Получение сообщения в чате по ордеру
    send_appeal_msg = 17  # Отправка сообщения по апелляции
    get_appeal_msg = -17  # Получение сообщения по апелляции
    """ Ex: Public """
    pms = 20  # Список платежных методов по каждой валюте
    curs = 21  # Список поддерживаемых валют тейкера
    cur_pms_map = 22  # Мэппинг валюта => платежные методы
    coins = 23  # Список торгуемых монет (с ограничениям по валютам, если есть)
    ads = 24  # Список объяв по (buy/sell, cur, coin, pm)
    """ Agent: Fiat """
    my_fiats = 25  # Список реквизитов моих платежных методов
    fiat_new = 26  # Создание
    fiat_upd = 27  # Редактирование
    fiat_del = 28  # Удаление
    """ Agent: Ad """
    my_ads = 29  # Список моих ad
    ad_new = 30  # Создание ad:
    ad_upd = 31  # Редактирование
    ad_del = 32  # Удаление
    ad_switch = 33  # Вкл/выкл объявления
    ads_switch = 34  # Вкл/выкл всех объявлений
    """ Agent: Taker """
    get_user = 35  # Получить объект юзера по его ид
    send_user_msg = 36  # Отправка сообщения юзеру с приложенным файлом
    block_user = 37  # [Раз]Блокировать юзера
    rate_user = 38  # Поставить отзыв юзеру
    """ Agent: Inbound """
    get_user_msg = -36  # Получение сообщения от юзера
    got_blocked = -37  # Получение уведомления о [раз]блокировке юзером
    got_rated = -38  # Получение уведомления о полученном отзыве


exs = {
    "Beribit": (
        ExType.p2p,
        "https://sun9-41.userapi.com/impg/cZCGFTXH5-11_HjiWw9aWr3__SlbmMIiXSc-ig/YtOHJpjuVW0.jpg?size=604x604&quality=95&sign=def93bbe4283c563eb2d75a5968350f2",
        "beribit.app",
        "beribit.app",
        "beribit.app/login",
    ),
    "Binance": (
        ExType.main,
        "https://assets.coingecko.com/markets/images/52/large/binance.jpg",
        "binance.com",
        "p2p.binance.com",
        "accounts.binance.com/login",
    ),
    "BingX": (
        ExType.p2p,
        "https://assets.coingecko.com/markets/images/812/large/YtFwQwJr_400x400.jpg",
        "bingx.com",
        "bingx.com",
        "bingx.com/login",
    ),
    "Bisq": (ExType.p2p, "", "", "", ""),
    "BitcoinGlobal": (ExType.p2p, "", "", "", ""),
    "BitGet": (
        ExType.p2p,
        "https://assets.coingecko.com/markets/images/591/large/2023-07-25_21.47.43.jpg",
        "www.bitget.com",
        "www.bitget.com",
        "www.bitget.com/login",
    ),
    "BitPapa": (
        ExType.p2p,
        "https://avatars.mds.yandex.net/i?id=130c32d9900d514d738ef89b9c61bcd3_l-4767909-images-thumbs&n=13",
        "bitpapa.com",
        "bitpapa.com",
        "bitpapa.com/log-in",
    ),
    "Bitvalve ": (ExType.p2p, "", "", "", ""),
    "Bybit": (
        ExType.main,
        "https://assets.coingecko.com/markets/images/698/large/bybit_spot.png",
        "bybit.com",
        "bybit.com",
        "bybit.com/login",
    ),
    "CoinCola": (ExType.main, "", "", "", ""),
    "CRYPTED": (ExType.p2p, "", "", "", ""),
    "Garantex": (ExType.p2p, "", "", "", ""),
    "Gate": (
        ExType.p2p,
        "https://assets.coingecko.com/markets/images/403/large/gate_io_logo.jpg",
        "gate.io",
        "gate.io",
        "www.gate.io/login",
    ),
    "HodlHodl": (ExType.p2p, "", "", "", ""),
    "Htx": (
        ExType.main,
        "https://assets.coingecko.com/markets/images/25/large/logo_V_colour_black.png",
        "www.htx.com",
        "www.htx.com",
        "htx.com/login",
    ),
    "Koshelek": (ExType.p2p, "", "", "", ""),
    "KuCoin": (
        ExType.main,
        "https://assets.coingecko.com/markets/images/61/large/kucoin.png",
        "kucoin.com",
        "kucoin.com",
        "www.kucoin.com/ucenter/signin",
    ),
    "LocalCoinSwap": (ExType.p2p, "", "", "", ""),
    "LocalMonero": (ExType.p2p, "", "", "", ""),
    "Mexc": (
        ExType.main,
        "https://assets.coingecko.com/markets/images/409/large/MEXC_logo_square.jpeg",
        "www.mexc.com",
        "www.mexc.com",
        "www.mexc.com/login",
    ),
    "Noones ": (ExType.p2p, "", "", "", ""),
    "Okx": (
        ExType.main,
        "https://assets.coingecko.com/markets/images/379/large/WeChat_Image_20220117220452.png",
        "www.okx.cab",
        "www.okx.cab",
        "www.okx.cab/account/login",
    ),
    "Paxful": (ExType.p2p, "", "", "", ""),
    "PeachBitcoin": (ExType.p2p, "", "", "", ""),
    "Phemex": (ExType.p2p, "", "", "", ""),
    "Poloniex": (ExType.main, "", "", "", ""),
    "Remitano": (ExType.p2p, "", "", "", ""),
    "RiseX": (ExType.p2p, "", "", "", ""),
    "RoboSats": (ExType.p2p, "", "", "", ""),
    "Sigen": (
        ExType.p2p,
        "https://yastatic.net/naydex/yandex-search/neZ1W6346/a21f02dA/2SvJ6dTLJwRiz_lTFP-fhywHqi1fxPNRcIxuKzcpwJ0DGlJzbzdT8ARet86SrINoGNj87R9U-t8HLZcrrBASQf0_6OkAL7cgl6uc0gCrHxI9Y369emE2MJF5yotCyODdZ5iXljtkQJMXTMV9VXsEL68seaiqQF578wnB3V",
        "sigen.pro",
        "sigen.pro",
        "sigen.pro/p2p",
    ),
    "SkyCrypto": (ExType.p2p, "", "", "", ""),
    "SmartSwap": (ExType.p2p, "", "", "", ""),
    "Solid": (ExType.main, "", "", "", ""),
    "TgWallet": (
        ExType.p2p,
        "https://telerock.ru/uploads/posts/2024-03/f658443d9e_c9d505bbf856e2360ba6812079ba02d0.webp",
        "walletbot.me",
        "p2p.walletbot.me",
        "walletbot.me",
    ),
    "TotalCoin": (ExType.p2p, "", "", "", ""),
    "WazirX": (ExType.p2p, "", "", "", ""),
    "WebMoney": (
        ExType.p2p,
        "https://vectorseek.com/wp-content/uploads/2023/08/Webmoney-Icon-Logo-Vector.svg-.png",
        "exchanger.money",
        "exchanger.money",
        "exchanger.money",
    ),
    "WhiteBIT": (ExType.p2p, "", "", "", ""),
    "xRocket": (
        ExType.p2p,
        "https://cdn.allmylinks.com/prod/Upload/file/R/L/6/8G0TaGNtUV8C1V7VQsivDtJcpEz2z7Lc.jpg",
        "",
        "",
        "",
    ),
    # "catalogop2p(.com": ExType.p2p, ''), todo: discover brazilian p2p platforms
}
