

# pylint: disable=W0622


class Initializer:
    """
    Initializer class for generating payment URLs for the Paylik system.
    """
    def __init__(self, service_id, merchant_id):
        """
        Initialize Initializer object

        Args:
            service_id (str): Service ID provided by CLICK
            merchant_id (str): Merchant ID provided by CLICK
        """
        self.service_id = service_id
        self.merchant_id = merchant_id

    def generate_pay_link(self, id, amount, return_url):
        """
        Generate a payment URL for the Paylik system.

        :param amount: Payment amount (float or string)
        :param id: Transaction-specific parameter (string)
        :param return_url: URL to return to after payment (string)
        :return: Generated Paylik URL (string)
        """
        base_url = "https://my.click.uz/services/pay"
        paylik_url = (
            f"{base_url}?service_id={self.service_id}&merchant_id={self.merchant_id}" # noqa
            f"&amount={amount}&transaction_param={id}"
            f"&return_url={return_url}"
        )
        return paylik_url
