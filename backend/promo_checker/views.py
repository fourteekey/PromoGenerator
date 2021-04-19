from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from . import services


class PromoCheckerAPIView(APIView):
    @swagger_auto_schema(
        description='Get list promocodes by amount',
        manual_parameters=[
            openapi.Parameter('promocode', openapi.IN_QUERY, type='string', description='promocode', required=True)
        ])
    def get(self, request):
        promocode = request.query_params.get('promocode', None)
        if not promocode: return Response({'error': 'Invalid required params.',
                                           'detail': 'В запросе отсуствует обязательные параметры.'},
                                          status=status.HTTP_400_BAD_REQUEST)

        result = services.get_promocode(promocode, path=settings.PATH_JSON_FILE)
        if not result: return Response({'result': 'код не существует'}, status.HTTP_204_NO_CONTENT)

        return Response({'result': f'Промокод \'{result["promocode"]}\' существует. группа = {result["group_name"]}'},
                        status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'amount': openapi.Schema(type=openapi.TYPE_INTEGER),
                'group': openapi.Schema(type=openapi.TYPE_STRING),
            })
    )
    def post(self, request):
        amount = request.data.get('amount', None)
        group = request.data.get('group', None)

        if amount is None or (group is None or group == ''):
            return Response({'error': 'Invalid required data.',
                             'detail': 'В запросе отсуствует обязательные параметры.'},
                            status=status.HTTP_400_BAD_REQUEST)
        elif (not isinstance(amount, str) and not isinstance(amount, int)) \
                or (isinstance(amount, str) and not amount.isdigit()) \
                or int(amount) == 0:
            return Response({'error': 'Invalid amount data.',
                             'detail': 'Значение amount должно быть числом и больше 0.'},
                            status=status.HTTP_400_BAD_REQUEST)


        promocode = services.insert_new_promo(group_name=group, amount=amount, path=settings.PATH_JSON_FILE)
        if not promocode: return Response({'result': 'Не удалось сохранить код. Сбой на сервере.'},
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'promocode': promocode}, status=status.HTTP_201_CREATED)


class PromoGeneratorAPIView(APIView):
    @swagger_auto_schema(description='Generate basa.json with promocodes')
    def post(self, request):
        result = services.generate_base_file(path=settings.PATH_JSON_FILE)
        if not result: return Response(status=status.HTTP_409_CONFLICT)

        return Response()
