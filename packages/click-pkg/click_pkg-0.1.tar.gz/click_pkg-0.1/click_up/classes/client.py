from click_up.classes.initializer import Initializer


class ClickUp:
    """
    CLICK Up client class
    """
    def __init__(self, service_id, merchant_id):
        """
        Initialize Click object

        Args:
            service_id (str): Service ID provided by CLICK
            merchant_id (str): Merchant ID provided by CLICK
        """
        self.initializer = Initializer(service_id, merchant_id)
