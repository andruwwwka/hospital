# -*- coding: utf-8 -*-
from django.contrib import admin

from main.models import Visit, Specialization, Doctor


class FilterBase(admin.SimpleListFilter):
    def queryset(self, request, queryset):
        if self.value():
            dictionary = dict(((self.parameter_name, self.value()),))
            return queryset.filter(**dictionary)


class DoctorFilter(FilterBase):
    title = 'Доктор'
    parameter_name = 'doctor_id'

    def lookups(self, request, model_admin):
        return tuple((d.id, d.full_name)
                     for d in Doctor.objects.filter(pk__in=
                                                    Visit.objects.values_list('doctor').distinct())
        )


class VisitAdmin(admin.ModelAdmin):

    def doctor_name(self, obj):
        return obj.doctor.full_name
    doctor_name.short_description = u'Доктор'

    def patient_name(self, obj):
        return obj.patient.full_name
    patient_name.short_description = u'Пациент'

    list_display = (
        'doctor_name',
        'visit_date',
        'patient_name',
    )

    ordering = ('doctor__surname', 'visit_date')

    list_filter = [
        DoctorFilter,
    ]


admin.site.register(Specialization)
admin.site.register(Visit, VisitAdmin)
admin.site.register(Doctor)