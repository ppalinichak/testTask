from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, InputOptionsForm
import requests
from datetime import date, timedelta
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Ваш аккаунт создан: можно войти на сайт.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def get_data(start_day, finish_day, campaign_id, buyer_id):
    headers = {
        'accept': 'application/json',
        'Api-Key': '',
    }

    json_data = {
        'range': {
            'from': '{}T21:00:00.000Z'.format(start_day),
            'to': '{}T20:59:59.999Z'.format(finish_day),
            'timezone': 'Europe/Istanbul',
        },
        'grouping': [
            'campaign'
        ],
        'metrics': [
            'clicks',
            'conversions'
        ],
        'filters': [
            {"name": "sub_id_6","operator":"EQUALS","expression":buyer_id},
            {"name": "campaign_id", "operator": "EQUALS", "expression": campaign_id}
        ],
        'sort':[
            {'name' : 'campaign_id',
             'order': 'asc'}
        ]
    }

    response = requests.post('http:///admin_api/v1/report/build', headers=headers, json=json_data)
    try:
        return response.json()['rows'][0]['clicks'], response.json()['rows'][0]['conversions']
    except: return ['0', '0']


@login_required
def profile(request):
    print(date.today())
    start_day = date.today() - timedelta(days=1)
    stop_day  = date.today()
    campaign_id = 200
    buyer_id = 'bogdan'
    timeperiodstr = 'Today (Default)'

    error = ''
    if request.method == 'POST':
        form = InputOptionsForm(request.POST)
        if form.is_valid():
            start_day   = form['start_day'].value()
            stop_day    = form['finish_day'].value()
            campaign_id = form['campaign_id'].value()
            buyer_id    = form['buyer_id'].value()
            timeperiodstr = 'From {} to {}'.format(form['start_day'].value(), form['finish_day'].value())
        else:
            error ='Form isnt correct'

    cc = get_data(start_day, stop_day, campaign_id, buyer_id)

    form = InputOptionsForm()

    return render(request, 'users/profile.html',
                  {'clicks': 'Number of clicks: {}'.format(cc[0]),
                   'conversions': 'Number of conversions: {}'.format(cc[1]),
                   'timeperiod': timeperiodstr,
                   'form' : form,
                   'error': error,
                   'campaign_id': 'Campaign Id: {}'.format(campaign_id),
                   'buyer_id': 'Buyer name: {}'.format(buyer_id)})


