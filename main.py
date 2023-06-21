import asyncio
import datetime
from pathlib import Path

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore_async
from dynaconf import Dynaconf
from google.cloud import firestore
from google.cloud.firestore import GeoPoint

from bus import Bus
from generator import generate_random_buses


async def main():
    settings = Dynaconf(
        settings_files=[".settings.local.toml"],
        root_path=Path(__file__).parent,
        merge_enabled=True,
    )

    cred = credentials.Certificate(settings.CRED.json_name)

    firebase_admin.initialize_app(cred)

    db = firestore_async.client()

    buses = db.collection("buses")

    b1_ref = db.collection("routes").document("b1")

    buses_list = generate_random_buses(10000, route=b1_ref)

    coros = []
    for bus in buses_list:
        coros.append(buses.add(bus.return_doc_format()))
        if len(coros) == 50 or bus == buses_list[-1]:
            await asyncio.gather(*coros)
            coros = []

    transaction = db.transaction()
    bus_ref = db.collection("buses").document("00LHbblFf49bqxbYP73q")

    @firestore.async_transactional
    async def update_in_transaction(transaction, bus_ref):
        snapshot = await bus_ref.get(transaction=transaction)
        old_geopoint = snapshot.get("lastLocation")
        new_geopoint = GeoPoint(old_geopoint.latitude + 10, old_geopoint.longitude - 10)
        transaction.update(bus_ref, {"lastLocation": new_geopoint})

    await update_in_transaction(transaction, bus_ref)

    batch = db.batch()

    bus1_ref = db.collection("buses").document("01uL55kb2WHEYCE5ctIB")
    batch.update(bus1_ref, {"lastUpdated": datetime.datetime.now()})

    bus2_ref = db.collection("buses").document("018wdsuGInlffvcyAlPt")
    batch.update(bus2_ref, {"lastUpdated": datetime.datetime.now()})

    bus3_ref = db.collection("buses").document("019hLnmXNX6VkqvU1FQW")
    batch.update(bus3_ref, {"lastUpdated": datetime.datetime.now()})

    await batch.commit()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
