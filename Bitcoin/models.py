from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
import logging



class Plan(models.Model):
    PLAN_CHOICES = [
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('platinum', 'Platinum'),
        ('business', 'Business'),
        ('premium/enterprise ', 'Premium/Enterprise'),
    ]

    name = models.CharField(max_length=20, choices=PLAN_CHOICES, unique=True)
    hourly_rate = models.FloatField(help_text="Percentage growth per hour, e.g. 0.5 for 0.50%")

    def __str__(self):
        return f"{self.name.title()} Plan ({self.hourly_rate}%/hr)"

logger = logging.getLogger(__name__)
class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    plan = models.ForeignKey('Plan', on_delete=models.SET_NULL, null=True, blank=True)
    last_updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username}'s Wallet"

    def apply_hourly_interest(self):
        if not self.plan:
            logger.info("No plan assigned to wallet.")
            return

        now = timezone.now()
        hours_passed = int((now - self.last_updated).total_seconds() // 3600)
        logger.info(f"Hours passed: {hours_passed}")

        if hours_passed >= 1:
            rate = Decimal(str(self.plan.hourly_rate)) / 100
            logger.info(f"Applying rate: {rate}")
            for _ in range(hours_passed):
                self.balance += self.balance * rate

            self.last_updated = now
            self.save()
            logger.info(f"New balance: {self.balance}")
        
class Deposit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    is_approved = models.BooleanField(default=False)  # Only admins can approve
    date_requested = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - ${self.amount} - {'Approved' if self.is_approved else 'Pending'}"
    
class Withdrawal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    account_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=50)
    bank_name = models.CharField(max_length=255)
    is_approved = models.BooleanField(default=False)  # Only admins can approve
    seen_by_user = models.BooleanField(default=False)
    date_requested = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - ${self.amount} - {'Approved' if self.is_approved else 'Pending'}"
