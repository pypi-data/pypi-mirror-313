from django.test import TestCase
from postcodes.postcode import (
    address_check, Address
)


# Get a free API key from postcode.go-dev.nl
POSTCODE_API_KEY = "YOUR_API_KEY"


class PostcodeAPITestCase(TestCase):
    def setUp(self):
        self.postcode = "7315 AA"
        self.home_number = "23"

    def test_postcode_api(self):
        addr: Address = address_check(
            postcode=self.postcode,
            number=self.home_number,
            api_key=POSTCODE_API_KEY,
        )

        street = "Koninklijk Park"
        city = "Apeldoorn"
        municipality = "Apeldoorn"
        province = "Gelderland"
        build_year = 1968

        self.assertEqual(addr.street.lower(), street.lower())
        self.assertEqual(addr.city.lower(), city.lower())
        self.assertEqual(addr.municipality.lower(), municipality.lower())
        self.assertEqual(addr.province.lower(), province.lower())
        self.assertEqual(addr.build_year, build_year)

        
