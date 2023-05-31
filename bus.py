class Bus:
    def __init__(self, route=None, last_location=None, last_updated=None, plate=None):
        self.route = route
        self.last_location = last_location
        self.last_updated = last_updated
        self.plate = plate

    def build_from_doc(self, firestore_obj):
        self.route = firestore_obj.get("route")
        self.last_location = firestore_obj.get("lastLocation")
        self.last_updated = firestore_obj.get("lastUpdated", None)
        self.plate = firestore_obj.get("placa", None)

    def return_doc_format(self):
        return {
            "route": self.route,
            "lastLocation": self.last_location,
            "lastUpdated": self.last_updated,
            "placa": self.plate
        }

    def __str__(self):
        return (
            f"Rota: {self.route.id}; Localização: {self.last_location.latitude} - {self.last_location.longitude};"
            f" Atualização: {self.last_updated};"
            f" Placa: {self.plate}"
        )

    def __eq__(self, other):
        return other.plate == self.plate
