# -*- coding: utf-8 -*-
from django.db import models


DOCTOR_CATEGORY = (
    (1, u'Первая'),
    (2, u'Вторая'),
    (3, u'Высшая'),
)


class Person(models.Model):
    name = models.CharField(
        u'Имя',
        max_length=31
    )
    surname = models.CharField(
        u'Фамилия',
        max_length=31
    )
    patronymic = models.CharField(
        u'Отчество',
        max_length=31
    )

    class Meta:
        abstract = True

    @property
    def full_name(self):
        return u'%s %s %s' % (self.surname, self.name, self.patronymic)

    def __str__(self):
        return self.full_name


class Patient(Person):
    pass


class Specialization(models.Model):
    name = models.CharField(
        u'Название специальности',
        max_length=63,
        unique=True
    )

    class Meta:
        verbose_name = u'Специализация'
        verbose_name_plural = u'Специализации'

    def __str__(self):
        return self.name


class Doctor(Person):
    specialization = models.ForeignKey(
        Specialization,
        verbose_name=u'Специализация'
    )
    category = models.IntegerField(
        u'Категория',
        choices=DOCTOR_CATEGORY
    )

    class Meta:
        verbose_name = u'Доктор'
        verbose_name_plural = u'Доктора'
        unique_together = [
            'name',
            'surname',
            'patronymic',
            'specialization'
        ]

    def __str__(self):
        return u'%s %s %s - %s' % (self.surname, self.name, self.patronymic, self.specialization.name)


class Visit(models.Model):
    patient = models.ForeignKey(
        Patient,
        verbose_name=u'Пациент'
    )
    doctor = models.ForeignKey(
        Doctor,
        verbose_name=u'Доктор'
    )
    visit_date = models.DateTimeField(
        u'Дата приема'
    )

    class Meta:
        verbose_name = u'Посещение'
        verbose_name_plural = u'Посещения'
        unique_together = [
            'doctor',
            'visit_date'
        ]