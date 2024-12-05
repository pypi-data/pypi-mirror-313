import pytest
import unittest
import os

from ecom_data_helpers.energy_account_extraction import format_response


class TestEcomDataHelpersEnergyAccountExtraction(unittest.TestCase):

    def setUp(self):

        self.prompt_response : dict = {
            "transaction_id": "1d2b4328-a677-4361-b23c-e1f0bec4094f",
            "s3_key": "staging/1d2b4328-a677-4361-b23c-e1f0bec4094f-teste.pdf",
            "processed_at": "2024-10-02 17:53:30.559706",
            "client": "augusto.lorencatto",
            "webhook_url": "https://637b7e45-b905-4ffe-938b-b3236d0e49c3.mock.pstmn.io/echo",
            "webhook_auth_token": "123213213213213213213213213213123",
            "result": {
                "nome_distribuidora": "ENEL SP",
                "cnpj_distribuidora": "61695227000193",
                "resultado_distribuidora": "61695227000193",
                "titular": "FACULDADES METROPOLITANAS UNIDAS EDUCACI",
                "endereco": "{'rua': 'AV LIBERDADE', 'numero': '747', 'bairro': 'LIBERDADE', 'cidade': 'SAO PAULO', 'estado': 'SP', 'cep': '01503-001'}",
                "uc": "10001144",
                "vencimento": "05/08/2024",
                "dias_faturados": "30",
                "subgrupo": "A4",
                "modalidade_tarifaria": "VERDE",
                "tipo_fornecimento": "TRIFASICO",
                "valor": "17723.85",
                "demanda": "390.00",
                "consumo_ponta": "10445.28",
                "consumo_fora_ponta": "39895.20",
                "consumo_total": "50340.48",
                "pendencia_pagamento": "0",
                "demanda_ultrapassada": False,
                "qtde_demanda_ultrapassada":"",
                "observacao": "O endereço de instalação difere do endereço de correspondência. A extração foi feita com base no endereço de correspondência.",
                "inferencia_subgrupo": "0",
                "confiabilidade": "95"
            }
        }

    def test_zfill_function_with_cnpj(self):
        int_cnpj : str = "6981180000116"
        assert int_cnpj.zfill(14) == "06981180000116"


    def test_format_response_with_sucess(self):

        transaction_id : str = self.prompt_response['transaction_id']

        response : dict = format_response(
            input_data={
                "transaction_id":transaction_id,
                "response_info" : {
                    "client": self.prompt_response['client']
                }
            },
            result=self.prompt_response['result'],
            processed_at=self.prompt_response['processed_at']
        )

        assert response['transaction']['id'] == transaction_id


        assert type(response['data']['providerData']['cnpj']) == str
        assert response['data']['providerData']['cnpj'] == "61695227000193"


if __name__ == "__main__":
    unittest.main()