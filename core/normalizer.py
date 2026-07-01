import re


COUNTRY_CODES = {

    "EG": "20",

    "SA": "966",

    "AE": "971",

    "KW": "965",

    "QA": "974",

    "BH": "973",

    "OM": "968",

    "IQ": "964",

    "JO": "962",

    "SY": "963",

    "LB": "961"

}


def digits(number):

    return re.sub(r"\D", "", str(number))


def normalize(number, country="EG"):

    number = digits(number)

    if not number:

        return None

    if number.startswith("00"):

        number = number[2:]

    code = COUNTRY_CODES.get(country, "20")

    if number.startswith(code):

        return number

    if number.startswith("0"):

        return code + number[1:]

    return number
