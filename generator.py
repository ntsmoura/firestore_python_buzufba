import datetime

from faker import Faker
from bus import Bus
from google.cloud.firestore import GeoPoint

fake = Faker("pt_BR")
Faker.seed(0)


def generate_random_buses(n, route):
    buses_list = []
    for _ in range(n+1):
        last_location = fake.local_latlng(country_code="BR")
        last_location = GeoPoint(float(last_location[0]), float(last_location[1]))
        bus = Bus(
            plate=fake.license_plate().replace("-", ""),
            last_updated=datetime.datetime.now(),
            last_location=last_location,
            route=route,
        )
        if bus not in buses_list:
            buses_list.append(bus)
    return buses_list