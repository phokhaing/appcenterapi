from datetime import datetime
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.utils import timezone

# from django.contrib.auth.models import User

from ..branch.models import Branch
from ..department.models import Department
from ..position.models import Position


class UserManager(BaseUserManager):
    def _create_user(
        self,
        username,
        email,
        password,
        is_active,
        is_staff,
        is_superuser,
        **extra_fields,
    ):
        if not username:
            raise ValueError("The given username is not valid")

        now = datetime.now()
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            is_active=is_active,
            is_staff=is_staff,
            is_superuser=is_superuser,
            date_joined=now,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password, **extra_fields):
        return self._create_user(
            username,
            email,
            password,
            is_active=True,
            is_staff=True,
            is_superuser=False,
            **extra_fields,
        )

    def create_superuser(self, username, email, password, **extra_fields):
        user = self._create_user(
            username,
            email,
            password,
            is_active=True,
            is_staff=True,
            is_superuser=True,
            **extra_fields,
        )
        user.save(using=self._db)
        return user


class Permission(models.Model):
    permission_name = models.CharField(max_length=100, null=False, unique=True)
    description = models.TextField(blank=True, max_length=500)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.permission_name) if self.permission_name else ''

    class Meta:
        db_table = "ftb_permission"
        managed = True
        verbose_name = "Permission"
        verbose_name_plural = "07. Permissions"


class Module(models.Model):
    module_name = models.CharField(max_length=255, null=False, unique=True)
    path = models.CharField(max_length=255, null=False, unique=True)
    status = models.BooleanField(default=True)
    # permissions = models.ManyToManyField(Permission, related_name='modules')  # module_permissions many to many relationship
    permissions = models.ManyToManyField(
        Permission, through='ModulePermission', related_name='modules')

    def __str__(self):
        return str(self.module_name) if self.module_name else ''

    class Meta:
        db_table = 'ftb_module'
        managed = True
        verbose_name = 'Module'
        verbose_name_plural = "05. Modules"


class Role(models.Model):
    role_name_en = models.CharField(max_length=100, null=False, unique=True)
    role_name_kh = models.CharField(max_length=100, null=False, unique=True)
    description = models.TextField(blank=True, max_length=500)
    is_active = models.BooleanField(default=True)
    # modules = models.ManyToManyField(Module, related_name='roles')  # role_modules many to many relationship
    modules = models.ManyToManyField(
        Module, through='RoleModule', related_name='roles')

    def __str__(self):
        return str(self.role_name_en) if self.role_name_en else ''

    class Meta:
        db_table = "ftb_role"
        managed = True
        verbose_name = "Role"
        verbose_name_plural = "02. Roles"


class ModulePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.module) if self.module else ''

    class Meta:
        db_table = 'ftb_module_permissions'
        managed = True
        verbose_name = "Module permission"
        verbose_name_plural = "06. Module permissions"


class User(AbstractBaseUser, PermissionsMixin):
    # staff_id = models.CharField(unique=True, max_length=255)
    # email = models.EmailField(max_length=250, unique=True)

    staff_id = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=250)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    first_name_kh = models.CharField(max_length=255, blank=True, null=True)
    last_name_kh = models.CharField(max_length=255, blank=True, null=True)
    photo = models.ImageField(
        default='profile1.png', upload_to='images/profile/', null=True, blank=True)
    GENDER_CHOICES = (("M", "Male"), ("F", "Female"), ("O", "Others"))
    gender = models.CharField(
        choices=GENDER_CHOICES, max_length=1, null=True, blank=True
    )
    # date_of_birth = models.DateTimeField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    ext = models.CharField(max_length=25, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    # date_joined = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    date_joined = models.DateField(null=True, blank=True)
    pc_id = models.CharField(max_length=255, null=True, blank=True)
    # ip_address = models.GenericIPAddressField(unique=True, null=True, blank=True)
    ip_address = models.CharField(max_length=255, null=True, blank=True)
    email_notification = models.BooleanField(default=True)
    online_timestamp = models.CharField(max_length=255, null=True, blank=True)
    noti_count = models.IntegerField(default=0, null=True, blank=True)
    position = models.ForeignKey(
        Position, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True)
    branch = models.ForeignKey(
        Branch, on_delete=models.SET_NULL, null=True, blank=True)
    manager = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True)
    # roles = models.ManyToManyField(Role, related_name="users") # user_roles many to many relationship
    roles = models.ManyToManyField(
        Role, through='UserRole', related_name='users')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name="created_by_user")
    updated_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name="updated_by_user")

    objects = UserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = [
        "email",
    ]

    @property
    def fullname(self):
        return f"{self.last_name} {self.first_name}"

    def __unicode__(self):
        return self.staff_id

    class Meta:
        db_table = "ftb_user"
        managed = True
        verbose_name = "User"
        verbose_name_plural = "01. Users"


class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user) if self.user else ''

    class Meta:
        db_table = 'ftb_user_roles'
        managed = True
        verbose_name = "User role"
        verbose_name_plural = "03. User roles"


class RoleModule(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL,
                                   related_name='%(class)s_created_by', blank=True, null=True, db_column='created_by')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL,
                                   related_name="%(class)s_updated_by", blank=True, null=True, db_column="updated_by")

    def __str__(self):
        return str(self.role) if self.role else ''

    class Meta:
        db_table = 'ftb_role_modules'
        managed = True
        verbose_name = "Role module"
        verbose_name_plural = "04. Roles modules"


# Auto create user auth token when user created
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def GenerateToken(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class UserAvatar(models.Model):
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, db_column="user_id", related_name='attachment_files')
    upload_file_name = models.CharField(max_length=500, blank=True, null=True)
    original_name = models.CharField(max_length=500, blank=True, null=True)
    file_type = models.CharField(max_length=255, blank=True, null=True)
    extension = models.CharField(max_length=12, blank=True, null=True)
    file_size = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.IntegerField(blank=True, null=True)
    file_path = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.BooleanField(blank=True, null=True, default=True)

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="%(class)s_created_by",
        blank=True,
        null=True,
        db_column="created_by",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="%(class)s_updated_by",
        blank=True,
        null=True,
        db_column="updated_by",
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ftb_user_avatar"
        verbose_name = "User avatar"
        verbose_name_plural = "08. User avatars"
        managed = True


class GroupsUser(models.Model):
    title = models.CharField(max_length=500, null=False, unique=True)
    hook = models.CharField(max_length=500, null=False, unique=True)
    status = models.BooleanField(default=True)

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="%(class)s_created_by",
        blank=True,
        null=True,
        db_column="created_by",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="%(class)s_updated_by",
        blank=True,
        null=True,
        db_column="updated_by",
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id) if self.id else ''

    class Meta:
        db_table = "ftb_groups_user"
        verbose_name = "Groups User"
        verbose_name_plural = "09. Groups User"
        managed = True


class GroupMembership(models.Model):
    group_id = models.ForeignKey(
        GroupsUser,
        on_delete=models.CASCADE,
        db_column='group_id',
        related_name='group_id'
    )

    user_id = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='%(class)s_user_id',
        null=True,
        db_column='user_id',
        # related_name='user_memberships',
    )
    status = models.BooleanField(default=True)

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="%(class)s_created_by",
        blank=True,
        null=True,
        db_column="created_by",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="%(class)s_updated_by",
        blank=True,
        null=True,
        db_column="updated_by",
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ftb_group_membership"
        verbose_name = "Group Membership"
        verbose_name_plural = "10. Group Membership"
        managed = True
