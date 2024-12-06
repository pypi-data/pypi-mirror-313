from doku_python_library.src.model.direct_debit.account_binding_additional_info_response import AccountBindingAdditionalInfoResponse

class AccountBindingResponse:

    def __init__(self, responseCode: str = None, responseMessage: str = None, 
                 referenceNo: str = None, redirectUrl: str = None, additionalInfo: AccountBindingAdditionalInfoResponse = None) -> None:
        self.response_code = responseCode
        self.response_message = responseMessage
        self.reference_no = referenceNo
        self.redirect_url = redirectUrl
        self.additional_info = additionalInfo
    
    def json(self) -> dict:
        response = {
            "responseCode": self.response_code if self.response_code is not None else None,
            "responseMessage": self.response_message if self.response_message is not None else None,
        }
        if self.reference_no is not None:
            response["referenceNo"] = self.reference_no
        if self.redirect_url is not None:
            response["redirectUrl"] = self.redirect_url 
        if self.additional_info is not None:
            response["additionalInfo"] = self.additional_info 
        return response