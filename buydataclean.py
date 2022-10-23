import pandas as pd
from tabulate import tabulate
from django.conf import settings
import Realestate.settings as app_settings
settings.configure(INSTALLED_APPS=app_settings.INSTALLED_APPS,DATABASES=app_settings.DATABASES)
import django
django.setup()
from realestateapp.models import Apartment, Properties


def add_all_states():
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    texas = pd.read_csv('TexasBuy.csv')
    colorado = pd.read_csv('ColoradoBuy.csv')
    florida = pd.read_csv('FloridaBuy.csv')
    newyork = pd.read_csv('NewYorkBuy.csv')
    ohio = pd.read_csv('OhioBuy.csv')
    total = pd.concat([texas, colorado, florida, newyork, ohio], axis=0, ignore_index=True)
    print(tabulate(total, headers=total.columns))
    total.to_csv('TotalBuy.csv', index=False)

def create_records(row):
    apart = Properties.objects.create(
        price=float(row['price']),
        beds = float(row['beds']),
        baths = float(row['baths']),
        garage = row['garage'],
        sqft = row['sqft'],
        year_built = int(row['year_built']),
        address = row['address'],
        postal_code = int(row['postal_code']),
        state = row['state'],
        city = row['city'],
        county = row['county'],
        pictures = row['pictures'],
        pictures1 = row['pictures1'],
    )
    return apart
add_all_states()
df = pd.read_csv('TotalBuy.csv')
print(len(df))
df.dropna(axis=0, subset=['year_built', 'baths', 'sqft', 'price', 'beds', 'postal_code'], inplace=True)

df['db'] = df.apply(lambda row: create_records(row), axis=1)
df.to_csv('TotalBuy1.csv', index=False)
print(tabulate(df.head(5), headers=df.columns))

print(Properties.objects.all())

