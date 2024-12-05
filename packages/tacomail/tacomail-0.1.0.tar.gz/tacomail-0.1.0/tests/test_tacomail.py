import pytest
from tacomail import TacomailClient, Email
from email_sender import PostmarkEmailSender


@pytest.fixture
def client():
    with TacomailClient("https://tacomail.de") as client:
        yield client


def test_get_contact_email(client):
    email = client.get_contact_email()
    assert isinstance(email, str)
    assert "@" in email


def test_get_random_username(client):
    username = client.get_random_username()
    assert isinstance(username, str)
    assert len(username) > 0


def test_get_domains(client):
    domains = client.get_domains()
    assert isinstance(domains, list)
    assert len(domains) > 0
    assert all(isinstance(domain, str) for domain in domains)
    assert all("." in domain for domain in domains)


def test_fetch_empty_inbox(client: TacomailClient):
    # Get a random email address using available domains
    domains = client.get_domains()
    username = client.get_random_username()
    email = f"{username}@{domains[0]}"
    # Fetch inbox for this random email
    emails = client.get_inbox(email)
    assert isinstance(emails, list)
    assert len(emails) == 0


def test_email_sender_initialization():
    sender = PostmarkEmailSender()
    assert sender.api_token is not None
    assert sender.SMTP_SERVER == "smtp.postmarkapp.com"
    assert sender.SMTP_PORT == 587


@pytest.mark.flow
def test_full_email_flow(client: TacomailClient):
    # Get random email address
    username = client.get_random_username()
    domains = client.get_domains()
    test_email = f"{username}@{domains[0]}"

    # Verify inbox is empty initially
    initial_inbox = client.get_inbox(test_email)
    assert len(initial_inbox) == 0

    # Send test email
    sender = PostmarkEmailSender()
    test_subject = "Test Email Flow"
    test_body = "This is a test email for the full flow test."

    success = sender.send_email(
        to_email=test_email, subject=test_subject, body=test_body
    )
    assert success is True

    # Wait for email to arrive
    received_email = client.wait_for_email(test_email)
    assert received_email is not None

    # Verify email contents
    assert received_email.subject == test_subject
    assert received_email.body.text == test_body
    assert received_email.to.address == test_email


@pytest.mark.flow
def test_delete_functionality(client: TacomailClient):
    # Setup: Create email address and send two test emails
    username = client.get_random_username()
    domains = client.get_domains()
    test_email = f"{username}@{domains[0]}"

    sender = PostmarkEmailSender()

    # Send both emails
    sender.send_email(
        to_email=test_email, subject="Test Email 1", body="First test email"
    )

    sender.send_email(
        to_email=test_email, subject="Test Email 2", body="Second test email"
    )

    # Wait for both emails to arrive
    received_email = client.wait_for_email(test_email, expected_count=2)
    assert received_email is not None

    # Verify both emails are in inbox
    inbox = client.get_inbox(test_email)
    assert len(inbox) == 2

    # Delete first email
    first_email_id = inbox[0].id
    client.delete_email(test_email, first_email_id)

    # Verify only one email remains
    inbox = client.get_inbox(test_email)
    assert len(inbox) == 1
    assert inbox[0].id != first_email_id

    # Delete entire inbox
    client.delete_inbox(test_email)

    # Verify inbox is empty
    inbox = client.get_inbox(test_email)
    assert len(inbox) == 0


@pytest.mark.flow
def test_wait_for_email_timeout(client: TacomailClient):
    # Get random email address
    username = client.get_random_username()
    domains = client.get_domains()
    test_email = f"{username}@{domains[0]}"

    # Try to wait for an email that will never arrive (with short timeout)
    result = client.wait_for_email(test_email, timeout=5, interval=1)
    assert result is None


@pytest.mark.flow
def test_wait_for_email_filtered(client: TacomailClient):
    # Get random email address
    username = client.get_random_username()
    domains = client.get_domains()
    test_email = f"{username}@{domains[0]}"

    sender = PostmarkEmailSender()

    # Send two emails with different subjects
    sender.send_email(
        to_email=test_email, subject="First Subject", body="First test email"
    )

    sender.send_email(
        to_email=test_email, subject="Second Subject", body="Second test email"
    )

    # Wait for email with specific subject
    def filter_second_email(email: Email) -> bool:
        return email.subject == "Second Subject"

    received_email = client.wait_for_email_filtered(
        test_email, filter_fn=filter_second_email
    )

    assert received_email is not None
    assert received_email.subject == "Second Subject"
    assert received_email.body.text == "Second test email"

    # Test with a filter that won't match
    def filter_nonexistent(email: Email) -> bool:
        return email.subject == "Nonexistent Subject"

    result = client.wait_for_email_filtered(
        test_email, filter_fn=filter_nonexistent, timeout=5, interval=1
    )
    assert result is None
