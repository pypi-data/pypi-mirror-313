import json
import httpx
import boto3

def auth_4docs() -> str:
    """

    Returns:
        str: Bearer token code 
    """

    BASE_URL : str = "https://api.4docs.cloud"
    url : str = BASE_URL + "/v2/oauth2/token"

    querystring = {"grant_type":"client_credentials"}

    # TODO : Colocar nos secrets
    headers = {
        "grant_type": "client_credentials",
        "Authorization": "Basic ZGlnaXRhbEBlY29tZW5lcmdpYS5jb20uYnI6Z0dsQm4zdXdqaVdDYlp4"
    }

    payload = ""
    
    r = httpx.request("POST", url, data=payload, headers=headers, params=querystring,verify=False)

    return (r.json()).get("access_token")

def enrich_energy_account_with_4docs(bucket_name : str, s3_path : str) -> dict:
    """
    """

    bearer_token : str = auth_4docs()
    s3_client = boto3.client('s3')
    data = s3_client.get_object(Bucket=bucket_name, Key=s3_path)
    content = data['Body'].read()

    BASE_URL : str = "https://api.4docs.cloud"
    url : str = BASE_URL + "/v2/quick_parse/9fbc3a280191a0428e55c4a8fb235d8c"

    file_name_formatted : str = s3_path.split('/')[-1]

    files=[
        ('file',(file_name_formatted,content,'application/pdf'))
    ]

    payload = {'json': '{"callbackUrl":"https://api.4docs.cloud/v2/null","pipelineName":"energy","clientData":{"fatura_id":123}}'}

    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }

    r = httpx.request("POST", url, headers=headers, data=payload, files=files,verify=False)

    if r.status_code == 200:
        return r.json()
    else:
        raise Exception(f"Error on 4docs API | {r.status_code} | {r.text}")

def format_response(input_data : dict, result : dict,processed_at : str) -> dict:
    """
    """
    
    extraction_result : dict = result
    address_result : dict = json.loads((extraction_result['endereco']).replace("'",'"'))

    # 
    reliability : int = int(extraction_result['confiabilidade'])
    cnpj : str = (extraction_result['cnpj_distribuidora']).zfill(14)

    trust : bool = True if reliability >= 85 else False

    if trust == True:

        return {
            "transaction":{
                "id": input_data['transaction_id'],
                "client":input_data['response_info']['client'],
                "processed_at":processed_at,
                "reliability": reliability,
                "trust":trust,
                "notes":extraction_result['observacao'],
            },
            "data" : {
                    "providerData": {
                    "name" : extraction_result.get('nome_distribuidora'),
                    "cnpj": cnpj
                },
                "customer":{
                    "name":extraction_result.get('titular'),
                    "docType": extraction_result.get('tipo_documento_titular') if extraction_result.get("tipo_documento_titular") != "" else None,
                    "docNumber": extraction_result.get('documento_titular') if extraction_result.get("documento_titular") != "" else None,
                    "address": {
                        "streetAndNumber": address_result.get('rua'),
                        "city": address_result.get('cidade'),
                        "state": address_result.get('estado'),
                        "zipCode": address_result.get('cep'),
                        "district": address_result.get('bairro'),
                    }
                },
                "dates":{
                    "due": extraction_result.get('vencimento'), # Ver se vale formatar para datetime
                    "reading":{
                        "days": int(extraction_result.get('dias_faturados')) if extraction_result.get('dias_faturados') != "" else None
                    }
                },
                "locationNumber":extraction_result.get('uc'),
                "subgroup":(extraction_result.get('subgrupo')),
                "totalCharges":float(extraction_result['valor']) if extraction_result.get("valor") != "" else None,
                "tariffModality":(extraction_result.get('modalidade_tarifaria')).upper(),
                "supply_type" : (extraction_result.get('tipo_fornecimento')).upper(),
                "payment" : {
                    "debts" : True if extraction_result.get("pendencia_pagamento") == "1" else False
                },
                "demand_analysis": {
                    "exceeded_demand" : extraction_result.get("demanda_ultrapassada"),
                    "exceeded_demand_quantity": float(extraction_result.get("qtde_demanda_ultrapassada")) if extraction_result.get("qtde_demanda_ultrapassada") != "" else None
                },
                "energy":{
                    "demand":float(extraction_result.get('demanda')) if extraction_result.get('demanda') != "" else None,
                    "peak":float(extraction_result.get('consumo_ponta')) if extraction_result.get('consumo_ponta') != "" else None,
                    "off-peak":float(extraction_result.get('consumo_fora_ponta')) if extraction_result.get('consumo_fora_ponta') != "" else None,
                    "total": float(extraction_result.get('consumo_total')) if extraction_result.get("consumo_total") != "" else None,
                }
            }
        }
    
    return {
        "transaction":{
            "id": input_data['transaction_id'],
            "client":input_data['response_info']['client'],
            "processed_at":processed_at,
            "reliability": reliability,
            "trust":trust,
            "notes":extraction_result['observacao'],
        },
        "data" : {}
    }



if __name__ == "__main__":

    print(auth_4docs())

    s3_path : str = "staging/95f954f9-a767-415c-bf95-c51ee0340b19-teste-conta-augusto-3.pdf"
    bucket_name : str = "ecom-energy-account-data-extraction"

    # result : dict = enrich_energy_account_with_4docs(bucket_name, s3_path)

    result : dict = {'requestId': 1845476, 'md5sum': '2a6a3f589e8bca29dac4207c05a81c99', 'clientData': {'fatura_id': 123}, 'newStatus': 'SUCCESS', 'whenChanged': '2024-10-21 14:52:27 +0000', 'message': '', 'result': {'version': '2.0', 'md5': '2a6a3f589e8bca29dac4207c05a81c99', 'pipeline': 'energy', 'provider': 'Light', 'providerData': {'name': {'value': 'LIGHT SERVIÇOS DE ELETRICIDADE SA', 'confidence': 'high'}, 'cnpj': {'value': '60444437000146', 'confidence': 'high'}}, 'stdProvider': 'light', 'locationNumber': '430223171', 'class': 'Comercial', 'subclass': 'Comercial', 'subgroup': 'A4', 'group': 'A', 'customer': {'cnpj': '03608600000125', 'name': 'MSA EMPRESA CINEMATOGRAFICALTDA', 'address': {'streetAndNumber': 'RDV METALURGICO 1189C CR', 'city': 'VOLTA REDONDA', 'state': 'RJ', 'zipCode': '27253005', 'district': 'MONTE CASTELO'}}, 'totalCharges': 3346.32, 'tariffModality': 'blue', 'dates': {'due': '2024-08-27T00:00:00', 'month': '2024-07-01T00:00:00', 'reading': {'periodFrom': '2024-06-30T00:00:00', 'periodUntil': '2024-07-31T00:00:00', 'dateRead': '2024-07-31T00:00:00', 'next': '2024-08-31T00:00:00', 'days': 31}}, 'items': [{'type': 'energy', 'kind': 'Gen.', 'period': 'off-peak', 'billed': 40261.0, 'measured': 0, 'rate': 0.34631579, 'charge': 13943.01, 'tusdRate': 0, 'teRate': 0, 'texts': ['Consumo Energia Elétrica HFP'], 'basicRate': 0.2632, 'icmsCharge': 3346.32, 'icmsTaxable': 13943.01, 'icmsRate': 24.0}, {'type': 'tax', 'name': 'ICMS', 'taxable': 13943.01, 'rate': 0.24, 'charge': 3346.32, 'summable': False, 'texts': []}, {'type': 'tax', 'name': 'COFINS', 'summable': False, 'texts': ['COFINS']}, {'type': 'tax', 'name': 'PIS', 'summable': False, 'texts': ['PIS/PASEP']}, {'type': 'thirdPartyEnergy', 'kind': 'Gen.', 'period': 'off-peak', 'billed': -40261.0, 'rate': 0.2632, 'charge': -10596.69, 'measured': 0, 'tusdRate': 0, 'teRate': 0, 'texts': ['Energia Terc Comercializad HFP']}], 'history': {}}}

    # location_number : str = result['result']['locationNumber']


