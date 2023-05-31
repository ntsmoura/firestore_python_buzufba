import asyncio
from pathlib import Path

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore_async
from dynaconf import Dynaconf
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

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
