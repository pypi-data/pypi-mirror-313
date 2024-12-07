# Description
You can use this module to retrieve price information, product details, and more from Amazon without needing to understand the SP-API provided by Amazon.

# Usage
Please create a "data" folder directly under the Project folder and create a "config.yaml" file within it.
Next, describe authentication information in the config.yaml file as follows.

amazon_config:  
  &nbsp;SPAPI_LWA_Client_ID: ''  
  &nbsp;SPAPI_LWA_Client_PW: ''  
  &nbsp;SPAPI_Refresh_Token: ''  
  &nbsp;SPAPI_Access_Token_Endpoint: 'https://api.amazon.com/auth/o2/token'  
  &nbsp;SPAPI_IAM_User_Access_Key: ''  
  &nbsp;SPAPI_IAM_User_Secret_Key: ''  
  &nbsp;SPAPI_Service: 'execute-api'  
  &nbsp;SPAPI_Domain: 'sellingpartnerapi-fe.amazon.com'  
  &nbsp;SPAPI_MarketplaceId: 'A1VC38T7YXB528'  
  &nbsp;SPAPI_Region: 'us-west-2'  
  &nbsp;SPAPI_Endpoint: 'https://sellingpartnerapi-fe.amazon.com'  
  &nbsp;SPAPI_SignatureMethod: 'AWS4-HMAC-SHA256'  
  &nbsp;SPAPI_UserAgent: ''  
  &nbsp;SPAPI_Method: 'GET'  

# Install
pip install sp_lib
