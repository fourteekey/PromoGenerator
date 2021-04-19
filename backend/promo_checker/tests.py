from rest_framework import status
from rest_framework.test import APITestCase


class CreatePromocodesCase(APITestCase):
    def test_2_checker(self):
        print('Start test manager')
        response = self.client.get("/api/v1/promo?promocode=manager")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(f'Response: {response.data}')
        self.assertEqual(response.data, {'result': f'Промокод \'manager\' существует. группа = Wheat'})
        print('# Test "manager": OK')

    def test_empty_promo_checker(self):
        print('Start test "empty promo"')
        response = self.client.get("/api/v1/promo?promocode=invalid_promo")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, {'result': 'код не существует'})
        print('# Test "empty promo": OK')

    def test_invalid_params_checker(self):
        print('Start test "invalid params"')
        response = self.client.get("/api/v1/promo?pramacode=invalid_promo")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Invalid required params.', 'detail': 'В запросе отсуствует обязательные параметры.'})
        print('# Test invalid params: OK!')

    def test_check_create_promo(self):
        print('Start test "create promo"')
        data = {"amount": 1, "group": 1}
        response = self.client.post("/api/v1/promo", data=data)
        promocode = response.data.get('promocode', None)

        if not promocode: raise AttributeError

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(f"/api/v1/promo?promocode={promocode}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'result': f'Промокод \'{promocode}\' существует. группа = {data["group"]}'})
        print(f'# Test create promo: OK! New promo = {promocode}.')
