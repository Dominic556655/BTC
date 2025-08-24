# Register your models here.
from django.contrib import admin
from .models import Wallet, Plan
from .models import Deposit, Withdrawal

# 1. Define the custom admin action
@admin.action(description="Approve selected deposits and update wallet balances")
def approve_deposits(modeladmin, request, queryset):
    for deposit in queryset:
        if not deposit.is_approved:
            deposit.is_approved = True
            deposit.save()

            # Update the user's wallet
            wallet, created = Wallet.objects.get_or_create(user=deposit.user)
            wallet.balance += deposit.amount
            wallet.save()
@admin.action(description="Approve selected withdrawal and update wallet balances")
def approve_withdrawal(modeladmin, request, queryset):
    for withdrawal in queryset:
        if not withdrawal.is_approved:
            withdrawal.is_approved = True
            withdrawal.save()

        # Update the user's wallet
            wallet, created = Wallet.objects.get_or_create(user=withdrawal.user)
            wallet.balance -= withdrawal.amount
            wallet.save()
# 2. Apply the action to the Deposit admin
class DepositAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'is_approved', 'date_requested')
    actions = [approve_deposits]  # <-- attach the custom action here
    
class WithdrawAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'is_approved', 'date_requested')
    actions = [approve_withdrawal]  # <-- attach the custom action here

# 3. Register your models
admin.site.register(Wallet)
admin.site.register(Plan)
admin.site.register(Deposit, DepositAdmin,)  # use custom Deposit admin
admin.site.register(Withdrawal, WithdrawAdmin,)


