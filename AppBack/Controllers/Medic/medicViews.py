from rest_framework import generics, permissions, status
from rest_framework.response import Response

from AppBack.models import Account, User

from .serializer import MedicAccountSerializer, MedicSerializer


class GetMedic(generics.RetrieveAPIView):
    serializer_class = MedicAccountSerializer
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.filter(user_type="Medico")


class GetAllMedics(generics.ListAPIView):
    serializer_class = MedicAccountSerializer
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.filter(user_type="Medico").all()


class CreateMedic(generics.CreateAPIView):
    serializer_class = MedicSerializer
    permission_classes = [permissions.AllowAny]
    model = User

    """
    def post(self, request):
        account = Account.objects.get(user_id = request.data['user_id'])
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            serializer.save(user_id = account)
            return Response({'message': 'Se creo correctamente',
                    'data': serializer.data }, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    """

    def post(self, request):
        try:
            account = Account.objects.create(
                user_id=request.data["user_id"],
                user_type=request.data["user_type"],
                password=request.data["password"],
                email=request.data["email"],
                user_status=request.data["user_status"],
            )

            account.save()

            user = User.objects.create(
                user_id=account,
                user_type=request.data["user_type"],
                name=request.data["name"],
                last_name=request.data["last_name"],
                city=request.data["city"],
            )

            user.save()

            return Response(
                {"message": "Se creo correctamente"}, status=status.HTTP_201_CREATED
            )
        except Exception:
            return Response(
                {"message": "Error al crear usuario"},
                status=status.HTTP_400_BAD_REQUEST,
            )
