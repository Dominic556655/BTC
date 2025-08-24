from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Wallet
from django.views.decorators.http import require_POST
from .models import Plan, Deposit, Withdrawal
from decimal import Decimal
from decimal import Decimal, InvalidOperation
import requests
import datetime
import json





# Create your views here.
def index (request): 
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'index.html')
def about (request):
    return render(request, 'about.html')
def blog (request):
    return render(request, 'blog.html')
def plan (request):
    return render(request, 'plan.html')
def news (request):
    return render(request, 'news.html')
def single_blog(request):
    return render(request, 'single-blog.html')

def Register (request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2= request.POST['password2']
        
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Already Used')
                return redirect('Register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Already Used')
                return redirect('Register')
            
            else:
                user = User.objects.create_user(username=username,email=email, password=password)
                user.save()
                return redirect('login')
        else:
            messages.info(request, 'Password not the same')
            return redirect('Register')
    else:
        return render (request, 'Register.html')
    
def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user= auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect ('login')
        
    else:
        return render (request, 'login.html')
    
def logout(request):
    auth.logout(request)
    return redirect('index')

def dashboard(request):
    # Bitcoin price in USD
    url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=USD'
    response = requests.get(url)
    data = response.json()
    btc_usd = data.get('bitcoin', {}).get('usd', None)

    # Bitcoin price history in NGN
    hist_url = 'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart'
    hist_params = {'vs_currency': 'ngn', 'days': '7'}
    hist_response = requests.get(hist_url, params=hist_params)
    hist_data = hist_response.json()

    dates = []
    prices = []
    if 'prices' in hist_data:
        for price_point in hist_data['prices']:
            date = datetime.datetime.fromtimestamp(price_point[0] / 1000).strftime('%b %d')
            dates.append(date)
            prices.append(price_point[1])

    # Wallet & Plan info
    wallet, _ = Wallet.objects.get_or_create(user=request.user)
    wallet.apply_hourly_interest()
    plans = Plan.objects.all()
    selected_plan = wallet.plan if wallet.plan else None

    # Deposits and withdrawals
    pending_deposits = Deposit.objects.filter(user=request.user, is_approved=False)
    withdrawals = Withdrawal.objects.filter(user=request.user).order_by('-date_requested')
    
    withdrawals = Withdrawal.objects.filter(
        user=request.user,
        seen_by_user=False  # 👈 Only show unseen withdrawals
    )
    
        # Mark approved withdrawals as seen
    for withdrawal in withdrawals:
        if withdrawal.is_approved:
            withdrawal.seen_by_user = True
            withdrawal.save()

    # Combine all context in ONE dictionary
    context = {
        'wallet': wallet,
        'plans': plans,
        'selected_plan': selected_plan,
        'pending_deposits': pending_deposits,
        'btc_USD': btc_usd,
        'dates': json.dumps(dates),
        'prices': json.dumps(prices),
        'withdrawals': withdrawals
    }

    return render(request, 'dashboard.html', context)

@require_POST
def transaction(request):
    if request.method == 'POST':
        raw_amount = request.POST.get('amount', '').replace('$', '').strip()
        try:
            amount = Decimal(raw_amount)
        except (InvalidOperation, TypeError):
            messages.error(request, "Invalid amount entered.")
            return redirect('dashboard')

        if amount <= 0:
            messages.error(request, "Amount must be greater than zero.")
            return redirect('dashboard')

        Deposit.objects.create(user=request.user, amount=amount)
        messages.success(request, f"Deposit of ${amount} submitted successfully. Awaiting approval.")
        return redirect('dashboard')
    
def withdraw(request):
    if request.method == 'POST':
        raw_amount = request.POST.get('amount', '').strip()
        account_name = request.POST.get('account_name', '').strip()
        account_number = request.POST.get('account_number', '').strip()
        bank_name = request.POST.get('bank_name', '').strip()

        try:
            amount = Decimal(raw_amount)
        except (InvalidOperation, TypeError):
            messages.error(request, "Invalid amount entered.")
            return redirect('withdraw')

        if amount <= 0:
            messages.error(request, "Amount must be greater than zero.")
            return redirect('withdrawal')

        Withdrawal.objects.create(
            user=request.user,
            amount=amount,
            account_name=account_name,
            account_number=account_number,
            bank_name=bank_name
        )

        messages.success(request, f"Withdrawal of ${amount} submitted successfully. Awaiting approval.")
        return redirect('dashboard')

    return render(request, 'withdraw.html')

    
def news(request):
    url = 'https://cryptopanic.com/api/v1/posts/?auth_token=YOUR_API_KEY&currencies=BTC'
    response = requests.get(url)
    data = response.json()

    articles = []
    if 'results' in data:
        for item in data['results'][:6]:  # Get top 6 news items
            articles.append({
                'title': item.get('title'),
                'published_at': datetime.strptime(item.get('published_at')[:10], '%Y-%m-%d').strftime('%d %b %Y'),
                'url': item.get('url'),
                'source': item.get('source', {}).get('title', 'Unknown Source'),
                'summary': item.get('summary', 'No summary available.'),
                # 'image': item.get('image_url', 'default.jpg'),  # If API returns image_url
            })

    context = {'articles': articles}
    return render(request, 'news.html', context)

