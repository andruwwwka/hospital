# -*- coding: utf-8 -*-
from django import forms
from django.contrib.admin.widgets import AdminDateWidget
import datetime
from main.models import Doctor, Specialization, Patient, Visit


class RegistrationForm(forms.Form):
    surname = forms.CharField(
        label=u'Фамилия',
        required=True
    )
    name = forms.CharField(
        label=u'Имя',
        required=True
    )
    patronymic = forms.CharField(
        label=u'Отчество',
        required=True
    )
    specialization = forms.ModelChoiceField(
        label=u'Специализация',
        queryset=()
    )
    doctor = forms.ModelChoiceField(
        label=u'Доктор',
        queryset=Doctor.objects.none(),
    )
    register_date = forms.DateField(
        label=u'Дата посещения',
        required=True,
        widget=AdminDateWidget
    )
    time = forms.ChoiceField(
        label=u'Время посещения',
        required=True,
        choices=[(item, '%s:00' % item) for item in range(9, 18)]
    )

    def __init__(self, *args):
        super(RegistrationForm, self).__init__(*args)
        spec_values = Doctor.objects.all().values('specialization').distinct()
        self.fields['specialization'].queryset = Specialization.objects.filter(id__in=spec_values)

    def is_valid(self):
        super(RegistrationForm, self).is_valid()
        for key in list(self.errors):
            if key != 'doctor':
                self._errors[self.fields[key].label] = self.error_class([self.errors[key]])
            del self.errors[key]
        if not self.errors:
            doctor = Doctor.objects.get(id=self.data['doctor'])
            hour = self.cleaned_data['time']
            v_date = datetime.datetime.combine(self.cleaned_data['register_date'], datetime.time(int(hour)))
            if self.cleaned_data['register_date'] < datetime.datetime.now().date():
                self._errors[self.fields['register_date'].label] = self.error_class([u'Вы выбрали прошедшую дату. '
                                                                                     u'Выберите другой день'])
            if v_date.weekday() > 4:
                self._errors[self.fields['register_date'].label] = self.error_class([u'Невозможно записаться на '
                                                                                     u'выходной день. Выберите '
                                                                                     u'рабочий день'])
            if Visit.objects.filter(doctor=doctor, visit_date=v_date).exists():
                start_date = datetime.datetime.combine(self.cleaned_data['register_date'], datetime.time(9))
                end_date = datetime.datetime.combine(self.cleaned_data['register_date'], datetime.time(17))
                date_values = Visit.objects.filter(doctor=doctor, visit_date__gte=start_date, visit_date__lte=end_date).values('visit_date')
                busy_hours = [item['visit_date'].time().hour+3 for item in date_values]
                if len(busy_hours) < 9:
                    available_hours = [item for item in range(9, 18) if item not in busy_hours]
                    self._errors[self.fields['time'].label] = self.error_class([u'Данное время занято, '
                                                                                u'пожалуйста, выберите значение '
                                                                                u'из %s' % ', '.join(['%s:00' % item for item in available_hours ])])
                else:
                    self._errors[self.fields['time'].label] = self.error_class([u'На данную дату нет свободных часов. '
                                                                                u'Выберите другую дату'])
        if self.errors:
            return False
        return True

    def save(self):
        patient = Patient(
            name=self.cleaned_data['name'],
            surname=self.cleaned_data['surname'],
            patronymic=self.cleaned_data['patronymic']
        )
        patient.save()
        doctor = Doctor.objects.get(id=self.data['doctor'])
        hour = self.cleaned_data['time']
        v_date = datetime.datetime.combine(self.cleaned_data['register_date'], datetime.time(int(hour)))
        Visit(
            patient=patient,
            doctor=doctor,
            visit_date=v_date
        ).save()
        self.message = u'%s %s ждет вам на прием %s' % (doctor.specialization.name, doctor.full_name, v_date)

