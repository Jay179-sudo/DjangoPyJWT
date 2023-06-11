from django.db import models

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class MyUserManager(BaseUserManager):
    def create_user(
        self,
        email,
        isSuperAdmin=False,
        isHostelAdmin=False,
        isMessManager=False,
        isStudent=False,
        password=None,
    ):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            isSuperAdmin=isSuperAdmin,
            isHostelAdmin=isHostelAdmin,
            isMessManager=isMessManager,
            isStudent=isStudent,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email,
        isSuperAdmin=False,
        isHostelAdmin=False,
        isMessManager=False,
        isStudent=False,
        password=None,
    ):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            isSuperAdmin=isSuperAdmin,
            isHostelAdmin=isHostelAdmin,
            isMessManager=isMessManager,
            isStudent=isStudent,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    isSuperAdmin = models.BooleanField(default=False)
    isHostelAdmin = models.BooleanField(default=False)
    isMessManager = models.BooleanField(default=False)
    isStudent = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class SuperAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Hostel(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    hostel_code = models.CharField(max_length=5)
    capacity = models.IntegerField()


class HostelAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hostel_supervised = models.ForeignKey(Hostel, on_delete=models.CASCADE)


class MessManager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hostel_catered = models.ForeignKey(Hostel, on_delete=models.CASCADE)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=50, unique=True)
    degree_awarded = models.BooleanField(default=False)
    Hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    Room_Number = models.CharField(max_length=10, blank=True, null=True)


class LeaveRequest(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    Address = models.CharField(max_length=100)
    AdminApproved = models.BooleanField(default=False)
    ReasonForLeave = models.CharField(max_length=100)
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
