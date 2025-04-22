from pyathena import connect
from pyathena.pandas.util import as_pandas

cursor = connect(
    s3_staging_dir='s3://my-athena-query-results-p64/',
    region_name='us-east-1',
    schema_name='athena_database'
).cursor()

query = """SELECT * FROM AddressTable  where city = %(city)s LIMIT 10;"""

params = {
    "city": "Bothell",
}

cursor.execute(query, params)
df = as_pandas(cursor)
print(df.iloc[0])
