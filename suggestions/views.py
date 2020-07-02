from django.http import HttpResponseRedirect
from django.shortcuts import render

from suggestions.models import Suggestion
from .forms import FeedbackForm


def index(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            mobile_number = form.cleaned_data['mobile_number']
            feedback = form.cleaned_data['feedback']

            suggestion = Suggestion(name=name, mobile_number=mobile_number, feedback=feedback)
            suggestion.save()

            return HttpResponseRedirect('/')
    else:
        form = FeedbackForm()
        form['name'].initial = request.user.username

    template_name = 'suggestions/index.html'
    return render(request, template_name, {'form': form})
