#!/usr/bin/env python3
import time
import logging
import multiprocessing
import pathlib

import pandas as pd
import timezonefinder

import postcode_to_timezone

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def log_time(func):

    def wrapper(*args, **kwargs):
        t0 = time.time()
        result = func(*args, **kwargs)
        logger.info('%s took %.2fs',
                    func.__name__.replace("_", " ").title(),
                    time.time() - t0)
        return result

    return wrapper


@log_time
def load_postcode_database():
    # Load the postcodes and their lon/lat from the CSV file
    result = pd.read_csv(
        './location_postcode.csv.xz',
        converters={
            'postcode': str,
            'country_code': str,
            'geometry': str,
        },
    )
    result.country_code = result.country_code.str.lower()
    return result


@log_time
def parse_geometry(postcodes):
    postcodes = postcodes[postcodes['geometry'].str.startswith('POINT')]
    logger.info('Parsing %d geometries', len(postcodes))

    latlon = postcodes.geometry\
        .str.removeprefix('POINT (')\
        .str.removesuffix(')')\
        .str.split(' ', n=1, expand=True)

    postcodes['lon'] = latlon[0].astype(float)
    postcodes['lat'] = latlon[1].astype(float)
    postcodes = postcodes.drop(columns=['geometry'])

    return postcodes


def normalize_postcode(lon, lat):
    return postcode_to_timezone.normalize_postcode(lon, lat, validate=True)

@log_time
def normalize_postcodes(postcodes):
    logger.info('Normalizing %d postcodes', len(postcodes))
    with multiprocessing.Pool() as pool:
        postcodes.loc[:, 'postcode'] = pool.starmap(
            normalize_postcode,
            postcodes[['country_code', 'postcode']].itertuples(index=False,
                                                               name=None),
        )

    postcodes = postcodes.dropna(subset=['postcode'])

    return postcodes


_finder = None


def lookup(lng, lat):
    global _finder
    if not _finder:
        _finder = timezonefinder.TimezoneFinder()
    return _finder.timezone_at(lng=lng, lat=lat)


@log_time
def lookup_timezones(postcodes):

    logger.info('Looking up timezones for %d postcodes', len(postcodes))
    with multiprocessing.Pool() as pool:
        timezones = pool.starmap(
            lookup,
            postcodes[['lon', 'lat']].itertuples(index=False, name=None),
        )

    postcodes['timezone'] = timezones

    return postcodes


@log_time
def build_lookup_table(postcodes):
    postcodes = postcodes.sort_values(by=['country_code', 'postcode'])
    postcodes['prev_country_code'] = postcodes.country_code.shift(1)
    postcodes['prev_timezone'] = postcodes.timezone.shift(1)

    # Remove postcodes that have the same country code and timezone as the
    # previous entry. A binary search will find the lower bound.
    result = postcodes[(postcodes.country_code != postcodes.prev_country_code)
                       | (postcodes.timezone != postcodes.prev_timezone)]
    result = result.drop(columns=['prev_country_code', 'prev_timezone'])

    # Find single-timezone countries, and remove the postcode
    # This will make the lookup table smaller on disk.
    simple_countries = result.groupby('country_code').timezone.nunique() == 1
    simple_countries = simple_countries[simple_countries].index

    result.loc[result.country_code.isin(simple_countries), 'postcode'] = None

    return result[['country_code', 'postcode', 'timezone']]


def main():
    postcodes = load_postcode_database()
    postcodes = normalize_postcodes(postcodes)

    postcodes = parse_geometry(postcodes)
    postcodes = lookup_timezones(postcodes)
    lookup_table = build_lookup_table(postcodes)

    db_path = pathlib.Path(__file__).parent / 'postcode_to_timezone_lookup.csv'
    logger.info('Writing %d entries to %s', len(lookup_table), db_path)
    lookup_table.to_csv(db_path, index=False, header=False)


if __name__ == '__main__':
    main()
