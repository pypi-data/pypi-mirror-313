from typing import List, Optional, Union, Callable
import httpx
from dataclasses import dataclass
from datetime import datetime
import time
import asyncio
import random


@dataclass
class EmailAddress:
    address: str
    name: str


@dataclass
class EmailBody:
    text: str
    html: str


@dataclass
class Attachment:
    id: str
    fileName: str
    present: bool


@dataclass
class Email:
    id: str
    from_: EmailAddress
    to: EmailAddress
    subject: str
    date: datetime
    body: EmailBody
    headers: dict
    attachments: List[Attachment]

    @classmethod
    def from_dict(cls, data: dict) -> "Email":
        return cls(
            id=data["id"],
            from_=EmailAddress(**data["from"]),
            to=EmailAddress(**data["to"]),
            subject=data["subject"],
            date=datetime.fromisoformat(data["date"].replace("Z", "+00:00")),
            body=EmailBody(**data["body"]),
            headers=data["headers"],
            attachments=[Attachment(**att) for att in data["attachments"]],
        )


class TacomailClient:
    """A synchronous client for interacting with the TacoMail API.

    This client provides methods to interact with temporary email inboxes, including
    retrieving emails, managing attachments, and waiting for new messages.

    Args:
        base_url (str): The base URL of the TacoMail API. Defaults to "https://tacomail.de".
        client (Optional[httpx.Client]): An optional pre-configured httpx Client instance.
            If not provided, a new client will be created.

    Examples:
        >>> client = TacomailClient()
        >>> # Get a random username and available domains
        >>> username = client.get_random_username()
        >>> domains = client.get_domains()
        >>> # Create an email address and check for emails
        >>> address = f"{username}@{domains[0]}"
        >>> emails = client.get_inbox(address)
    """

    def __init__(
        self,
        base_url: str = "https://tacomail.de",
        client: Optional[httpx.Client] = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.client = client if client is not None else httpx.Client()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    def get_contact_email(self) -> str:
        """Get the contact email address of the TacoMail instance."""
        response = self.client.get(f"{self.base_url}/api/v1/contactEmail")
        response.raise_for_status()
        return response.json()["email"]

    def get_random_username(self) -> str:
        """Get a random username."""
        response = self.client.get(f"{self.base_url}/api/v1/randomUsername")
        response.raise_for_status()
        return response.json()["username"]

    def get_domains(self) -> List[str]:
        """Get all available domains."""
        response = self.client.get(f"{self.base_url}/api/v1/domains")
        response.raise_for_status()
        return response.json()

    def get_random_address(self) -> str:
        """Get a random email address."""
        username = self.get_random_username()
        domains = self.get_domains()
        random_domain = random.choice(domains)
        return f"{username}@{random_domain}"

    def get_inbox(self, address: str, limit: Optional[int] = None) -> List[Email]:
        """Get the last 10 emails (or specified limit) from an inbox.
        
        Note: The maximum number of emails that can be retrieved is 10, regardless of the limit parameter."""
        params = {"limit": limit} if limit is not None else None
        response = self.client.get(
            f"{self.base_url}/api/v1/mail/{address}", params=params
        )
        response.raise_for_status()
        return [Email.from_dict(email) for email in response.json()]

    def get_email(self, address: str, mail_id: str) -> Email:
        """Get a single email by its ID."""
        response = self.client.get(f"{self.base_url}/api/v1/mail/{address}/{mail_id}")
        response.raise_for_status()
        return Email.from_dict(response.json())

    def get_attachments(self, address: str, mail_id: str) -> List[Attachment]:
        """Get all attachments of an email."""
        response = self.client.get(
            f"{self.base_url}/api/v1/mail/{address}/{mail_id}/attachments"
        )
        response.raise_for_status()
        return [Attachment(**att) for att in response.json()]

    def download_attachment(
        self, address: str, mail_id: str, attachment_id: str
    ) -> bytes:
        """Download a single attachment."""
        response = self.client.get(
            f"{self.base_url}/api/v1/mail/{address}/{mail_id}/attachments/{attachment_id}"
        )
        response.raise_for_status()
        return response.content

    def delete_email(self, address: str, mail_id: str) -> None:
        """Delete a single email."""
        response = self.client.delete(
            f"{self.base_url}/api/v1/mail/{address}/{mail_id}"
        )
        response.raise_for_status()

    def delete_inbox(self, address: str) -> None:
        """Delete all emails from an inbox."""
        response = self.client.delete(f"{self.base_url}/api/v1/mail/{address}")
        response.raise_for_status()

    def wait_for_email(
        self,
        address: str,
        timeout: int = 30,
        interval: int = 2,
        expected_count: int = 1,
    ) -> Union[Email, None]:
        """
        Wait for an email to arrive in the inbox.

        Args:
            address: Email address to check
            timeout: Maximum time to wait in seconds (default: 30)
            interval: Time between checks in seconds (default: 2)
            expected_count: Expected number of emails in inbox (default: 1)

        Returns:
            The latest Email object if found, None if timeout is reached
        """
        attempts = timeout // interval

        for _ in range(attempts):
            inbox = self.get_inbox(address)
            if len(inbox) >= expected_count:
                return inbox[0]  # Return the most recent email
            time.sleep(interval)

        return None

    def wait_for_email_filtered(
        self,
        address: str,
        filter_fn: Callable[[Email], bool],
        timeout: int = 30,
        interval: int = 2,
    ) -> Union[Email, None]:
        """
        Wait for an email that matches the given filter function.

        Args:
            address: Email address to check
            filter_fn: Function that takes an Email object and returns bool
            timeout: Maximum time to wait in seconds (default: 30)
            interval: Time between checks in seconds (default: 2)

        Returns:
            The first Email object that matches the filter, None if timeout is reached
        """
        attempts = timeout // interval

        for _ in range(attempts):
            inbox = self.get_inbox(address)
            for email in inbox:
                if filter_fn(email):
                    return email
            time.sleep(interval)

        return None


class AsyncTacomailClient:
    def __init__(
        self,
        base_url: str = "https://tacomail.de",
        client: Optional[httpx.AsyncClient] = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.client = client if client is not None else httpx.AsyncClient()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    async def get_contact_email(self) -> str:
        """Get the contact email address of the TacoMail instance."""
        response = await self.client.get(f"{self.base_url}/api/v1/contactEmail")
        response.raise_for_status()
        return response.json()["email"]

    async def get_random_username(self) -> str:
        """Get a random username."""
        response = await self.client.get(f"{self.base_url}/api/v1/randomUsername")
        response.raise_for_status()
        return response.json()["username"]

    async def get_domains(self) -> List[str]:
        """Get all available domains."""
        response = await self.client.get(f"{self.base_url}/api/v1/domains")
        response.raise_for_status()
        return response.json()

    async def get_random_address(self) -> str:
        """Get a random email address."""
        username, domains = await asyncio.gather(
            self.get_random_username(), self.get_domains()
        )
        random_domain = random.choice(domains)
        return f"{username}@{random_domain}"

    async def get_inbox(self, address: str, limit: Optional[int] = None) -> List[Email]:
        """Get the last 10 emails (or specified limit) from an inbox.
        
        Note: The maximum number of emails that can be retrieved is 10, regardless of the limit parameter."""
        params = {"limit": limit} if limit is not None else None
        response = await self.client.get(
            f"{self.base_url}/api/v1/mail/{address}", params=params
        )
        response.raise_for_status()
        return [Email.from_dict(email) for email in response.json()]

    async def get_email(self, address: str, mail_id: str) -> Email:
        """Get a single email by its ID."""
        response = await self.client.get(
            f"{self.base_url}/api/v1/mail/{address}/{mail_id}"
        )
        response.raise_for_status()
        return Email.from_dict(response.json())

    async def get_attachments(self, address: str, mail_id: str) -> List[Attachment]:
        """Get all attachments of an email."""
        response = await self.client.get(
            f"{self.base_url}/api/v1/mail/{address}/{mail_id}/attachments"
        )
        response.raise_for_status()
        return [Attachment(**att) for att in response.json()]

    async def download_attachment(
        self, address: str, mail_id: str, attachment_id: str
    ) -> bytes:
        """Download a single attachment."""
        response = await self.client.get(
            f"{self.base_url}/api/v1/mail/{address}/{mail_id}/attachments/{attachment_id}"
        )
        response.raise_for_status()
        return response.content

    async def delete_email(self, address: str, mail_id: str) -> None:
        """Delete a single email."""
        response = await self.client.delete(
            f"{self.base_url}/api/v1/mail/{address}/{mail_id}"
        )
        response.raise_for_status()

    async def delete_inbox(self, address: str) -> None:
        """Delete all emails from an inbox."""
        response = await self.client.delete(f"{self.base_url}/api/v1/mail/{address}")
        response.raise_for_status()

    async def wait_for_email(
        self,
        address: str,
        timeout: int = 30,
        interval: float = 2,
        expected_count: int = 1,
    ) -> Union[Email, None]:
        """
        Wait for an email to arrive in the inbox.

        Args:
            address: Email address to check
            timeout: Maximum time to wait in seconds (default: 30)
            interval: Time between checks in seconds (default: 2)
            expected_count: Expected number of emails in inbox (default: 1)

        Returns:
            The latest Email object if found, None if timeout is reached
        """
        end_time = time.time() + timeout

        while True:
            inbox = await self.get_inbox(address)
            if len(inbox) >= expected_count:
                return inbox[0]  # Return the most recent email

            # Calculate remaining time to avoid oversleeping
            remaining = end_time - time.time()
            if remaining <= 0:
                break

            # Sleep for the interval or remaining time, whichever is shorter
            await asyncio.sleep(min(interval, remaining))

        return None

    async def wait_for_email_filtered(
        self,
        address: str,
        filter_fn: Callable[[Email], bool],
        timeout: int = 30,
        interval: float = 2,
    ) -> Union[Email, None]:
        """
        Wait for an email that matches the given filter function.

        Args:
            address: Email address to check
            filter_fn: Function that takes an Email object and returns bool
            timeout: Maximum time to wait in seconds (default: 30)
            interval: Time between checks in seconds (default: 2)

        Returns:
            The first Email object that matches the filter, None if timeout is reached
        """
        end_time = time.time() + timeout

        while True:
            inbox = await self.get_inbox(address)
            for email in inbox:
                if filter_fn(email):
                    return email

            # Calculate remaining time to avoid oversleeping
            remaining = end_time - time.time()
            if remaining <= 0:
                break

            # Sleep for the interval or remaining time, whichever is shorter
            await asyncio.sleep(min(interval, remaining))

        return None
