from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import MoneyLog
from .forms import MoneyForm
from django.http import HttpResponseRedirect, Http404
from datetime import date
import plotly.express as px
import plotly
import pandas
from datetime import datetime
import math
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
    money_sum = 0
    for i in MoneyLog.objects.filter(owner=request.user).all():
        money_sum += i.money_made


    formatted_date = date.today().strftime("%Y-%m-%d")
    print(formatted_date)
    context = {'moneylogs': moneylogs, 'form': form, 'money_sum': money_sum, 'date_value': formatted_date}
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
    xdata = [i for i in range(len(moneylogs) + 1)]
    # # xdata = [int(time.mktime(datetime.datetime.combine(i.date_added,  my_time).timetuple()) * 1000) for i in moneylogs]
    ydata = []
    for i in range(len(moneylogs) + 1):
        total_sum = 0
        for j in moneylogs[:i]:
            total_sum += j.money_made
        ydata.append(total_sum)

    
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
        margin={'l': 0},
    )
    fig.update_xaxes(gridwidth=.5, gridcolor="LightGrey")
    fig.update_yaxes(gridwidth=.5, gridcolor="LightGrey")
    graph_div = plotly.offline.plot(
        fig, 
        auto_open = False,
        output_type="div", 
        config={'responsive': False, 'staticPlot': True},
    )

    # session average
    money_list = list([i.money_made for i in moneylogs])
    average_per_session = round(sum(money_list)/len(money_list),2 )

    # total money made
    total_money_made = round(sum(money_list), 2)

    # amount made this month
    currentMonth = datetime.now().month
    logs_this_month = list()
    for i in MoneyLog.objects.all():
        if i.date_added.month == currentMonth:
            logs_this_month.append(i)
    money_this_month = [i.money_made for i in logs_this_month]
    money_this_month = round(sum(money_this_month), 2)

    data = {'$/session': average_per_session, '$ total': total_money_made, '$ total this month': money_this_month}

    print('average_per_session ' + str(average_per_session))
    print('money_this_month ' + str(money_this_month))
    print('total_money_made ' + str(total_money_made))
    context = {'graph_div': graph_div, 'data': data}

    return render(request, 'money_data/data.html', context)

from django import template

register = template.Library()


@register.filter(name="abs")
def abs_filter(value):
    return abs(value)