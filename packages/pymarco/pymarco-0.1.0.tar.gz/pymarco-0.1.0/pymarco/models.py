from dataclasses import dataclass

@dataclass
class Country:
    alpha2: str
    alpha3: str
    numeric: str
    tld: str
    car_sign: str
    flag: str
    name: str
    native_name: str
    capital: str
    continent: str
    continent_code: str
    currency: str
    currency_code: str
    latlong: list
    calling_code: str
    timezone: str
    timezone_id: list
    demonym: str
    landlocked: bool
    languages: str

@dataclass
class Currency:
    name: str
    native_name: str
    code: str
    symbol: str
    subdivision: str
    subdivision_native: str
    factor: int

@dataclass
class language:
    name: str
    native_name: str
    code_2: str
    code_3: str
    rtl: bool
    alphabet: str
    locales: list[str]
