from celery import shared_task
from .models import Wallet

@shared_task
def apply_interest_to_all_wallets():
    for wallet in Wallet.objects.all():
        wallet.apply_hourly_interest()