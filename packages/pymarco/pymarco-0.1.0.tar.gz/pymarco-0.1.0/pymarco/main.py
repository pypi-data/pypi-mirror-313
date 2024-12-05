from .models import *
from .data import countries
from .data import currencies

def get_country(alpha2:str=None)->Country:
    if alpha2:
        country = [c for c in countries if c["alpha2"] == alpha2][0]
        return Country(**country)
    return

def get_currency(code:str=None)->Currency:
    if code:
        currency = [c for c in currencies if c["code"] == code]
        if currency:
            return Currency(**currency[0])
    return

def get_all_countries():
    all_countries = [c["name"] for c in countries]
    return all_countries
