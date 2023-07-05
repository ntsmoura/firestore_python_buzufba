from pathlib import Path

import firebase_admin
from dynaconf import Dynaconf
from firebase_admin import credentials, firestore
from google.cloud.firestore_bundle import FirestoreBundle

settings = Dynaconf(
    settings_files=[".settings.local.toml"],
    root_path=Path(__file__).parent,
    merge_enabled=True,
)

cred = credentials.Certificate(settings.CRED.json_name)

firebase_admin.initialize_app(cred)
db = firestore.client()

buses = db.collection("buses")

bundle_id = "onibus_rota_b1"

b1_ref = db.collection("routes").document("b1")

bundle = FirestoreBundle(bundle_id)

query = buses.where("route", "==", b1_ref)

bundle_buffer = (
    bundle.add_named_query(
        "onibus_b1",
        query,
    )
    .build()
)

print(bundle_buffer)

