from django.db import models
from django.conf import settings
from django.utils.module_loading import import_string


AccountModel = import_string(settings.CLICK_ACCOUNT_MODEL)

# pylint: disable=E1101,E1126


class ClickTransaction(models.Model):
    """
    Click transaction model
    """
    CREATED = 0
    INITIATING = 1
    SUCCESSFULLY = 2
    CANCELLED = -2

    STATE = [
        (CREATED, "Created"),
        (INITIATING, "Initiating"),
        (SUCCESSFULLY, "Successfully"),
    ]
    state = models.IntegerField(choices=STATE, default=CREATED)
    transaction_id = models.CharField(max_length=255)
    account = models.ForeignKey(
        AccountModel,
        related_name="click_transactions",
        on_delete=models.CASCADE
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ClickTransaction(id={self.id}, state={self.get_state_display()})" # noqa

    def get_state_display(self):
        """
        Return the state of the transaction as a string
        """
        return self.STATE[self.state][1]

    @classmethod
    def get_or_create(
        cls,
        account,
        transaction_id,
        amount,
        state=None
    ) -> "ClickTransaction":
        """
        Get an existing transaction or create a new one
        """
        # pylint: disable=E1101
        transaction, _ = ClickTransaction.objects.get_or_create(
            account=account,
            amount=amount,
            transaction_id=transaction_id,
            defaults={"state": cls.INITIATING},
        )
        if state is not None:
            transaction.state = state
            transaction.save()

        return transaction
