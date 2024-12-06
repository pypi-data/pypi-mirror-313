# Postcode to Timezone

Looks up timezones based on postcode. This is based on the assumption that
postcodes are roughly following the timezone lines. This is not always true,
especially in disputed territories, but it is a good approximation for most
cases.

The data used for this lookup is indirectly from OpenStreetMap.

## Usage example

```python
from postcode_to_timezone import get_tz

get_tz('us', '12345')
```

returns `'America/Chicago'`

## Building

To regenerate the lookup table, first obtain a dump of the location_postcode
table from a Nominatim database, and compress it to `location_postcode.csv.xz`.
Then run `python3 generate_lookup_table.py` to generate the lookup table.

Actual package is built with `hatch build`, and the package is uploaded to PyPI
with `hatch publish`.

## Data sources

### Postcode locations

A dump of the location_postcode table in a Nominatim database. Nominatim
creates this database from OpenStreetMap data using the following query:

```sql
SELECT
    COALESCE(plx.country_code, get_country_code(ST_Centroid(pl.geometry))) as country_code,
    pl.address->'postcode' as postcode,
    COALESCE(plx.centroid, ST_Centroid(pl.geometry)) as geometry
  FROM place AS pl
  LEFT OUTER JOIN placex AS plx
         ON pl.osm_id = plx.osm_id AND pl.osm_type = plx.osm_type
WHERE
 pl.address ? 'postcode'
 AND pl.geometry IS NOT null
```

A dump from that table is stored at `location_postcode.csv.xz`.

### Postcode validation

A copy from this [GitHub Gist](https://gist.githubusercontent.com/lkopocinski/bd4494588458f5a8cc8ffbd12a4deefd/raw/6bc84f50091852ecfa0ee6ea4b506cabcea1cc52/postal_codes_regex.json)
is stored in `postcode_regex.json`. Actual source not known.

### Timezone definitions

Timezone definitions are used from `timezonefinder` package on
[pypi](https://pypi.org/project/timezonefinder/). The package is licensed under
the MIT license.
