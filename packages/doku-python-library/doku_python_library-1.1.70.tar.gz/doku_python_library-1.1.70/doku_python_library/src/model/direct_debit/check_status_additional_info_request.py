from doku_python_library.src.model.va.origin import Origin
class CheckStatusAdditionalInfoRequest:

    def __init__(self, device_id: str = None, channel: str = None) -> None:
        self.device_id = device_id
        self.channel = channel
    
    def json(self) -> dict:
        return {
            "deviceId": self.device_id,
            "channel": self.channel,
            "origin": Origin.create_request_body()
        }