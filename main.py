from pathlib import Path

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from dynaconf import Dynaconf
from bus import Bus

settings = Dynaconf(
    settings_files=[".settings.local.toml"],
    root_path=Path(__file__).parent,
    merge_enabled=True,
)

cred = credentials.Certificate(settings.CRED.json_name)

app = firebase_admin.initialize_app(cred)

db = firestore.client()

buses = db.collection("buses")
docs = buses.stream()

for doc in docs:
    bus = Bus()
    bus.build_from_doc(doc.to_dict())
    print(str(bus))
