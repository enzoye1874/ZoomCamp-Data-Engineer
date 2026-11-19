import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm
import click

dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}
parse_dates = ['tpep_pickup_datetime', 'tpep_dropoff_datetime']


@click.command()
@click.option('--pg-user', default = 'root', help = 'PostgreSQL user')
@click.option('--pg-password', default = 'root123', help = 'PostgreSQL Password')
@click.option('--pg-host', default = 'localhost', help = 'PostgreSQL Host')
@click.option('--pg-port', default = 5432, type = int, help = 'PostgreSQL Port')
@click.option('--pg-database', default = 'ny_taxi', help = 'PostgreSQL Database')
@click.option('--pg-table', default = 'yellow_taxi_data', help = 'PostgreSQL Table')
@click.option('--year', default = 2021, type = int, help = 'Taxi Trip Year')
@click.option('--month', default = 1, type = int, help = 'Taxi Trip Month')
def ingest(pg_user, pg_password, pg_host, pg_port, pg_database, pg_table, year, month):
    prefix = f'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_{year}-{month:02d}.csv.gz'
    engine = create_engine(f'postgresql+psycopg://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_database}')
    df_iter = pd.read_csv(prefix, dtype = dtype, parse_dates = parse_dates, iterator = True, chunksize = 100000)
    first = True
    for df_chunk in tqdm(df_iter):
        if first:
            df_chunk.head(0).to_sql(name = pg_table, con=engine, if_exists = 'replace')
            first = False
            print('Table is Created')
        df_chunk.to_sql(name = pg_table, con=engine, if_exists='append')


if __name__ == '__main__':
    ingest()
