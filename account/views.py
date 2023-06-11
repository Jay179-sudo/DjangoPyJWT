from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import (
    SuperAdminSerializer,
    HostelAdminSerializer,
    HostelSerializer,
    MessManagerSerializer,
    SuperAdminLoginSerializer,
    StudentSerializer,
    LeaveSerializer,
    StudentLoginSerializer,
    HostelAdminLoginSerializer,
    MessManagerLoginSerializer,
    UserProfileSerializer,
    UserChangePasswordSerializer,
    SendPasswordResetEmailSerializer,
    UserPasswordResetSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User
from rest_framework.permissions import IsAuthenticated


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class SuperAdminRegister(APIView):
    serializer_class = SuperAdminSerializer

    def post(self, request, format=None):
        serializer = SuperAdminSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response(
                {"token": token, "msg": "Registration successful!"},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"msg": "Registration unsuccessful"}, status=status.HTTP_400_BAD_REQUEST
        )


class HostelAdminRegister(APIView):
    serializer_class = HostelAdminSerializer

    def post(self, request, format=None):
        print(request.query_params)
        serializer = HostelAdminSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"msg": "Hostel Admin registered!"}, status=status.HTTP_201_CREATED
            )
        return Response(
            {"msg": "Registration unsuccessful"}, status=status.HTTP_400_BAD_REQUEST
        )


class HostelRegister(APIView):
    serializer_class = HostelSerializer

    def post(self, request, format=None):
        serializer = HostelSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"msg": "Hostel registered!"}, status=status.HTTP_201_CREATED
            )
        return Response(
            {"msg": "Registration unsuccessful"}, status=status.HTTP_400_BAD_REQUEST
        )


class MessManagerRegister(APIView):
    serializer_class = MessManagerSerializer

    def post(self, request, format=None):
        serializer = MessManagerSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"msg": "Hostel registered!"}, status=status.HTTP_201_CREATED
            )
        return Response(
            {"msg": "Registration unsuccessful"}, status=status.HTTP_400_BAD_REQUEST
        )


class StudentRegister(APIView):
    serializer_class = StudentSerializer

    def post(self, request, format=None):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"msg": "Student registered!"}, status=status.HTTP_201_CREATED
            )
        print("Not")
        return Response(
            {"msg": "Registration unsuccessful"}, status=status.HTTP_400_BAD_REQUEST
        )


class LeaveRegister(APIView):
    serializer_class = LeaveSerializer

    def post(self, request, format=None):
        serializer = LeaveSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"msg": "Leave Request registered!"}, status=status.HTTP_201_CREATED
            )
        return Response(
            {"msg": "Registration unsuccessful"}, status=status.HTTP_400_BAD_REQUEST
        )


# Login View


class SuperAdminLoginView(APIView):
    def post(self, request, format=None):
        serializer = SuperAdminLoginSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.data)
            email = serializer.data.get("email")
            password = serializer.data.get("password")
            user = authenticate(email=email, password=password)
            print(user)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response(
                    {"token": token, "msg": "Login successful!"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "errors": {
                            "non_field_errors": ["Email or password is not Valid"]
                        }
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class HostelAdminLogin(APIView):
    def post(self, request, format=None):
        serializer = HostelAdminLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get("email")
            password = serializer.data.get("password")
            user = authenticate(email=email, password=password)

            # yesto check ni lagau that checks ki hostel admin ho ki nai tyo manche. Super admin bhayera ya ni login garna sakcha btw
            print(user)
            if user is not None:
                return Response({"msg": "Login successful!"}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {
                        "errors": {
                            "non_field_errors": ["Email or password is not Valid"]
                        }
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class MessManagerLogin(APIView):
    def post(self, request, format=None):
        serializer = MessManagerLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get("email")
            password = serializer.data.get("password")
            user = authenticate(email=email, password=password)

            # yesto check ni lagau that checks ki hostel admin ho ki nai tyo manche. Super admin bhayera ya ni login garna sakcha btw
            print(user)
            if user is not None:
                return Response({"msg": "Login successful!"}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {
                        "errors": {
                            "non_field_errors": ["Email or password is not Valid"]
                        }
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class StudentLogin(APIView):
    def post(self, request, format=None):
        serializer = StudentLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get("email")
            password = serializer.data.get("password")
            user = authenticate(email=email, password=password)

            # yesto check ni lagau that checks ki hostel admin ho ki nai tyo manche. Super admin bhayera ya ni login garna sakcha btw
            print(user)
            if user is not None:
                return Response({"msg": "Login successful!"}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {
                        "errors": {
                            "non_field_errors": ["Email or password is not Valid"]
                        }
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


# Profile View


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Change password


class UserChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    # is authetnicated bhaneko token pathau header ma
    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(
            data=request.data,
            context={"user_email": request.user.email, "user_request": request.user},
        )
        if serializer.is_valid(raise_exception=True):
            return Response(
                {"msg": "Password Change Successful!"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendPasswordResetEmail(APIView):
    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(
                {"msg": "Password Reset link sent. Please check your Email"},
                status=status.HTTP_200_OK,
            )
        # raise exception garey bhane no need to send a failure response, but failure response malai better way laagyo ngl


# yo maathi ko change garna lai


class UserPasswordResetView(APIView):
    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(
            data=request.data,
            context={"uid": uid, "token": token, "user_req": self.request.user},
        )
        if serializer.is_valid(raise_exception=True):
            return Response(
                {"msg": "Password Reset successful!"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # id chai user lai identify garna whereas token chai kei hawa request ta aako chaina ni confirm garira.
