import pytest
from tacomail import AsyncTacomailClient, Email
from email_sender import PostmarkEmailSender
import time
from typing import AsyncGenerator

pytest_plugins = ("pytest_asyncio",)


@pytest.fixture
async def client_generator():
    async with AsyncTacomailClient("https://tacomail.de") as client:
        yield client


@pytest.mark.asyncio
async def test_wait_for_email_async(
    client_generator: AsyncGenerator[AsyncTacomailClient, None],
):
    client: AsyncTacomailClient = await anext(client_generator)

    # Get random email address
    username = await client.get_random_username()
    domains = await client.get_domains()
    test_email = f"{username}@{domains[0]}"

    # Send test email (using sync sender)
    sender = PostmarkEmailSender()
    test_subject = "Test Async Email"
    test_body = "This is a test email for the async flow test."

    success = sender.send_email(
        to_email=test_email, subject=test_subject, body=test_body
    )
    assert success is True

    # Wait for email asynchronously
    received_email = await client.wait_for_email(test_email)
    assert received_email is not None
    assert received_email.subject == test_subject
    assert received_email.body.text == test_body


@pytest.mark.asyncio
async def test_wait_for_email_filtered_async(
    client_generator: AsyncGenerator[AsyncTacomailClient, None],
):
    client: AsyncTacomailClient = await anext(client_generator)

    # Get random email address
    username = await client.get_random_username()
    domains = await client.get_domains()
    test_email = f"{username}@{domains[0]}"

    sender = PostmarkEmailSender()

    # Send two emails with different subjects
    sender.send_email(
        to_email=test_email,
        subject="First Async Subject",
        body="First async test email",
    )

    sender.send_email(
        to_email=test_email,
        subject="Second Async Subject",
        body="Second async test email",
    )

    # Wait for email with specific subject
    def filter_second_email(email: Email) -> bool:
        return email.subject == "Second Async Subject"

    received_email = await client.wait_for_email_filtered(
        test_email, filter_fn=filter_second_email
    )

    assert received_email is not None
    assert received_email.subject == "Second Async Subject"
    assert received_email.body.text == "Second async test email"


@pytest.mark.asyncio
async def test_wait_for_email_timeout_async(
    client_generator: AsyncGenerator[AsyncTacomailClient, None],
):
    client: AsyncTacomailClient = await anext(client_generator)

    # Get random email address
    username = await client.get_random_username()
    domains = await client.get_domains()
    test_email = f"{username}@{domains[0]}"

    # Try to wait for an email that will never arrive
    result = await client.wait_for_email(test_email, timeout=5, interval=1)
    assert result is None


@pytest.mark.asyncio
async def test_wait_for_email_timing_async(
    client_generator: AsyncGenerator[AsyncTacomailClient, None],
):
    client: AsyncTacomailClient = await anext(client_generator)

    # Get random email address
    username = await client.get_random_username()
    domains = await client.get_domains()
    test_email = f"{username}@{domains[0]}"

    # Record start time
    start_time = time.time()

    # Try to wait for an email that will never arrive
    result = await client.wait_for_email(test_email, timeout=3, interval=0.5)

    # Calculate elapsed time
    elapsed = time.time() - start_time

    assert result is None
    # Allow for small timing variations but ensure we're close to the timeout
    assert 2.9 <= elapsed <= 3.2, f"Expected timeout of 3 seconds, got {elapsed}"
