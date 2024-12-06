from rest_framework.views import APIView
from rest_framework.response import Response

from .services import BaseService
from .exceptions import HandleExceptionsMixin

def parse_request_data(request):
    data = request.data.copy()
    parsed_data = {}

    for key in data:
        if isinstance(data[key], list):
            parsed_data[key] = data[key][0]
        else:
            parsed_data[key] = data[key]

    return parsed_data

class BaseView(HandleExceptionsMixin, APIView, BaseService): pass

class BaseUtilView(HandleExceptionsMixin, APIView, BaseService):
    def get(self, request):
        return Response({
            "mensaje": "Utilizando la API de Simple Rest Framework.",
            "data": {
                "create_fields": self.create_fields,
                "update_fields": self.update_fields,
                "serialize_fields": self.serialize_fields,
                "filter_fields": self.filter_fields,
                "foreign_fields": self.foreign_fields
                }
            })

class BaseSearchView(HandleExceptionsMixin, APIView, BaseService):
    def get(self, request):
        objetos = self.listar()

        return Response({
            "mensaje": f"Se encontraron {len(objetos)} {self.modelo._meta.verbose_name_plural.lower()}.",
            "data": objetos
            })

    def post(self, request):
        data = request.data

        objetos = self.listar(**data)

        return Response({
            "mensaje": f"Se encontraron {len(objetos)} {self.modelo._meta.verbose_name_plural.lower()}.",
            "data": objetos
            })

class BaseABMView(HandleExceptionsMixin, APIView, BaseService):
    def get(self, request, id):
        self.set_objeto(id)

        return Response(self.get_serializado())

    def post(self, request):
        data = request.data

        if  'multipart/form-data' in request.content_type:
            data = parse_request_data(request)

        self.crear(**data)

        return Response({
            "mensaje": f"{self.modelo._meta.verbose_name.lower()} creado con éxito.",
            "data": self.get_serializado()
            })

    def put(self, request):
        data = request.data

        if  'multipart/form-data' in request.content_type:
            data = parse_request_data(request)

        objeto_id = data.get('id')
        self.set_objeto(objeto_id)

        self.actualizar(**data)

        return Response({
            "mensaje": f"{self.modelo._meta.verbose_name.lower()} actualizado con éxito.",
            "data": self.get_serializado()
            })

    def delete(self, request):
        objeto_id = request.data.get('id')
        self.set_objeto(objeto_id)
        self.eliminar()

        return Response({
            "mensaje": f"{self.modelo._meta.verbose_name.lower()} eliminado con éxito."
            })
    