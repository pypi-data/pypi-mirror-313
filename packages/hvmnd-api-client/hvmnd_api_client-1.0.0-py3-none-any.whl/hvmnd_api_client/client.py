import requests


class APIClient:
    def __init__(self, base_url: str):
        """
        Initialize the API client.

        Parameters:
            base_url (str): The base URL of the API (e.g., 'http://localhost:8080').
        """
        self.base_url = base_url

    def get_nodes(
        self,
        id_: int = None,
        renter: int = None,
        status: str = None,
        any_desk_address: str = None,
        software: str = None
    ):
        """
        Retrieve nodes based on provided filters.

        Parameters:
            id_ (int): Node ID.
            renter (int): Renter ID. If 'non_null', returns nodes with a non-null renter.
            status (str): Node status.
            any_desk_address (str): AnyDesk address.
            software (str): Software name to filter nodes that have it installed.

        Returns:
            List of nodes matching the criteria.
        """
        url = f"{self.base_url}/nodes"
        params = {
            'id': id_,
            'renter': renter,
            'status': status,
            'any_desk_address': any_desk_address,
            'software': software,
        }
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}
        response = requests.get(url, params=params)
        return self._handle_response(response)

    def update_node(self, node_input: dict):
        """
        Update a node.

        Parameters:
            node_input (dict): Node data to update.

        Returns:
            Confirmation message.
        """
        url = f"{self.base_url}/nodes"
        response = requests.put(url, json=node_input)
        return self._handle_response(response)

    def get_payments(self, id_: int = None, user_id: int = None, status: str = None, limit: int = None):
        """
        Retrieve payments based on provided filters.

        Parameters:
            id_ (int): Payment ID.
            user_id (int): User ID.
            status (str): Payment status.
            limit (int): Limit the number of results.

        Returns:
            List of payments matching the criteria.
        """
        url = f"{self.base_url}/payments"
        params = {
            'id': id_,
            'user_id': user_id,
            'status': status,
            'limit': limit,
        }
        params = {k: v for k, v in params.items() if v is not None}
        response = requests.get(url, params=params)
        return self._handle_response(response)

    def create_payment_ticket(self, user_id: int, amount: float):
        """
        Create a payment ticket.

        Parameters:
            user_id (int): User ID.
            amount (float): Amount for the payment.

        Returns:
            Payment ticket ID.
        """
        url = f"{self.base_url}/payments"
        payload = {"user_id": user_id, "amount": amount}
        response = requests.post(url, json=payload)
        return self._handle_response(response)

    def complete_payment(self, id_: int):
        """
        Complete a payment.

        Parameters:
            id_ (int): Payment ID.

        Returns:
            Confirmation of payment completion.
        """
        url = f"{self.base_url}/payments/complete"
        params = {'id': id_}
        response = requests.post(url, params=params)
        return self._handle_response(response)

    def cancel_payment(self, id_: int):
        """
        Cancel a payment.

        Parameters:
            id_ (int): Payment ID.

        Returns:
            Confirmation of payment cancellation.
        """
        url = f"{self.base_url}/payments/cancel"
        params = {'id': id_}
        response = requests.post(url, params=params)
        return self._handle_response(response)

    def get_users(self, id_: int = None, telegram_id: int = None, limit: int = None):
        """
        Retrieve users based on provided filters.

        Parameters:
            id_ (int): User ID.
            telegram_id (int): Telegram ID.
            limit (int): Limit the number of results.

        Returns:
            List of users matching the criteria.
        """
        url = f"{self.base_url}/users"
        params = {
            'id': id_,
            'telegram_id': telegram_id,
            'limit': limit,
        }
        params = {k: v for k, v in params.items() if v is not None}
        response = requests.get(url, params=params)
        return self._handle_response(response)

    def create_or_update_user(self, user_input: dict):
        """
        Create or update a user.

        Parameters:
            user_input (dict): User data.

        Returns:
            User data after creation or update.
        """
        url = f"{self.base_url}/users"
        response = requests.post(url, json=user_input)
        return self._handle_response(response)

    def ping(self):
        """
        Ping the API.

        Returns:
            True if the API is reachable.
        """
        url = f"{self.base_url}/ping"
        response = requests.get(url)
        return response.status_code == 200

    def _handle_response(self, response):
        """
        Handle the API response.

        Parameters:
            response (requests.Response): The response object.

        Returns:
            Parsed JSON data if successful.

        Raises:
            Exception: If the API returns an error or invalid response.
        """
        try:
            json_data = response.json()
        except ValueError:
            # Response is not JSON
            response.raise_for_status()
            raise Exception(f"Invalid response: {response.text}")

        if response.status_code >= 200 and response.status_code < 300:
            if not json_data.get('success', False):
                error_message = json_data.get('error', 'Unknown error')
                raise Exception(f"API Error: {error_message}")
            else:
                return json_data.get('data')
        else:
            # Handle error status codes
            error_message = json_data.get('error', response.reason)
            raise Exception(f"API Error: {error_message}")
