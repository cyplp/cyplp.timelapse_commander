import couchdbkit
class StorageFile(couchdbkit.Document):
    batch = couchdbkit.StringProperty()
    filename = couchdbkit.StringProperty()
