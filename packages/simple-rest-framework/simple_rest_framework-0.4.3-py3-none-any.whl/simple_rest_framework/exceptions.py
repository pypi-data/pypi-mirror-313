from rest_framework.response import Response
from rest_framework import status

class ServiceException(Exception):
    pass


class HandleExceptionsMixin:
    def handle_exceptions(self, func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)

            except ServiceException as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return wrapper

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if hasattr(self, 'get'):
            self.get = self.handle_exceptions(self.get)

        if hasattr(self, 'post'):
            self.post = self.handle_exceptions(self.post)

        if hasattr(self, 'put'):
            self.put = self.handle_exceptions(self.put)

        if hasattr(self, 'delete'):
            self.delete = self.handle_exceptions(self.delete)