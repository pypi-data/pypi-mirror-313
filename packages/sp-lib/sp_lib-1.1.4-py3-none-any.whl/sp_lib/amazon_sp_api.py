import collections
import hashlib
import hmac
import time
from itertools import islice

import pandas
import urllib.parse
import requests
import json
import yaml
from datetime import datetime
from requests.exceptions import RequestException, ConnectionError, HTTPError, Timeout


class Amazon(object):
    def __init__(self):
        with open('./data/config.yaml', 'r') as yaml_file:
            config_data = yaml.safe_load(yaml_file)
        self.spapi_lwa_client_id = config_data['amazon_config']['SPAPI_LWA_Client_ID']
        self.spapi_lwa_client_pw = config_data['amazon_config']['SPAPI_LWA_Client_PW']
        self.spapi_refresh_token = config_data['amazon_config']['SPAPI_Refresh_Token']
        self.spapi_access_token_endpoint = config_data['amazon_config']['SPAPI_Access_Token_Endpoint']
        self.spapi_iam_user_access_key = config_data['amazon_config']['SPAPI_IAM_User_Access_Key']
        self.spapi_iam_user_secret_key = config_data['amazon_config']['SPAPI_IAM_User_Secret_Key']
        self.spapi_service = config_data['amazon_config']['SPAPI_Service']
        self.spapi_domain = config_data['amazon_config']['SPAPI_Domain']
        self.spapi_marketplaceid = config_data['amazon_config']['SPAPI_MarketplaceId']
        self.spapi_region = config_data['amazon_config']['SPAPI_Region']
        self.spapi_endpoint = config_data['amazon_config']['SPAPI_Endpoint']
        self.spapi_signature_method = config_data['amazon_config']['SPAPI_SignatureMethod']
        self.spapi_user_agent = config_data['amazon_config']['SPAPI_UserAgent']
        self.spapi_seller_id = config_data['amazon_config']['SPAPI_Seller_ID']
        self.time_gettoken = None
        self.token = None
        self.amazon_url = 'https://www.amazon.co.jp/dp/'
        self.retry_interval = 10
        self.retry_count = 3

    # トークンを取得するクラスメソッド
    def get_token(self):
        """
        Method to get token
        Parameters
        ----------
        None

        Returns
        ----------
        None
        """
        print('func : get_token')

        # 認証情報の作成
        auth = (self.spapi_lwa_client_id, self.spapi_lwa_client_pw)

        # Postパラメータ生成
        params = {
            "grant_type": "refresh_token",
            "refresh_token": self.spapi_refresh_token
        }

        # Postリクエスト処理の実行
        response = requests.post(url=self.spapi_access_token_endpoint, auth=auth, params=params)

        # レスポンスをjson型へでコード
        response_json = response.json()

        # Postに対するレスポンスの確認
        print(response, flush=True)
        print(json.dumps(response_json, indent=2, ensure_ascii=False), flush=True)

        # 値の取得
        response_access_token = response_json['access_token']
        response_refresh_token = response_json['refresh_token']
        response_token_type = response_json['token_type']
        response_expires_in = response_json['expires_in']

        # トークンを取得した時刻(エポック秒)をメンバ変数へ
        self.time_gettoken = time.time()
        print('トークンを取得したエポック秒 :' + str(self.time_gettoken))

        # 所得したトークンをクラス変数へ
        self.token = response_access_token

        # return response_access_token, response_refresh_token, response_token_type, response_expires_in

    # ASINからAmazonのURLを生成するメソッド
    def make_amazon_url(self, asin):
        """
        ASINをつけてAmazon urlを生成する関数。asinをリストで渡すとAmazon urlをリストで返す
        Parameters
        ----------
        asin : str or List[str]
            ASINをstrで指定。リストで渡すことも可能。

        Returns
        ----------
        url_dict : dict
            {ASIN1: Amazon url1, ASIN2: Amazon url2, ...}
        """
        url_dict = {}
        if isinstance(asin, list):
            for elem in asin:
                if elem is not None:
                    url = self.amazon_url + elem
                    url_dict[elem] = url
            return url_dict
        else:
            url = self.amazon_url + asin
            url_dict[asin] = url
            return url_dict

    # Request Header(GET)を作成するメソッド
    def make_get_request_headers(self, method, canonical_uri, request_parameters, token):
        # ************* REQUEST VALUES *************
        service = self.spapi_service
        host = 'sellingpartnerapi-fe.amazon.com'
        region = self.spapi_region
        user_agent = self.spapi_user_agent

        access_key = self.spapi_iam_user_access_key
        secret_key = self.spapi_iam_user_secret_key

        # Key derivation functions. See:
        # http://docs.aws.amazon.com/general/latest/gr/signature-v4-examples.html#signature-v4-examples-python

        def sign(key, msg):
            return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

        def getSignatureKey(key, dateStamp, regionName, serviceName):
            kDate = sign(('AWS4' + key).encode('utf-8'), dateStamp)
            kRegion = sign(kDate, regionName)
            kService = sign(kRegion, serviceName)
            kSigning = sign(kService, 'aws4_request')
            return kSigning

        # Read AWS access key from env. variables or configuration file. Best practice is NOT
        # to embed credentials in code.
        if access_key is None or secret_key is None:
            raise Exception('No access key is available.')

        # Create a date for headers and the credential string
        t = datetime.utcnow()
        amzdate = t.strftime('%Y%m%dT%H%M%SZ')
        # Date w/o time, used in credential scope
        datestamp = t.strftime('%Y%m%d')

        # ************* TASK 1: CREATE A CANONICAL REQUEST *************
        # http://docs.aws.amazon.com/general/latest/gr/sigv4-create-canonical-request.html
        canonical_querystring = request_parameters
        canonical_headers = 'host:' + host + '\n' + 'x-amz-date:' + amzdate + '\n'

        signed_headers = 'host;x-amz-date'

        payload_hash = hashlib.sha256(('').encode('utf-8')).hexdigest()

        canonical_request = method + '\n' + canonical_uri + '\n' + canonical_querystring + \
                            '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash

        # ************* TASK 2:     *************
        algorithm = 'AWS4-HMAC-SHA256'
        credential_scope = datestamp + '/' + region + \
                           '/' + service + '/' + 'aws4_request'
        string_to_sign = algorithm + '\n' + amzdate + '\n' + credential_scope + \
                         '\n' + \
                         hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()

        # ************* TASK 3: CALCULATE THE SIGNATURE *************
        signing_key = getSignatureKey(secret_key, datestamp, region, service)

        # Sign the string_to_sign using the signing_key
        signature = hmac.new(signing_key, (string_to_sign).encode(
            'utf-8'), hashlib.sha256).hexdigest()

        # ************* TASK 4: ADD SIGNING INFORMATION TO THE REQUEST *************
        authorization_header = algorithm + ' ' + 'Credential=' + access_key + '/' + \
                               credential_scope + ', ' + 'SignedHeaders=' + \
                               signed_headers + ', ' + 'Signature=' + signature

        # x-amz-date はPostmanでは自動で付与してくれるので設定してませんが必要です
        headers = {'x-amz-access-token': token, 'user-agent': user_agent,
                   'x-amz-date': amzdate, 'Authorization': authorization_header}

        return headers

    # Request Header(POST)を作成するメソッド
    def make_post_request_headers(self, method, canonical_uri, request_parameters, token):
        # ************* REQUEST VALUES *************
        service = self.spapi_service
        host = 'sellingpartnerapi-fe.amazon.com'
        region = self.spapi_region
        user_agent = self.spapi_user_agent
        content_type = 'application/json'

        access_key = self.spapi_iam_user_access_key
        secret_key = self.spapi_iam_user_secret_key

        # Key derivation functions. See:
        # http://docs.aws.amazon.com/general/latest/gr/signature-v4-examples.html#signature-v4-examples-python
        def sign(key, msg):
            return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

        def getSignatureKey(key, date_stamp, regionName, serviceName):
            kDate = sign(('AWS4' + key).encode('utf-8'), date_stamp)
            kRegion = sign(kDate, regionName)
            kService = sign(kRegion, serviceName)
            kSigning = sign(kService, 'aws4_request')
            return kSigning

        if access_key is None or secret_key is None:
            raise Exception('No access key is available.')

        t = datetime.utcnow()
        amz_date = t.strftime('%Y%m%dT%H%M%SZ')
        date_stamp = t.strftime('%Y%m%d')

        # ************* TASK 1: CREATE A CANONICAL REQUEST *************
        # http://docs.aws.amazon.com/general/latest/gr/sigv4-create-canonical-request.html

        canonical_querystring = ''
        canonical_headers = 'content-type:' + content_type + '\n' + \
                            'host:' + host + '\n' + 'x-amz-date:' + amz_date + '\n'

        signed_headers = 'content-type;host;x-amz-date'
        # signed_headers = 'host;x-amz-content-sha256;x-amz-date'

        payload_hash = hashlib.sha256(request_parameters.encode('utf-8')).hexdigest()

        # 空文字のハッシュを生成
        none_hash = hashlib.sha256(('').encode('utf-8')).hexdigest()

        canonical_request = method + '\n' + canonical_uri + '\n' + canonical_querystring + \
                            '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash

        # ************* TASK 2: CREATE THE STRING TO SIGN*************
        # Match the algorithm to the hashing algorithm you use, either SHA-1 or
        # SHA-256 (recommended)
        algorithm = 'AWS4-HMAC-SHA256'
        credential_scope = date_stamp + '/' + region + \
                           '/' + service + '/' + 'aws4_request'
        string_to_sign = algorithm + '\n' + amz_date + '\n' + credential_scope + \
                         '\n' + \
                         hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()

        # ************* TASK 3: CALCULATE THE SIGNATURE *************
        # Create the signing key using the function defined above.
        signing_key = getSignatureKey(secret_key, date_stamp, region, service)

        signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()

        # ************* TASK 4: ADD SIGNING INFORMATION TO THE REQUEST *************
        authorization_header = algorithm + ' ' + 'Credential=' + access_key + '/' + \
                               credential_scope + ', ' + 'SignedHeaders=' + \
                               signed_headers + ', ' + 'Signature=' + signature

        headers = {'user-agent': user_agent,
                   'x-amz-access-token': token,
                   # 'x-amz-content-sha256': none_hash,
                   'x-amz-date': amz_date,
                   'Authorization': authorization_header,
                   'Content-Type': content_type}

        return headers


class SpApiMethod(Amazon):
    # トークンが有効かチェックするデコレーター
    def check_expire(func):
        def wrapper(self, *args, **kwargs):
            print('Checking token expire with chech_expire@decorator')
            # トークンが無ければ取得
            if self.token is None:
                self.get_token()
            # トークンがあってExpireの5分前なら再度トークンを取得
            elif self.time_gettoken is not None:
                time_now = time.time()
                diff_time = time_now - self.time_gettoken
                if diff_time > 3300:
                    self.get_token
            result = func(self, *args, **kwargs)
            return result
        return wrapper

    @check_expire
    def get_item_offers_for_asin(self, asin_code, data_type='json'):
        """
        :param1 asin_code: ASIN
        :param2 data_type: json or lowest_price or cart_price or number_of_offers
                default: json
        :return: depent on data_type
                data_type = json: return json
                data_type = lowest_price: return int(lowest price)
                data_type = cart_price: return int(cart price)
                data_type = number_of_offers: return int(number of offers)

        Rate(request per sec): 0.5
        Burst: 1
        """
        print('func : get_item_offers_for_asin')

        # Version: 2020-12-01
        # パス設定
        sp_api_path = '/products/pricing/v0/items/{}/offers'.format(asin_code)

        # リクエストパラメータ設定(パラメータはアルファベット順にすること&URLエンコードは必須)
        request_parameters_unencode = {
            'ItemCondition': 'New',
            'MarketplaceId': str(self.spapi_marketplaceid)
        }
        request_parameters = urllib.parse.urlencode(request_parameters_unencode)

        # URI設定
        canonical_uri = sp_api_path

        headers = self.make_get_request_headers('GET', canonical_uri, request_parameters, self.token)

        # APIリクエストURLの生成
        request_url = self.spapi_endpoint + canonical_uri + '?' + request_parameters

        # リクエスト送信
        print('===Request===')
        print('Request URL = ' + request_url)
        print('Headers = ' + str(headers))
        api_response = requests.get(request_url, headers=headers)

        # レスポンスをdictに
        response_dict = json.loads(api_response.text)

        # 加工
        response_json = json.dumps(response_dict, indent=2, ensure_ascii=False)

        # 表示
        print('=== Response detail -get_item_offers_for_asin ===')
        print('Response status : ' + str(api_response.status_code))
        print('Response headers :\r\n' + str(api_response.headers))
        print('Response json :\r\n' + str(response_json))

        # Lowest priceを取得
        try:
            lowest_price = int(response_dict['payload']['Summary']['LowestPrices'][0]['LandedPrice']['Amount'])
        except KeyError:
            lowest_price = None

        # Cart priceを取得
        try:
            cart_price = int(response_dict['payload']['Summary']['BuyBoxPrices'][0]['LandedPrice']['Amount'])
        except KeyError:
            cart_price = None

        # 出品者数を取得
        try:
            number_of_offers = int(response_dict['payload']['Summary']['NumberOfOffers'][0]['OfferCount'])
        except KeyError:
            number_of_offers = None

        if data_type == 'json':
            return response_json
        elif data_type == 'lowest_price':
            return lowest_price
        elif data_type == 'cart_price':
            return cart_price
        elif data_type == 'number_of_offers':
            return number_of_offers
        else:
            return response_json

    @check_expire
    def get_search_catalog_items(self, code, identifier='asin', includeddata='summaries', wait=1):
        """
        :param code: ASIN code or JAN code
        :param identifier: 'jan' or 'asin'
                            For identifying 'code'.
        :param includeddata: 'summaries' or 'dimensions' or 'identifiers' or 'images' or 'productTypes' or 'relationships'
        or 'salesRanks' or 'vendorDetails'
        Separate with ',' when you request multiple info. Default value is 'summaries'
        :return: json
        Rate(requests per sec): 0.5
        Burst: 1
        """
        print('func : get_search_catalog_items')

        # Version: 2022-04-01
        # パス設定
        sp_api_path = '/catalog/2022-04-01/items'

        # codeがリスト型であればコンマ区切りにする
        if isinstance(code, str):
            request_code = code
        elif isinstance(code, list):
            request_code = ','.join(code)

        # codeがJANコードの場合
        if identifier == 'jan' or identifier == 'jan_list':
            # リクエストパラメータ設定(パラメータはアルファベット順にすること&URLエンコードは必須)
            request_parameters_unencode = {
                'identifiers': request_code,
                'identifiersType': 'JAN',
                'includedData': includeddata,
                'marketplaceIds': str(self.spapi_marketplaceid)
            }
        elif identifier == 'asin' or identifier == 'asin_list':
            request_parameters_unencode = {
                'identifiers': request_code,
                'identifiersType': 'ASIN',
                'includedData': 'dimensions,images,salesRanks,summaries,identifiers',
                'marketplaceIds': str(self.spapi_marketplaceid)
            }
        request_parameters = urllib.parse.urlencode(request_parameters_unencode)

        # URI設定
        canonical_uri = sp_api_path

        headers = self.make_get_request_headers('GET', canonical_uri, request_parameters, self.token)

        # APIリクエストURLの生成
        request_url = self.spapi_endpoint + canonical_uri + '?' + request_parameters

        # リクエスト送信
        print('===Request===')
        print('Request URL = ' + request_url)
        print('Headers = ' + str(headers))
        api_response = requests.get(request_url, headers=headers)

        # Wait
        time.sleep(wait)

        # レスポンスをdictに
        response_dict = json.loads(api_response.text, object_pairs_hook=collections.OrderedDict)

        # 加工
        response_json = json.dumps(response_dict, indent=2, ensure_ascii=False)

        # 表示
        print('=== Response detail -get_search_catalog_items ===')
        print('Response status : ' + str(api_response.status_code))
        print('Response headers :\r\n' + str(api_response.headers))
        print('Response json :\r\n' + str(response_json))

        return response_json

    @check_expire
    def get_items_offers_batch(self, asin_list, wait=7):
        """
        :param asin_list: Max20
        :return: api_response
        Rate(requests per second): 0.5
        Burst: 1
        """
        print('func : get_items_offers_batch')

        # Version: 2020-12-01
        # パス設定
        sp_api_path = '/batches/products/pricing/v0/itemOffers'

        # ASIN毎のKeyとValueを格納するリストをまず定義
        list_data = []
        for index, asin in enumerate(asin_list):
            data = {
                'uri': '/products/pricing/v0/items/{}/offers'.format(asin),
                'method': 'GET',
                'MarketplaceId': self.spapi_marketplaceid,
                'ItemCondition': 'New'
            }
            list_data.append(data)

        # 上記のdata(リスト)を"requests"にリストとして格納
        body = {'requests': list_data}

        # request_parameters = urllib.parse.urlencode(body)
        request_parameters = json.dumps(body)

        # URI設定
        canonical_uri = sp_api_path

        headers = self.make_post_request_headers('POST', canonical_uri, request_parameters, self.token)

        # APIリクエストURLの生成
        end_point = self.spapi_endpoint + canonical_uri

        # エラーの時はリトライ
        for i in range(0, self.retry_count):
            try:
                # リクエスト送信
                print('===Request===')
                print('Request URL = ' + end_point)
                print('Request headers = ' + str(headers))
                # print('Request parameters = ' + str(request_parameters))
                api_response = requests.post(end_point, data=request_parameters, headers=headers)
                print('Response status : ' + str(api_response.status_code))
                print('Response headers :\r\n' + str(api_response.headers))
                # print('Response body :\r\n' + str(api_response.content))
                api_response.raise_for_status()
                time.sleep(wait)
                return api_response
                break
            except HTTPError:
                if i + 1 == self.retry_count:
                    print("リトライエラー:最大回数{}回のリトライに失敗しました".format(self.retry_count))
                    return api_response
                    break
                    # raise Exception
                time.sleep(self.retry_interval)
                print("HTTP Error:", HTTPError)
                print("リトライ回数:{}回目です".format(i + 1))
                continue

    # ASINリストを元にFBA手数料を返すクラスメソッド
    @check_expire
    def get_myfees_estimates(self, lowest_price_dict, wait=2):
        '''
        :param lowest_price_dict: ASIN and Lowest price dictionary
        :return: ASIN and FBA fees dictionary
        {'B03219024398': 714, 'B09832132123': 980, ...}
        '''
        print('func : get_myfees_estimates')
        # パス設定
        sp_api_path = '/products/fees/v0/feesEstimate'
        # Postのbodyとなるリストを定義
        body = []
        for asin,lowest_price in lowest_price_dict.items():
            data = {
                "FeesEstimateRequest": {
                    "MarketplaceId": self.spapi_marketplaceid,
                    "IsAmazonFulfilled": True,
                    "PriceToEstimateFees": {
                        "ListingPrice": {
                            "CurrencyCode": "JPY",
                            "Amount": lowest_price
                        },
                        "Shipping": {
                            "CurrencyCode": "JPY",
                            "Amount": 0
                        },
                        "Points": {
                            "PointsNumber": 0,
                            "PointsMonetaryValue": {
                                "CurrencyCode": "JPY",
                                "Amount": 0
                            }
                        }
                    },
                    "Identifier": asin
                },
                "IdType": "ASIN",
                "IdValue": asin
            }
            body.append(data)

        request_parameters = json.dumps(body)

        # URI設定
        canonical_uri = sp_api_path

        headers = self.make_post_request_headers('POST', canonical_uri, request_parameters, self.token)

        # APIリクエストURLの生成
        end_point = self.spapi_endpoint + canonical_uri

        # リクエスト送信
        print('===Request===')
        print('Request URL = ' + end_point)
        print('Request headers = ' + str(headers))
        # print('Request parameters = ' + str(request_parameters))
        api_response = requests.post(end_point, data=request_parameters, headers=headers)
        print('Response status : ' + str(api_response.status_code))
        print('Response headers :\r\n' + str(api_response.headers))
        # print('Response body :\r\n' + str(api_response.content))

        # Wait
        time.sleep(wait)

        # レスポンスをdictに
        response_dict = json.loads(api_response.text)

        # 加工
        response_json = json.dumps(response_dict, indent=4, ensure_ascii=False)

        # print('Response json :\r\n' + str(response_json))

        return api_response

    # ASINから出品可能かチェックするクラスメソッド
    @check_expire
    def get_listings_restrictions(self, asin, wait=1):
        # パス設定
        sp_api_path = '/listings/2021-08-01/restrictions'
        request_parameters_unencode = {
            'asin': asin,
            'conditionType': 'new_new',
            'sellerId': self.spapi_seller_id,
            'marketplaceIds': str(self.spapi_marketplaceid)
        }
        request_parameters = urllib.parse.urlencode(request_parameters_unencode)
        # URI設定
        canonical_uri = sp_api_path

        headers = self.make_get_request_headers('GET', canonical_uri, request_parameters, self.token)

        # APIリクエストURLの生成
        request_url = self.spapi_endpoint + canonical_uri + '?' + request_parameters

        # リクエスト送信
        print('===Request===')
        print('Request URL = ' + request_url)
        print('Headers = ' + str(headers))
        api_response = requests.get(request_url, headers=headers)

        # Wait
        time.sleep(wait)

        # レスポンスをdictに
        response_dict = json.loads(api_response.text, object_pairs_hook=collections.OrderedDict)

        # 加工
        response_json = json.dumps(response_dict, indent=2, ensure_ascii=False)

        # 表示
        print('=== Response detail -get_listings_restrictions ===')
        print('Response status : ' + str(api_response.status_code))
        print('Response headers :\r\n' + str(api_response.headers))
        # print('Response json :\r\n' + str(response_json))

        return response_dict

    # 危険物かチェックするクラスメソッド
    @check_expire
    def check_fba_inbound(self, asin, wait=1):
        # パス設定
        sp_api_path = '/fba/inbound/v1/eligibility/itemPreview'
        request_parameters_unencode = {
            'asin': asin,
            'marketplaceIds': str(self.spapi_marketplaceid),
            'program': 'INBOUND'
        }
        request_parameters = urllib.parse.urlencode(request_parameters_unencode)
        # URI設定
        canonical_uri = sp_api_path

        headers = self.make_get_request_headers('GET', canonical_uri, request_parameters, self.token)

        # APIリクエストURLの生成
        request_url = self.spapi_endpoint + canonical_uri + '?' + request_parameters

        # リクエスト送信
        print('===Request===')
        print('Request URL = ' + request_url)
        print('Headers = ' + str(headers))
        api_response = requests.get(request_url, headers=headers)

        # Wait
        time.sleep(wait)

        # レスポンスをdictに
        response_dict = json.loads(api_response.text, object_pairs_hook=collections.OrderedDict)

        # 加工
        response_json = json.dumps(response_dict, indent=2, ensure_ascii=False)

        # 表示
        print('=== Response detail -get_listings_restrictions ===')
        print('Response status : ' + str(api_response.status_code))
        print('Response headers :\r\n' + str(api_response.headers))
        # print('Response json :\r\n' + str(response_json))

        return response_dict

    # get_items_offers_batchからASINと最安値(辞書型)とカート情報(辞書型)を返すクラスメソッド
    def get_lowest_prices_batch(self, asin_list, wait=7):
        """
        get_items_offers_batchを使ってASINと最安値、カート取得情報を取得する
        :param asin_list: list
            ASINのリスト(Max20個まで)
        :return: lowest_prices(dict), buy_box(dict)
            lowest_priceが最安値、buy_boxは誰がカートをとっているか
            Curt by Amazon・・・Amazonがカートを取得
            Curt by 3rd-Party・・・Amazon以外がカートを取得
            No Curt・・・カートなし
            例えば以下のように返される
            ex)
            lowest_prices{"ASIN1": int(lowest price1),"ASIN2": int(lowest price2),...}
            buy_box{"ASIN1": str('Curt by Amazon'),"ASIN2": str('Curt by 3rd-Party'),"ASIN3": str('No Curt'),...}
        """
        print("func : get_lowest_prices_batch")
        results = self.get_items_offers_batch(asin_list, wait)

        # get_items_offers_batchのレスポンスからASINと最安値をdictへ
        # resultsをjsonへ
        response_dict = json.loads(results.text)
        response_json = json.dumps(response_dict, indent=4, ensure_ascii=False)

        lowest_prices = {}
        buy_box = {}

        for index, asin in enumerate(asin_list):
            try:
                reffered_asin = response_dict['responses'][index]['body']['payload']['ASIN']
            except:
                lowest_prices[asin] = None
                continue
            try:
                price_anchor = response_dict['responses'][index]['body']['payload']['Summary']['LowestPrices']
            except:
                lowest_prices[asin] = None
                continue
            price_list = []
            for i in range(len(price_anchor)):
                condtion = price_anchor[i].get('condition')
                if condtion == 'new' and reffered_asin == asin:
                    price_list.append(price_anchor[i]['LandedPrice'].get('Amount'))
            if len(price_list) != 0:
                lowest_prices[asin] = min(price_list)
            else:
                lowest_prices[asin] = None

            # カートがAmazonかどうかをチェックする
            # Offers以降をリストにする
            try:
                buy_box_anchor = response_dict['responses'][index]['body']['payload']['Offers']
            except:
                buy_box[asin] = None
                continue
            # Offersの数だけループ
            for i in range(len(buy_box_anchor)):
                winner = buy_box_anchor[i].get('IsBuyBoxWinner')
                seller_id = buy_box_anchor[i].get('SellerId')
                # IsBuyBoxWinnerがtrueのとき(つまりカートを取得している出品者)
                if winner is True:
                    if seller_id == 'AN1VRQENFRJN5':
                        buy_box[asin] = 'Curt by Amazon'
                        break
                    else:
                        buy_box[asin] = 'Curt by 3rd-Party'
                        break
                else:
                    buy_box[asin] = 'No Curt'

        return lowest_prices, buy_box

    # get_search_catalog_itemsからASINを返すメソッド
    # 現状は1by1 リストで指定すると順不同で返ってきてしまう
    def jan2asin(self, code, identifier='jan'):
        response_json = self.get_search_catalog_items(code, identifier=identifier)
        response_dict = json.loads(response_json, object_pairs_hook=collections.OrderedDict)
        target_response = response_dict['items']
        asin_dict = {}
        if len(target_response):
            target_json = json.dumps(target_response, indent=4, ensure_ascii=False)
            df = pandas.read_json(target_json)
            # print(df.head())
            if isinstance(code, str):
                asin_dict[code] = df.loc[0, 'asin']
            elif isinstance(code, list):
                for index, jan in enumerate(code):
                    asin_dict[jan] = df.loc[index, 'asin']
        else:
            asin_dict[code] = None
        return asin_dict

    def jan2asin_ranking(self, code, identifier='jan'):
        response_json = self.get_search_catalog_items(code, identifier=identifier, includeddata='salesRanks')
        response_dict = json.loads(response_json)
        try:
            asin = response_dict['items'][0]['asin']
        except:
            asin = None
        try:
            category = response_dict['items'][0]['salesRanks'][0]['displayGroupRanks'][0]['title']
        except:
            category = None
        try:
            ranking = response_dict['items'][0]['salesRanks'][0]['displayGroupRanks'][0]['rank']
        except:
            ranking = 0
        return asin, category, ranking

    # ASINとLowest_priceを20個に分割してget_myfees_estimatesへ送信
    def get_fba_fees(self, lowest_price_dict):
        # lowest_price_dictからASINがNoneのものを取除く
        filtered_dict = {asin: lowest_price for asin, lowest_price in lowest_price_dict.items() if asin is not None and lowest_price is not None}
        # 辞書を20個に分割
        it = iter(filtered_dict)
        full_dict = {}
        for i in range(0, len(filtered_dict), 20):
            split_dict = {k: filtered_dict[k] for k in islice(it, 20)}
            results = self.get_myfees_estimates(split_dict)
            # resultをdictに変換
            response_list = json.loads(results.text)
            # responseのリスと数だけASINとFBA Feeを繰り返し取得
            for n in range(len(response_list)):
                # resultからASINを抽出
                try:
                    asin = response_list[n]['FeesEstimateIdentifier']['IdValue']
                except:
                    asin = None
                try:
                    estimate_fee = response_list[n]['FeesEstimate']['TotalFeesEstimate'].get('Amount')
                except:
                    estimate_fee = None
                full_dict[asin] = estimate_fee
        # print(full_dict)
        return full_dict

    # check_fba_inboundを使ったラッパー関数
    def check_dangerous_goods(self, asin):
        '''
        危険物かどうかcheck_fba_inboundを使ったラッパー関数
        :param asin: リスト型もOK
        :return: asinがリスト型なら{asin1: "納品可能", asin2: "納品不可"...}
        のように辞書型で返す
        注意:危険物でもFBAに納品できるものは"納品可能"を返す
        '''
        # get_listings_restrictionsのレスポンスから納品可能かを返す関数
        def dengerous_goods(response):
            # print(response)
            # print(type(response))
            # restrict_data = response[0]['payload'][0]['isEligibleForProgram']
            restrict_data = response['payload']['isEligibleForProgram']
            if restrict_data is True:
                return "納品可能"
            elif restrict_data is False:
                return "納品不可"
            else:
                return "判別不能"

        # asinがリスト型からfor文で繰り返し
        # リスト型ならASINとrestriction infoの辞書型を設定
        restrict_info = {}
        if isinstance(asin, list):
            for index, row in enumerate(asin):
                response = self.check_fba_inbound(row)
                result = dengerous_goods(response)
                restrict_info[row] = result
            return restrict_info
        elif isinstance(asin, str):
            response = self.check_fba_inbound(asin)
            result = dengerous_goods(response)
            return result
        else:
            print('ASINが設定されていません')
            return ''

    # get_listings_restrictionsを使ったラッパー関数
    def get_approval_restrictions_info(self, asin):
        '''
        出品制限がないかget_listings_restrictionsを使ったラッパー関数
        :param asin: リスト型もOK
        :return: asinがリスト型なら{asin1: restriction info1, asin2: restriction info2...}
        のように辞書型で返す
        '''

        # get_listings_restrictionsのレスポンスから納品可能かを返す関数
        def restriction_info(response):
            # print(response)
            # print(type(response))
            restrict_data = response['restrictions']
            if not restrict_data:
                return "出品可能"
            else:
                rest_reason = restrict_data[0]['reasons'][0]['reasonCode']
                return rest_reason

        # asinがリスト型からfor文で繰り返し
        # リスト型ならASINとrestriction infoの辞書型を設定
        restrict_info = {}
        if isinstance(asin, list):
            for index, row in enumerate(asin):
                response = self.get_listings_restrictions(row)
                result = restriction_info(response)
                restrict_info[row] = result
            return restrict_info
        elif isinstance(asin, str):
            response = self.get_listings_restrictions(asin)
            result = restriction_info(response)
            return result
        else:
            print('ASINが設定されていません')
            return ''
