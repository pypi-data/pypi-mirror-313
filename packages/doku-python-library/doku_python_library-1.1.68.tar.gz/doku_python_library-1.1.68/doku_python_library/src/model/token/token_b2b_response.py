class TokenB2BResponse :
    
    def __init__(self, 
                 responseCode: str = None, 
                 responseMessage: str = None, 
                 accessToken: str = None, 
                 tokenType: str = None, 
                 expiresIn: int = None, 
                 additionalInfo: str = None) -> None:
        self.response_code = responseCode
        self.response_message = responseMessage
        self.access_token = accessToken
        self.token_type = tokenType
        self.expires_in = expiresIn
        self.additional_info = additionalInfo
        self.generated_timestamp = ''
    
    def json(self) -> dict:
        return {
            "responseCode": self.response_code,
            "responseMessage": self.response_message,
            "accessToken": self.access_token,
            "tokenType": self.token_type,
            "expiresIn": self.expires_in,
            "additionalInfo": self.additional_info
        }