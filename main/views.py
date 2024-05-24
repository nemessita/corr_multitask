from django.shortcuts import render
import requests

def index(request):
    result = None
    test_str = None
    if request.method == 'POST':
        test_str = request.POST.get('test_str')
        result = len([ele for ele in test_str if ele.isalpha()])
    
    context = {
        'test_str': test_str,
        'result': result,
    }
    
    return render(request, 'index.html', context)


def home(request):
    result = None
    test_str = None
    if request.method == 'POST':
        test_str = request.POST.get('test_str')
        if test_str:
            # Split the string by whitespace and filter out empty strings
            result = len([word for word in test_str.split() if word])

    context = {
        'test_str': test_str,
        'result': result,
    }

    return render(request, 'home.html', context)




API_KEY = '8c61a5f549f79b0f525c907c'
EXCHANGE_API_URL = 'https://api.exchangerate-api.com/v4/latest/USD'

def get_exchange_rate(currency_from, currency_to):
    try:
        response = requests.get(EXCHANGE_API_URL)
        data = response.json()
        rates = data.get('rates', {})
        
        from_rate = rates.get(currency_from.upper())
        to_rate = rates.get(currency_to.upper())

        if from_rate and to_rate:
            return to_rate / from_rate
        else:
            return None
    except requests.RequestException:
        return None

def exc(request):
    context = {}

    if request.method == 'POST':
        currency_from = request.POST.get('currency_from', '').lower()
        currency_to = request.POST.get('currency_to', '').lower()
        amount = request.POST.get('amount', '').strip()

        try:
            amount = float(amount)
            exchange_rate = get_exchange_rate(currency_from, currency_to)

            if exchange_rate is not None:
                exchanged_amount = amount * exchange_rate
            else:
                exchanged_amount = None
                context['error'] = 'Invalid currency conversion or API error.'

            context.update({
                'currency_from': currency_from,
                'currency_to': currency_to,
                'amount': amount,
                'exchange_rate': exchange_rate,
                'exchanged_amount': exchanged_amount
            })

        except ValueError:
            context['error'] = 'Invalid amount. Please enter a number.'

    return render(request, 'exc.html', context)
