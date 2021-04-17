from rest_framework import status
from rest_framework.test import APITestCase


class CreatePromocodesCase(APITestCase):
    def test_1_generator(self):
        response = self.client.post("/api/v1/promo/generate")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print('# Test generator: OK')

    def test_2_checker(self):
        response = self.client.get("/api/v1/promo?promocode=manager")
        print('Result by promocode manager: ', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print('# Test success checker: OK')

    def test_empty_promo_checker(self):
        response = self.client.get("/api/v1/promo?promocode=invalid_promo")
        print('Result by promocode empty_promo: ', response.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        print('# Test empty promo params: OK!')

    def test_invalid_params_checker(self):
        response = self.client.get("/api/v1/promo?pramacode=invalid_promo")
        print('Result by pramacode: ', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print('# Test invalid params: OK!')

    def test_check_create_promo(self):
        data = {"amount": 1, "group": 0}
        response = self.client.post("/api/v1/promo", data=data)
        promocode = response.data.get('promocode', None)
        if not promocode: raise AttributeError

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(f"/api/v1/promo?promocode={promocode}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(f'# Test create promo: OK! New promo = {promocode}.')
