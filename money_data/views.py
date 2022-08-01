from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import MoneyLog
from .forms import MoneyForm
from django.http import HttpResponseRedirect, Http404
from datetime import date
import random
import plotly.express as px
import plotly
import pandas
# Create your views here.

def index(request):
    return render(request, 'money_data/index.html')

@login_required
def money(request):
    moneylogs = MoneyLog.objects.filter(owner=request.user).order_by('-date_added')

    # render and process add form
    if request.method != 'POST':
        form = MoneyForm({'date_added': date.today()})
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
    if log.owner != request.user:
        raise Http404
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

@login_required
def line_chart(request):
    moneylogs = MoneyLog.objects.filter(owner=request.user).order_by('date_added')
    # nb_element = len(moneylogs)
    # xdata = range(nb_element)
    xdata = [i for i in range(len(moneylogs))]
    # # xdata = [int(time.mktime(datetime.datetime.combine(i.date_added,  my_time).timetuple()) * 1000) for i in moneylogs]
    ydata = []
    for i in range(len(moneylogs)):
        sum = 0
        for j in moneylogs[:i]:
            sum += j.money_made
        ydata.append(sum)

    
    df = pandas.DataFrame(dict(x=xdata, y=ydata))
    fig = px.line(
        df, 
        x="x", 
        y="y", 
        markers=True, 
        labels=dict(x="session #", y="total money"), 
        title='Earnings',
    )
    fig.update_layout(
        xaxis=dict(
            tickmode='linear',
        ),
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(255, 255, 255)',
    )
    fig.update_xaxes(gridwidth=.5, gridcolor="LightGrey")
    fig.update_yaxes(gridwidth=.5, gridcolor="LightGrey")
    graph_div = plotly.offline.plot(
        fig, 
        auto_open = False,
        output_type="div", 
        config={'responsive': False, 'staticPlot': True}
    )

    context = {'graph_div': graph_div}

    return render(request, 'money_data/data.html', context)