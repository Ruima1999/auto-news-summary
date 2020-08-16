from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.shortcuts import render

from .models import email
from .forms import emailForm


class ResultsView(generic.TemplateView):
    template_name = 'results.html'

def addemail(request):
    if request.method == "POST":
        form = emailForm(request.POST, request.FILES)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.save()
            return HttpResponseRedirect('/results')
    else:
        form = emailForm()
        return render(request, 'index.html', {'form': form})