from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import MoneyLog
from .forms import MoneyForm
from django.http import HttpResponseRedirect, Http404

# Create your views here.

def index(request):
    return render(request, 'money_data/index.html')

@login_required
def money(request):
    moneylogs = MoneyLog.objects.filter(owner=request.user).order_by('date_added')

    # render and process add form
    if request.method != 'POST': 
        form = MoneyForm
    else:
        form = MoneyForm(data=request.POST)
        if form.is_valid():
            new_log = form.save(commit=False)
            new_log.owner = request.user
            new_log.save()
            return HttpResponseRedirect(reverse('money_data:moneylogs'))

    # show total loss/profit
    sum = 0
    for i in MoneyLog.objects.filter(owner=request.user).all():
        sum += i.money_made

    context = {'moneylogs': moneylogs, 'form': form, 'money_sum': sum}
    return render(request, 'money_data/moneylogs.html', context)

def delete_log(request, log_id):
    log = MoneyLog.objects.get(id=log_id)
    log.delete()
    return HttpResponseRedirect(reverse('money_data:moneylogs'))

def edit_log(request, log_id):
    log = MoneyLog.objects.get(id=log_id)
    if log.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = MoneyForm(instance=log)
    else:
        form = MoneyForm(instance=log, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('money_data:moneylogs'))

    context = { 'log': log, 'form': form }
    return render(request, 'money_data/edit_log.html', context)