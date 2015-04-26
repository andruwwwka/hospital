# -*- coding: utf-8 -*-
import json
from django.http import HttpResponse
from django.shortcuts import render
from main.forms import RegistrationForm
from main.models import Doctor


def index_page(request):
    was_saved = False
    show_message = u''
    if request.method == 'POST':
        if 'new_register' in request.POST:
            form = RegistrationForm()
        else:
            form = RegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                was_saved = True
                show_message = form.message
                form = RegistrationForm()
    else:
        form = RegistrationForm()
    ctx = {
        'show_message': show_message,
        'was_saved': was_saved,
        'form': form
    }
    return render(request, 'index.html', ctx)


def get_doctors(request, spec_id):
    res = {}
    doctors = Doctor.objects.filter(specialization__id=spec_id)
    for doc in doctors:
        res.update({doc.id: doc.full_name})
    return HttpResponse(json.dumps(res),
                        content_type='application/json')