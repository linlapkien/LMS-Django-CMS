"""
Django admin customizations
"""
from django.contrib import admin # noqa
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin # noqa
from django.utils.translation import gettext_lazy as _ # noqa

""" import all the custome models that we want to register in django admin"""
from core import models # noqa


class UserAdmin(BaseUserAdmin):
    """ Define the admin pages for users. """
    ordering = ['id']
    list_display = ['email', 'name', 'phone_number', 'created_at', 'updated_at']

    """ Fieldsets is a tuple. """
    """ None is the title of the section. """
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'phone_number', 'role_id')}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Important dates'), {'fields': ('last_login', 'created_at', 'updated_at')})
    )
    readonly_fields = ['last_login', 'created_at', 'updated_at']

    """ Add fieldsets for creating user. """
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'phone_number',
                'role_id',
                'is_active',
                'is_staff',
                'is_superuser'
            ),
        }),
    )

class RoleAdmin(admin.ModelAdmin):
    """ Define the admin pages for roles. """
    ordering = ['id']
    list_display = ('name', 'description')
    search_fields = ('name',)

    """ Fieldsets is a tuple. """
    fieldsets = (
        (None, {
            "fields": (
                'name',
                'description',
            ),
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'name',
                'description',
            ),
        }),
    )

class LessonAdmin(admin.ModelAdmin):
    """ Define the admin pages for lessons. """
    ordering = ['id']
    list_display = ('title', 'course', 'content_type', 'order', 'created_at')
    list_filter = ('content_type',)
    search_fields = ('title', 'course__title')


class CourseAdmin(admin.ModelAdmin):
    """ Define the admin pages for courses. """
    list_display = ('title', 'instructor', 'price', 'status', 'created_at', 'end_at')
    list_filter = ('status',)
    search_fields = ('title', 'instructor__email')
    ordering = ('-created_at',)


class EnrollmentAdmin(admin.ModelAdmin):
    """ Define the admin pages for enrollments. """
    list_display = ('user', 'course', 'status', 'enrolled_at', 'end_at')
    list_filter = ('status',)
    search_fields = ('user__email', 'course__title')
    ordering = ('-enrolled_at',)


class PaymentAdmin(admin.ModelAdmin):
    """ Define the admin pages for payments. """
    list_display = ('user', 'course', 'price', 'status', 'transaction_date', 'updated_at')
    list_filter = ('status',)
    search_fields = ('user__email', 'course__title')
    ordering = ('-transaction_date',)


class ListOfUserCourseAdmin(admin.ModelAdmin):
    """ Define the admin pages for list of user courses. """
    list_display = ('user', 'course', 'created_at')
    search_fields = ('user__email', 'course__title')
    ordering = ('-created_at',)


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Role, RoleAdmin)
admin.site.register(models.Course, CourseAdmin)
admin.site.register(models.Lesson, LessonAdmin)
admin.site.register(models.Enrollment, EnrollmentAdmin)
admin.site.register(models.Payment, PaymentAdmin)
admin.site.register(models.ListOfUserCourse, ListOfUserCourseAdmin)
