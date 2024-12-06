"""
https://postcode.tech/

Deze Postcode API is gratis, maar dat betekent niet dat de API gebruikt kan worden om een kopie van alle data te maken. 
Daarom is er een limiet van 10k requests per dag, per gebruiker. Heb je meer requests nodig per dag, neem dan even contact met ons op.

Deze service is beschikbaar as-is, dat betekent dat het gebruik op eigen risico is. 
De service wordt met zorg beschikbaar gesteld en onderhouden, maar dit is geen garantie voor juistheid van data, beschikbaarheid en snelheid.

Om ervoor te zorgen dat iedereen zoveel mogelijk gebruik kan maken van deze dienst kunnen er limieten aan gebruikers worden gesteld in het kader van fair use.

Doe geen voor het publiek herleidbare verzoeken aan deze service, maar verwerk het in eigen software en tracht zoveel mogelijk caching toe te passen op reeds gedane verzoeken. 
Dit om de belasting van de service te beperken.

Het is niet de bedoeling de data of deze services door te verkopen of in commerciële wederverkoop aan te bieden. 
Dit houdt o.a. in dat het niet is toestaan een eigen service aan te bieden die deze data als bron gebruikt.
"""
import requests
from django.utils.translation import gettext_lazy as _
from django.core.cache import cache

import logging

from postcodes.settings import (
    ADDRESS_CHECK_API_KEY,
    ADDRESS_CHECK_API_URL,
    URL_PARAMETER_FORMAT,
    ADDRESS_CACHE_TIMEOUT,
    API_KEY_ATTRIBUTE,
    ERROR_ATTRIBUTE,
)

_default_headers = {
    "Accept": "application/json",
    API_KEY_ATTRIBUTE: ADDRESS_CHECK_API_KEY,
}


logger = logging.getLogger(__name__)


class Address:
    """
        A simple address object to store address information.
    """
    postcode: str = None
    home_number: int = None

    def __init__(self, postcode, home_number, data):
        self.postcode = postcode
        self.home_number = home_number
        self.data = data or {}

    def dict(self):
        return {
            "postcode": self.postcode,
            "home_number": self.home_number,
            "data": self.data,
        }
    
    def __getattr__(self, name):
        if name in ["postcode", "home_number", "data", "dict"]:
            return super().__getattribute__(name)
        
        if name in self:
            return self[name]
        
        raise AttributeError(f"Attribute {name} not found in address data.")
    
    def __getitem__(self, name):
        try:
            return getattr(self, name)
        except AttributeError:
            return None


class AddressValidationError(Exception):
    def __init__(self, message, *args, **kwargs):
        self.message = message
        if not args:
            args = (message, )
        super().__init__(*args, **kwargs)


def make_cache_key(postcode, number):
    return f"address_check_{postcode}_{number}"


def address_check(postcode: str, number: int, api_key = None) -> Address:
    """
        Validate if a postal code and house number are valid.
        This only works for dutch addressess.
    """

    if not ADDRESS_CHECK_API_KEY and not api_key:
        raise ImportError("No API key found. Please set ADDR_VALIDATOR_API_KEY in your settings file.")
    
    # Do some simple cleaning of the input.
    postcode = postcode.replace(" ", "").upper()
    number = number.replace(" ", "").upper()

    if not postcode or not number:
        raise AddressValidationError(_("Please provide a postcode and house number."))

    # Check if the address is already cached.
    cache_key = make_cache_key(postcode, number)
    address = cache.get(cache_key, default=None)
    if address:
        return Address(**address)

    headers = _default_headers.copy()
    if api_key:
        headers[API_KEY_ATTRIBUTE] = api_key

    # Generate a new address validation request.
    parameters = URL_PARAMETER_FORMAT(
        postcode=postcode, 
        huisnummer=number,
    )
    
    url = f"{ADDRESS_CHECK_API_URL}?{parameters}"
    response = requests.get(url, headers=headers)
    try:
        data = response.json()
    except:
        raise AddressValidationError(_(f"Endpoint returned an invalid response: {response.text}"))
    
    if response.status_code != 200:
        raise AddressValidationError(
            _("Invalid Response status %(status)s / %(url)s") % {"status": response.status_code, "url": url},
            getattr(data, ERROR_ATTRIBUTE, _("Endpoint returned an error response."))
        )

    # Create a new address instance
    address = Address(
        postcode=postcode,
        home_number=number,
        data=data,
    )

    # Cache the address for a week.
    cache.set(cache_key, address.dict(), timeout=ADDRESS_CACHE_TIMEOUT)

    return address    
