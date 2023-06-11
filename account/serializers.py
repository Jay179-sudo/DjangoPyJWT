from rest_framework import serializers
from account.models import (
    User,
    SuperAdmin,
    HostelAdmin,
    Hostel,
    MessManager,
    Student,
    LeaveRequest,
)
from .utils import Util

# send password reset emails
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class SuperAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "password",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        superAdmin = SuperAdmin(user=user)
        superAdmin.save()

        return user


class SuperAdminLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField()

    def validate(self, attrs):
        return attrs


class HostelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hostel
        fields = "__all__"


class HostelAdminSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField()
    hostel_supervised = serializers.IntegerField()

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        hostel_supervised_id = validated_data.pop("hostel_supervised")
        user = User.objects.create_user(**validated_data)
        hostel_supervised = Hostel.objects.get(pk=hostel_supervised_id)
        hostelAdmin = HostelAdmin(user=user, hostel_supervised=hostel_supervised)
        hostelAdmin.save()

        return user


class HostelAdminLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField()

    def validate(self, attrs):
        return attrs


class MessManagerSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField()
    hostel_catered = serializers.IntegerField()

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        hostel_supervised_id = validated_data.pop("hostel_catered")
        user = User.objects.create_user(**validated_data)
        hostel_supervised = Hostel.objects.get(pk=hostel_supervised_id)
        hostelAdmin = MessManager(user=user, hostel_catered=hostel_supervised)
        hostelAdmin.save()

        return user


class MessManagerLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField()

    def validate(self, attrs):
        return attrs


class StudentSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField()
    name = serializers.CharField(max_length=100)
    roll_number = serializers.CharField(max_length=50)
    Hostel = serializers.IntegerField()
    Room_Number = serializers.CharField(max_length=10)

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        print("shfsd")
        hostel_supervised_id = validated_data.pop("Hostel")
        name = validated_data.pop("name")
        roll_number = validated_data.pop("roll_number")
        Room_Number = validated_data.pop("Room_Number")

        user = User.objects.create_user(**validated_data)
        hostel_supervised = Hostel.objects.get(pk=hostel_supervised_id)

        student = Student(
            user=user,
            name=name,
            roll_number=roll_number,
            degree_awarded=False,
            Room_Number=Room_Number,
            Hostel=hostel_supervised,
        )
        student.save()

        return user


class StudentLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField()

    def validate(self, attrs):
        return attrs


class LeaveSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    Address = serializers.CharField(max_length=100)
    AdminApproved = serializers.BooleanField(default=False)
    ReasonForLeave = serializers.CharField(max_length=100)
    hostel = serializers.IntegerField()

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        email = validated_data.pop("email")
        password = validated_data.pop("password")
        start_date = validated_data.pop("start_date")
        end_date = validated_data.pop("end_date")
        Address = validated_data.pop("Address")
        AdminApproved = validated_data.pop("AdminApproved")
        ReasonForLeave = validated_data.pop("ReasonForLeave")
        hostel = validated_data.pop("hostel")

        user = User.objects.get(email=email, password=password)
        student = Student.objects.get(user=user)
        hostel = Hostel.objects.get(pk=hostel)
        Leave = LeaveRequest(
            student=student,
            start_date=start_date,
            end_date=end_date,
            Address=Address,
            AdminApproved=AdminApproved,
            ReasonForLeave=ReasonForLeave,
            hostel=hostel,
        )
        Leave.save()

        return user


# User Profile Serializer


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email"]


# Change password


class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )
    password2 = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )

    def validate(self, attrs):
        email = self.context.get("user_email")
        user_req = self.context.get("user_request")
        password = attrs.get("password")
        password2 = attrs.get("password2")
        user = User.objects.get(email=email)
        # if user_req != user:
        #     raise serializers.ValidationError("Password does not match")
        success = user.check_password(raw_password=password)
        if success:
            user.set_password(password2)
            user.save()
            return attrs
        else:
            raise serializers.ValidationError("Password does not match")


# Password Reset Emails


class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ["email"]

    def validate(self, attrs):
        email = attrs.get("email")
        if User.objects.filter(email=email).exists():
            # email pathau yeta

            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print("Encoded UID", uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print("Password Reset Token", token)
            link = "http://localhost:3000/api/user/reset/" + uid + "/" + token
            print("Password Reset Link", link)

            # send email
            body = "Click the following link to reset your password " + link
            # data variable ma subject, body, ... diney
            data = {
                "subject": "Rest Your Password",
                "body": body,
                "to_email": user.email,
            }
            Util.send_email(data)

            return attrs
        else:
            raise serializers.ValidationError("You are not a registered user!")


class UserPasswordResetSerializer(serializers.Serializer):
    # same chaapdeko ho maile tyo password change serializer bata
    password = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )

    def validate(self, attrs):
        try:
            user_req = self.context.get("user_request")
            password = attrs.get("password")

            uid = self.context.get("uid")
            token = self.context.get("token")

            # id nikalam user ko
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)

            # aaba token check garne. Token thik cha ki nai check garnu paryo
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError(
                    "Access Denied! Invalid or expired token"
                )

            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError("Access Denied! Invalid or expired token")
