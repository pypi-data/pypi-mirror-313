import bisect
import functools
import json
import pathlib
import re
import typing

# Some countries have were colonies at some point but now use their own
# country code. Several still use the colonizer's postal code system.
# This is a mapping of the dependency's country code to the colonizer's
# country code.
dependents_map = {
    # France, uses postcodes 97XXX and 98XXX.
    "gf": "fr",  # French Guiana
    "gp": "fr",  # Guadeloupe
    "mq": "fr",  # Martinique
    "nc": "fr",  # New Caledonia
    "pf": "fr",  # French Polynesia
    "re": "fr",  # Réunion

    # United Kingdom
    "ai": "gb",  # Anguilla, uses postcode AI-2640 (not in the lookup table)
    "io": "gb",  # British Indian Ocean Territory
    "je": "gb",  # Jersey, uses postcode JE1 1AA - JE5 999
    "ky": "gb",  # Cayman Islands, uses postcodes KYx-xxxx
    "ms": "gb",  # Montserrat, uses postcodes MSR1xxx
    "pn": "gb",  # Pitcairn Islands, uses postcodes PCRN 1ZZ
    "vg": "gb",  # British Virgin Islands, uses postcodes VG11xx
    "ta": "gb",  # Tristan da Cunha, uses TDCU 1ZZ

    # United States
    "as": "us",  # American Samoa, 96799
    "gu": "us",  # Guam, 96910–96932
    "mp": "us",  # Northern Mariana Islands, 96950-96952
    "pr": "us",  # Puerto Rico, 006xx-009xx
    "vi": "us",  # U.S. Virgin Islands, 008xx

    # Netherlands
    "bq": "nl",  # Bonaire, Sint Eustatius and Saba (has no actual postcodes)
    "cw": "nl",  # Curaçao, uses 0000xx
    "sx": "nl",  # Sint Maarten, uses 17xx xx

    # China
    "hk": "cn",  # Hong Kong, uses 999077
    "mo": "cn",  # Macau, uses 999078

    # Norway
    "sj": "no",  # Svalbard and Jan Mayen, uses 917x

    # New Zealand
    "ck": "nz",  # Cook Islands (no postcode system)
    "nu": "nz",  # Niue, uses 9974
    "tk": "nz",  # Tokelau, (no postcode system)

    # Australia
    "cc": "au",  # Cocos (Keeling) Islands, uses WA 6799
    "cx": "au",  # Christmas Island, uses WA 6798
    "nf": "au",  # Norfolk Island, uses 2899

    # Spain
    "ea": "es",  # Ceuta and Melilla, uses 5100x

    # Sweden
    "ax": "fi",  # Åland Islands, uses AX22000–AX22999
}


def cache_fn(fn):
    sentinel = object()
    cache = sentinel

    @functools.wraps(fn)
    def wrapper():
        nonlocal cache
        if cache is sentinel:
            cache = fn()
        return cache

    return wrapper


@cache_fn
def _country_regexes():
    with open('postcode_regex.json') as f:
        postcode_spec = json.load(f)
    return {
        spec['abbrev'].lower(): re.compile(f'^{spec["postal"].lower()}$')
        for spec in postcode_spec
        if "postal" in spec  # Exclude countries without postal code
    }


def normalize_postcode(country_code: str, postcode: str, *, validate=False):
    if validate and len(country_code) != 2 or not country_code.isalpha():
        return None

    country_code = country_code.lower()
    postcode = postcode.lower()

    # Remove the leading country code if it's ther
    # Special case for the UK, which has postcodes that start with two letters.
    if postcode.startswith(country_code) and (country_code != 'gb'
                                              or len(postcode) > 8):
        postcode = postcode[2:]

    # Remove any leading/trailing whitespace or punctuation
    postcode = postcode.strip('-/ \t\n\r_')

    if validate:
        re_postcode = _country_regexes().get(country_code)
        if re_postcode is not None:
            # print(re_postcode)
            match = re_postcode.match(postcode) or re_postcode.match(postcode.replace(' ', '').replace('-', ''))
            if match:
                postcode = match.group(0).lower()
            else:
                return None

    return "".join(filter(str.isalnum, postcode))


@cache_fn
def _postcodes_lookup():
    db_path = pathlib.Path(__file__).parent / 'postcode_to_timezone_lookup.csv'

    with db_path.open() as f:
        return [tuple(line.strip().split(',')) for line in f]


def get_tz(country_code: str,
           postcode: str,
           fallback: typing.Optional[str] = "UTC") -> typing.Optional[str]:
    country_code = country_code.lower()
    postcode = normalize_postcode(country_code, postcode)

    lut = _postcodes_lookup()
    # Add ascii character 255 to the end of the postcode to ensure that the
    # lookup never returns an exact match. This places the insertion point
    # after the last postcode, so we need to shift it by 1 to get the exact
    # match.
    i = bisect.bisect(lut, (country_code, postcode + '\xff'))
    if i != 0 and i != len(lut) and lut[i - 1][0] == country_code:
        return lut[i - 1][2]

    if country_code in dependents_map:
        # Retry with the (former?) parent country code
        return get_tz(dependents_map[country_code], postcode)

    return fallback
