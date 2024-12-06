# TODO(pankaj) Start using this.
# Currently, this is not used, we use fastapi.HTTPException.
class HTTPException(Exception):
    def __init__(self, status_code, detail="HTTP Exception occurred"):
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"{detail}: {status_code}")
