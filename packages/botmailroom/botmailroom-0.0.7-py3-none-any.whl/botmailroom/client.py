import asyncio
import hashlib
import hmac
import json
import logging
import os
from datetime import datetime, timedelta
from time import sleep
from typing import Any, Optional, Union

import httpx
from pydantic import BaseModel

from .botmailroom_types import (
    ControlFromAddress,
    DNSRecordStatus,
    Domain,
    EmailContent,
    EmailOverview,
    EmailPayload,
    Inbox,
    InboxConfigurationResponse,
    MessageType,
    OutboundEmailOverview,
    ToolSchemaType,
    WebhookAuthenticationType,
)

logger = logging.getLogger(__name__)


class BotMailRoom:
    """BotMailRoom Python Client"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the BotMailRoom client.

        Args:
            api_key: The API key to use for authentication. You can also set the environment variable `BOTMAILROOM_API_KEY`. Api Keys can be found at https://auth.botmailroom.com/account/api_keys
        """
        self.api_key = api_key or os.getenv("BOTMAILROOM_API_KEY")
        if self.api_key is None:
            raise ValueError(
                "No api key found. Either pass it in via the `api_key` argument or set the environment variable `BOTMAILROOM_API_KEY`."
            )
        self.base_url = "https://api.botmailroom.com/api/v1"
        self._tools: dict[ToolSchemaType, Optional[list[dict]]] = {
            ToolSchemaType.openai: None,
            ToolSchemaType.claude: None,
        }

    def _base_sync_request(
        self, method: str, url: str, **kwargs
    ) -> httpx.Response:
        response = httpx.request(
            method,
            url,
            headers={"Authorization": f"Bearer {self.api_key}"},
            **kwargs,
        )
        if response.status_code >= 400:
            logger.warning(
                f"Request to {url} failed with status code {response.status_code} and message {response.text}"
            )
        response.raise_for_status()
        return response

    async def _base_async_request(
        self, method: str, url: str, **kwargs
    ) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method,
                url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                **kwargs,
            )
            if response.status_code >= 400:
                logger.warning(
                    f"Request to {url} failed with status code {response.status_code} and message {response.text}"
                )
            response.raise_for_status()
            return response

    def get_emails(
        self,
        valid_only: bool = True,
        search_term: Optional[str] = None,
        inbox_ids: Optional[list[str]] = None,
        from_addresses: Optional[list[str]] = None,
        limit: int = 100,
    ) -> list[EmailOverview]:
        """
        Get a list of all emails for the user - only returns the metadata of the emails

        Args:
            valid_only: Whether to only return valid emails. Defaults to True.
            search_term: The search term to filter by. Filters across email content, subject, and attachment filenames. Defaults to None.
            inbox_ids: The inbox IDs to filter by. Defaults to None.
            from_addresses: The from addresses to filter by. Defaults to None.
            limit: The maximum number of emails to return. Defaults to 100.

        Returns:
            A list of EmailOverview objects.
        """
        url = os.path.join(self.base_url, "email")
        params = {
            "valid_only": valid_only,
            "limit": limit,
        }
        if search_term is not None:
            params["search_term"] = search_term
        if inbox_ids is not None:
            params["inbox_ids"] = inbox_ids
        if from_addresses is not None:
            params["from_addresses"] = from_addresses
        response = self._base_sync_request("GET", url, params=params)
        return [EmailOverview(**email) for email in response.json()]

    async def get_emails_async(
        self,
        valid_only: bool = True,
        search_term: Optional[str] = None,
        inbox_ids: Optional[list[str]] = None,
        from_addresses: Optional[list[str]] = None,
        limit: int = 100,
    ) -> list[EmailOverview]:
        """
        Async version of get_emails

        Get a list of all emails for the user - only returns the metadata of the emails

        Args:
            valid_only: Whether to only return valid emails. Defaults to True.
            search_term: The search term to filter by. Filters across email content, subject, and attachment filenames. Defaults to None.
            inbox_ids: The inbox IDs to filter by. Defaults to None.
            from_addresses: The from addresses to filter by. Defaults to None.
            limit: The maximum number of emails to return. Defaults to 100.

        Returns:
            A list of EmailOverview objects.
        """
        url = os.path.join(self.base_url, "email")
        params = {
            "valid_only": valid_only,
            "limit": limit,
        }
        if search_term is not None:
            params["search_term"] = search_term
        if inbox_ids is not None:
            params["inbox_ids"] = inbox_ids
        if from_addresses is not None:
            params["from_addresses"] = from_addresses
        response = await self._base_async_request("GET", url, params=params)
        return [EmailOverview(**email) for email in response.json()]

    def get_email_content(self, email_id: str) -> EmailContent:
        """
        Get the metadata and content of an email. Only attachment metadata is included, use the get_email_attachment method to get the raw attachment. Only available for valid emails.

        Args:
            email_id: The ID of the email to get the content of.

        Returns:
            An EmailContent object
        """
        url = os.path.join(self.base_url, "email", email_id)
        response = self._base_sync_request("GET", url)
        return EmailContent(**response.json())

    async def get_email_content_async(self, email_id: str) -> EmailContent:
        """
        Async version of get_email_content

        Get the metadata and content of an email. Only attachment metadata is included, use the get_email_attachment_async method to get the raw attachment. Only available for valid emails.

        Args:
            email_id: The ID of the email to get the content of.

        Returns:
            An EmailContent object
        """
        url = os.path.join(self.base_url, "email", email_id)
        response = await self._base_async_request("GET", url)
        return EmailContent(**response.json())

    def get_email_attachment(self, email_id: str, attachment_id: str) -> bytes:
        """
        Get a raw attachment from an email. Only available for valid emails.

        Args:
            email_id: The ID of the email to get the attachment from.
            attachment_id: The ID of the attachment to get.

        Returns:
            The raw attachment as bytes.
        """
        url = os.path.join(
            self.base_url,
            "email",
            email_id,
            "attachment",
            attachment_id,
        )
        response = self._base_sync_request("GET", url)
        return response.content

    async def get_email_attachment_async(
        self, email_id: str, attachment_id: str
    ) -> bytes:
        """
        Async version of get_email_attachment

        Get a raw attachment from an email. Only available for valid emails.

        Args:
            email_id: The ID of the email to get the attachment from.
            attachment_id: The ID of the attachment to get.

        Returns:
            The raw attachment as bytes.
        """
        url = os.path.join(
            self.base_url,
            "email",
            email_id,
            "attachment",
            attachment_id,
        )
        response = await self._base_async_request("GET", url)
        return await response.aread()

    def get_email_raw(self, email_id: str) -> bytes:
        """
        Get the entire unparsed email file as an EML file. Only available for valid
        emails.

        Args:
            email_id: The ID of the email to get the raw content of.

        Returns:
            The raw email content as bytes.
        """
        url = os.path.join(self.base_url, "email", email_id, "raw")
        response = self._base_sync_request("GET", url)
        return response.content

    async def get_email_raw_async(self, email_id: str) -> bytes:
        """
        Async version of get_email_raw

        Get the entire unparsed email file as an EML file. Only available for valid
        emails.

        Args:
            email_id: The ID of the email to get the raw content of.

        Returns:
            The raw email content as bytes.
        """
        url = os.path.join(self.base_url, "email", email_id, "raw")
        response = await self._base_async_request("GET", url)
        return await response.aread()

    def mark_email(self, email_id: str, valid: bool) -> EmailOverview:
        """
        Mark an email as valid or invalid.

        Args:
            email_id: The ID of the email to mark.
            valid: Whether to mark the email as valid or invalid.

        Returns:
            An EmailOverview object.
        """
        url = os.path.join(
            self.base_url,
            "email",
            email_id,
            "mark",
            str(valid),
        )
        response = self._base_sync_request("POST", url)
        return EmailOverview(**response.json())

    async def mark_email_async(
        self, email_id: str, valid: bool
    ) -> EmailOverview:
        """
        Async version of mark_email

        Mark an email as valid or invalid.

        Args:
            email_id: The ID of the email to mark.
            valid: Whether to mark the email as valid or invalid.

        Returns:
            An EmailOverview object.
        """
        url = os.path.join(
            self.base_url,
            "email",
            email_id,
            "mark",
            str(valid),
        )
        response = await self._base_async_request("POST", url)
        return EmailOverview(**response.json())

    def get_inboxes(self) -> list[Inbox]:
        """
        Get a list of all inboxes for the user.

        Returns:
            A list of Inbox objects.
        """
        url = os.path.join(self.base_url, "inbox")
        response = self._base_sync_request("GET", url)
        return [Inbox(**inbox) for inbox in response.json()]

    async def get_inboxes_async(self) -> list[Inbox]:
        """
        Async version of get_inboxes

        Get a list of all inboxes for the user.

        Returns:
            A list of Inbox objects.
        """
        url = os.path.join(self.base_url, "inbox")
        response = await self._base_async_request("GET", url)
        return [Inbox(**inbox) for inbox in response.json()]

    def create_inbox(
        self,
        name: str,
        email_address: str,
        allow_cc: bool = True,
        allow_bcc: bool = True,
        spf_pass_required: bool = True,
        dkim_pass_required: bool = True,
        dmarc_pass_required: bool = True,
        allowed_from_addresses: Optional[ControlFromAddress] = None,
        blocked_from_addresses: Optional[ControlFromAddress] = None,
        webhook_url: Optional[str] = None,
        webhook_authentication_type: Optional[
            WebhookAuthenticationType
        ] = None,
        webhook_secret: Optional[str] = None,
        open_and_click_tracking: bool = False,
    ) -> InboxConfigurationResponse:
        """
        Create a new inbox.

        Args:
            name: The name of the inbox.
            email_address: The email address of the inbox.
            allow_cc: If `true`, emails that contain the inbox email address in the Cc field will be marked valid. Defaults to True.
            allow_bcc: If `true`, emails that contain the inbox email address in the Bcc field will be marked valid. Defaults to True.
            spf_pass_required: If `true`, emails need to pass the SPF check to be marked valid. See [here](https://www.cloudflare.com/learning/dns/dns-records/dns-spf-record/) for more information on SPF. Defaults to True.
            dkim_pass_required: If `true`, emails need to pass the DKIM check to be marked valid. See [here](https://www.cloudflare.com/learning/dns/dns-records/dns-dkim-record/) for more information on DKIM. Defaults to True.
            dmarc_pass_required: If `true`, emails need to pass the DMARC check to be marked valid. See [here](https://www.cloudflare.com/learning/email-security/dmarc-explained/) for more information on DMARC. Defaults to True.
            allowed_from_addresses: A list of addresses and domains that are allowed to send emails to the inbox. If the field is `null`, or the `addresses` and `domains` fields are both empty lists, all from addresses are allowed. Defaults to None.
            blocked_from_addresses: A list of addresses and domains that are blocked from sending emails to the inbox. If the field is `null`, or the `addresses` and `domains` fields are both empty lists, no from addresses are blocked. Defaults to None.
            webhook_url: The url to send webhooks to when an email is received by the inbox. Defaults to None.
            webhook_authentication_type: The type of authentication to use for the webhook. Must be provided if `webhook_url` is provided. See [here](https://docs.botmailroom.com/documentation/inbox/webhook-validation) for more information.
            webhook_secret: The secret to use for the webhook. This is only valid when `webhook_authentication_type` is `bearer_token`.
            open_and_click_tracking: If `true`, the inbox will track opens and clicks for emails sent from the inbox. Defaults to False.

        Returns:
            An InboxConfigurationResponse object:
                id: The ID of the inbox.
                webhook_secret: The webhook signing secret for the inbox. This is only returned if the webhook URL is provided and the webhook authentication type is `signing_secret`. Be sure to save this value as it is used to verify the authenticity of webhooks and will not be returned again.
        """
        url = os.path.join(self.base_url, "inbox", "upsert")
        response = self._base_sync_request(
            "POST",
            url,
            json={
                "id": None,
                "name": name,
                "email_address": email_address,
                "allow_cc": allow_cc,
                "allow_bcc": allow_bcc,
                "spf_pass_required": spf_pass_required,
                "dkim_pass_required": dkim_pass_required,
                "dmarc_pass_required": dmarc_pass_required,
                "allowed_from_addresses": allowed_from_addresses,
                "blocked_from_addresses": blocked_from_addresses,
                "webhook_url": webhook_url,
                "webhook_authentication_type": webhook_authentication_type,
                "webhook_secret": webhook_secret,
                "open_and_click_tracking": open_and_click_tracking,
            },
        )
        output = response.json()
        return InboxConfigurationResponse(**output)

    async def create_inbox_async(
        self,
        name: str,
        email_address: str,
        allow_cc: bool = True,
        allow_bcc: bool = True,
        spf_pass_required: bool = True,
        dkim_pass_required: bool = True,
        dmarc_pass_required: bool = True,
        allowed_from_addresses: Optional[ControlFromAddress] = None,
        blocked_from_addresses: Optional[ControlFromAddress] = None,
        webhook_url: Optional[str] = None,
        webhook_authentication_type: Optional[
            WebhookAuthenticationType
        ] = None,
        webhook_secret: Optional[str] = None,
        open_and_click_tracking: bool = False,
    ) -> InboxConfigurationResponse:
        """
        Async version of create_inbox

        Create a new inbox.

        Args:
            name: The name of the inbox.
            email_address: The email address of the inbox.
            allow_cc: If `true`, emails that contain the inbox email address in the Cc field will be marked valid. Defaults to True.
            allow_bcc: If `true`, emails that contain the inbox email address in the Bcc field will be marked valid. Defaults to True.
            spf_pass_required: If `true`, emails need to pass the SPF check to be marked valid. See [here](https://www.cloudflare.com/learning/dns/dns-records/dns-spf-record/) for more information on SPF. Defaults to True.
            dkim_pass_required: If `true`, emails need to pass the DKIM check to be marked valid. See [here](https://www.cloudflare.com/learning/dns/dns-records/dns-dkim-record/) for more information on DKIM. Defaults to True.
            dmarc_pass_required: If `true`, emails need to pass the DMARC check to be marked valid. See [here](https://www.cloudflare.com/learning/email-security/dmarc-explained/) for more information on DMARC. Defaults to True.
            allowed_from_addresses: A list of addresses and domains that are allowed to send emails to the inbox. If the field is `null`, or the `addresses` and `domains` fields are both empty lists, all from addresses are allowed. Defaults to None.
            blocked_from_addresses: A list of addresses and domains that are blocked from sending emails to the inbox. If the field is `null`, or the `addresses` and `domains` fields are both empty lists, no from addresses are blocked. Defaults to None.
            webhook_url: The url to send webhooks to when an email is received by the inbox. Defaults to None.
            webhook_authentication_type: The type of authentication to use for the webhook. Must be provided if `webhook_url` is provided. See [here](https://docs.botmailroom.com/documentation/inbox/webhook-validation) for more information.
            webhook_secret: The secret to use for the webhook. This is only valid when `webhook_authentication_type` is `bearer_token`.
            open_and_click_tracking: If `true`, the inbox will track opens and clicks for emails sent from the inbox. Defaults to False.

        Returns:
            An InboxConfigurationResponse object:
                id: The ID of the inbox.
                webhook_secret: The webhook signing secret for the inbox. This is only returned if the webhook URL is provided and the webhook authentication type is `signing_secret`. Be sure to save this value as it is used to verify the authenticity of webhooks and will not be returned again.
        """
        url = os.path.join(self.base_url, "inbox", "upsert")
        response = await self._base_async_request(
            "POST",
            url,
            json={
                "id": None,
                "name": name,
                "email_address": email_address,
                "allow_cc": allow_cc,
                "allow_bcc": allow_bcc,
                "spf_pass_required": spf_pass_required,
                "dkim_pass_required": dkim_pass_required,
                "dmarc_pass_required": dmarc_pass_required,
                "allowed_from_addresses": allowed_from_addresses,
                "blocked_from_addresses": blocked_from_addresses,
                "webhook_url": webhook_url,
                "webhook_authentication_type": webhook_authentication_type,
                "webhook_secret": webhook_secret,
                "open_and_click_tracking": open_and_click_tracking,
            },
        )
        output = response.json()
        return InboxConfigurationResponse(**output)

    def update_inbox(
        self,
        id: str,
        name: str,
        email_address: str,
        allow_cc: bool = True,
        allow_bcc: bool = True,
        spf_pass_required: bool = True,
        dkim_pass_required: bool = True,
        dmarc_pass_required: bool = True,
        allowed_from_addresses: Optional[ControlFromAddress] = None,
        blocked_from_addresses: Optional[ControlFromAddress] = None,
        webhook_url: Optional[str] = None,
        webhook_authentication_type: Optional[
            WebhookAuthenticationType
        ] = None,
        webhook_secret: Optional[str] = None,
        open_and_click_tracking: bool = False,
    ) -> InboxConfigurationResponse:
        """
        Update an existing inbox. WARNING: This is a full update, so all fields must be provided with their desired values.

        Args:
            id: The ID of the inbox to update.
            name: The name of the inbox.
            email_address: The email address of the inbox.
            allow_cc: If `true`, emails that contain the inbox email address in the Cc field will be marked valid. Defaults to True.
            allow_bcc: If `true`, emails that contain the inbox email address in the Bcc field will be marked valid. Defaults to True.
            spf_pass_required: If `true`, emails need to pass the SPF check to be marked valid. See [here](https://www.cloudflare.com/learning/dns/dns-records/dns-spf-record/) for more information on SPF. Defaults to True.
            dkim_pass_required: If `true`, emails need to pass the DKIM check to be marked valid. See [here](https://www.cloudflare.com/learning/dns/dns-records/dns-dkim-record/) for more information on DKIM. Defaults to True.
            dmarc_pass_required: If `true`, emails need to pass the DMARC check to be marked valid. See [here](https://www.cloudflare.com/learning/email-security/dmarc-explained/) for more information on DMARC. Defaults to True.
            allowed_from_addresses: A list of addresses and domains that are allowed to send emails to the inbox. If the field is `null`, or the `addresses` and `domains` fields are both empty lists, all from addresses are allowed. Defaults to None.
            blocked_from_addresses: A list of addresses and domains that are blocked from sending emails to the inbox. If the field is `null`, or the `addresses` and `domains` fields are both empty lists, no from addresses are blocked. Defaults to None.
            webhook_url: The url to send webhooks to when an email is received by the inbox. Defaults to None.
            webhook_authentication_type: The type of authentication to use for the webhook. Must be provided if `webhook_url` is provided. See [here](https://docs.botmailroom.com/documentation/inbox/webhook-validation) for more information.
            webhook_secret: The secret to use for the webhook. This is only valid when `webhook_authentication_type` is `bearer_token`.
            open_and_click_tracking: If `true`, the inbox will track opens and clicks for emails sent from the inbox. Defaults to False.

        Returns:
            An InboxConfigurationResponse object:
                id: The ID of the inbox.
                webhook_secret: The webhook signing secret for the inbox. This is only returned if the webhook URL is provided and the webhook authentication type is `signing_secret`. Be sure to save this value as it is used to verify the authenticity of webhooks and will not be returned again.
        """
        url = os.path.join(self.base_url, "inbox", "upsert")
        response = self._base_sync_request(
            "POST",
            url,
            json={
                "id": id,
                "name": name,
                "email_address": email_address,
                "allow_cc": allow_cc,
                "allow_bcc": allow_bcc,
                "spf_pass_required": spf_pass_required,
                "dkim_pass_required": dkim_pass_required,
                "dmarc_pass_required": dmarc_pass_required,
                "allowed_from_addresses": allowed_from_addresses,
                "blocked_from_addresses": blocked_from_addresses,
                "webhook_url": webhook_url,
                "webhook_authentication_type": webhook_authentication_type,
                "webhook_secret": webhook_secret,
                "open_and_click_tracking": open_and_click_tracking,
            },
        )
        output = response.json()
        return InboxConfigurationResponse(**output)

    async def update_inbox_async(
        self,
        id: str,
        name: str,
        email_address: str,
        allow_cc: bool = True,
        allow_bcc: bool = True,
        spf_pass_required: bool = True,
        dkim_pass_required: bool = True,
        dmarc_pass_required: bool = True,
        allowed_from_addresses: Optional[ControlFromAddress] = None,
        blocked_from_addresses: Optional[ControlFromAddress] = None,
        webhook_url: Optional[str] = None,
        webhook_authentication_type: Optional[
            WebhookAuthenticationType
        ] = None,
        webhook_secret: Optional[str] = None,
        open_and_click_tracking: bool = False,
    ) -> InboxConfigurationResponse:
        """
        Async version of update_inbox

        Update an existing inbox. WARNING: This is a full update, so all fields must be provided with their desired values.

        Args:
            id: The ID of the inbox to update.
            name: The name of the inbox.
            email_address: The email address of the inbox.
            allow_cc: If `true`, emails that contain the inbox email address in the Cc field will be marked valid. Defaults to True.
            allow_bcc: If `true`, emails that contain the inbox email address in the Bcc field will be marked valid. Defaults to True.
            spf_pass_required: If `true`, emails need to pass the SPF check to be marked valid. See [here](https://www.cloudflare.com/learning/dns/dns-records/dns-spf-record/) for more information on SPF. Defaults to True.
            dkim_pass_required: If `true`, emails need to pass the DKIM check to be marked valid. See [here](https://www.cloudflare.com/learning/dns/dns-records/dns-dkim-record/) for more information on DKIM. Defaults to True.
            dmarc_pass_required: If `true`, emails need to pass the DMARC check to be marked valid. See [here](https://www.cloudflare.com/learning/email-security/dmarc-explained/) for more information on DMARC. Defaults to True.
            allowed_from_addresses: A list of addresses and domains that are allowed to send emails to the inbox. If the field is `null`, or the `addresses` and `domains` fields are both empty lists, all from addresses are allowed. Defaults to None.
            blocked_from_addresses: A list of addresses and domains that are blocked from sending emails to the inbox. If the field is `null`, or the `addresses` and `domains` fields are both empty lists, no from addresses are blocked. Defaults to None.
            webhook_url: The url to send webhooks to when an email is received by the inbox. Defaults to None.
            webhook_authentication_type: The type of authentication to use for the webhook. Must be provided if `webhook_url` is provided. See [here](https://docs.botmailroom.com/documentation/inbox/webhook-validation) for more information.
            webhook_secret: The secret to use for the webhook. This is only valid when `webhook_authentication_type` is `bearer_token`.
            open_and_click_tracking: If `true`, the inbox will track opens and clicks for emails sent from the inbox. Defaults to False.

        Returns:
            An InboxConfigurationResponse object:
                id: The ID of the inbox.
                webhook_secret: The webhook signing secret for the inbox. This is only returned if the webhook URL is provided and the webhook authentication type is `signing_secret`. Be sure to save this value as it is used to verify the authenticity of webhooks and will not be returned again.
        """
        url = os.path.join(self.base_url, "inbox", "upsert")
        response = await self._base_async_request(
            "POST",
            url,
            json={
                "id": id,
                "name": name,
                "email_address": email_address,
                "allow_cc": allow_cc,
                "allow_bcc": allow_bcc,
                "spf_pass_required": spf_pass_required,
                "dkim_pass_required": dkim_pass_required,
                "dmarc_pass_required": dmarc_pass_required,
                "allowed_from_addresses": allowed_from_addresses,
                "blocked_from_addresses": blocked_from_addresses,
                "webhook_url": webhook_url,
                "webhook_authentication_type": webhook_authentication_type,
                "webhook_secret": webhook_secret,
                "open_and_click_tracking": open_and_click_tracking,
            },
        )
        output = response.json()
        return InboxConfigurationResponse(**output)

    def get_domains(self) -> list[Domain]:
        """
        Get all custom domains

        Returns:
            A list of Domain objects.
        """
        url = os.path.join(self.base_url, "domain")
        response = self._base_sync_request("GET", url)
        return [Domain(**domain) for domain in response.json()]

    async def get_domains_async(self) -> list[Domain]:
        """
        Async version of get_domains

        Get all custom domains

        Returns:
            A list of Domain objects.
        """
        url = os.path.join(self.base_url, "domain")
        response = await self._base_async_request("GET", url)
        return [Domain(**domain) for domain in response.json()]

    def create_domain(self, domain: str) -> Domain:
        """
        Add a custom domain

        Args:
            domain: The domain to add. You must have access to the DNS records for this domain.

        Returns:
            A Domain object.
        """
        url = os.path.join(self.base_url, "domain", "create")
        response = self._base_sync_request(
            "POST", url, json={"domain": domain}
        )
        return Domain(**response.json())

    async def create_domain_async(self, domain: str) -> Domain:
        """
        Async version of create_domain

        Add a custom domain

        Args:
            domain: The domain to add. You must have access to the DNS records for this domain.

        Returns:
            A Domain object.
        """
        url = os.path.join(self.base_url, "domain", "create")
        response = await self._base_async_request(
            "POST", url, json={"domain": domain}
        )
        return Domain(**response.json())

    def verify_domain(self, domain_id: str) -> DNSRecordStatus:
        """
        Verify a custom domain

        Args:
            domain_id: The ID of the domain to verify.

        Returns:
            status: The status of the domain verification.
        """
        url = os.path.join(self.base_url, "domain", domain_id, "verify")
        response = self._base_sync_request("GET", url)
        return DNSRecordStatus(response.json()["status"])

    async def verify_domain_async(self, domain_id: str) -> DNSRecordStatus:
        """
        Async version of verify_domain

        Verify a custom domain

        Args:
            domain_id: The ID of the domain to verify.

        Returns:
            status: The status of the domain verification.
        """
        url = os.path.join(self.base_url, "domain", domain_id, "verify")
        response = await self._base_async_request("GET", url)
        return DNSRecordStatus(response.json()["status"])

    def add_attachment_to_pool(
        self, file: bytes, filename: str, content_type: Optional[str] = None
    ) -> str:
        """
        Add an attachment to the attachments pool. Only attachments in the pool can be used in `send_email` requests.

        Args:
            file: The attachment file as bytes. The file can be up to 10MB in size.
            filename: The name of the file to be used in the email
            content_type: The MIME type of the file (e.g., 'application/pdf', 'image/jpeg').
                        If not provided, will attempt to guess from the filename.

        Returns:
            The ID of the attachment to use in `send_email` requests
        """
        url = os.path.join(self.base_url, "email", "add-attachment-to-pool")
        files = {"file": (filename, file, content_type)}
        response = self._base_sync_request("POST", url, files=files)
        return response.json()["id"]

    async def add_attachment_to_pool_async(
        self, file: bytes, filename: str, content_type: Optional[str] = None
    ) -> str:
        """
        Async version of add_attachment_to_pool

        Add an attachment to the attachments pool. Only attachments in the pool can be used in `send_email` requests.

        Args:
            file: The attachment file as bytes. The file can be up to 10MB in size.
            filename: The name of the file to be used in the email
            content_type: The MIME type of the file (e.g., 'application/pdf', 'image/jpeg').
                        If not provided, will attempt to guess from the filename.

        Returns:
            The ID of the attachment to use in `send_email` requests
        """
        url = os.path.join(self.base_url, "email", "add-attachment-to-pool")
        files = {"file": (filename, file, content_type)}
        response = await self._base_async_request("POST", url, files=files)
        output = response.json()
        return output["id"]

    def send_email(
        self,
        inbox_id: str,
        subject: Optional[str] = None,
        to_addresses: Optional[list[str]] = None,
        cc_addresses: Optional[list[str]] = None,
        bcc_addresses: Optional[list[str]] = None,
        reply_to_addresses: Optional[list[str]] = None,
        idempotency_key: Optional[str] = None,
        plain_text: Optional[str] = None,
        html: Optional[str] = None,
        alternative_content: bool = False,
        existing_email_id: Optional[str] = None,
        message_type: MessageType = MessageType.new,
        attachment_ids: Optional[list[str]] = None,
        attachments_raw: Optional[
            list[tuple[str, bytes, Optional[str]]]
        ] = None,
        open_and_click_tracking: Optional[bool] = None,
    ) -> str:
        """
        Send an email from one of your inboxes.

        Args:
            inbox_id: The ID of the inbox to send the email from
            subject: The subject line of the email. Can only be None if existing_email_id is provided and the email is a reply or forward.
            to_addresses: List of recipient email addresses. One of to_addresses, cc_addresses, or bcc_addresses must be provided. Defaults to None
            cc_addresses: List of CC recipient email addresses. One of to_addresses, cc_addresses, or bcc_addresses must be provided. Defaults to None
            bcc_addresses: List of BCC recipient email addresses. One of to_addresses, cc_addresses, or bcc_addresses must be provided. Defaults to None
            reply_to_addresses: List of Reply-To email addresses. Defaults to None
            idempotency_key: Optional unique identifier for the email. If the same request is sent multiple times with the same key, only the first email will be sent. Defaults to None
            plain_text: Optional plain text content of the email. Can be None if the email is only available in HTML. Either plain_text or html must be provided.
            html: Optional HTML content of the email. Can be None if the email is only available in plain text. Either plain_text or html must be provided.
            alternative_content: If True, html and plain_text are alternative representations of the same content. If both are provided, this must be True. Defaults to False.
            existing_email_id: Optional BotMailRoom ID of the email to reply to or forward. None if this is a new email. Defaults to None
            message_type: Type of message ("new", "reply", or "forward"). Defaults to "new"
            attachment_ids: List of attachment IDs from the attachments pool to include in the email. Only this or attachments_raw can be provided. Defaults to None
            attachments_raw: List of tuples containing the filename, file bytes, and MIME type of each attachment to include in the email. Only this or attachment_ids can be provided. Defaults to None
            open_and_click_tracking: If `true`, the inbox will track opens and clicks for emails sent from the inbox. If None, the inbox's default setting will be used. Defaults to None

        Returns:
            The ID of the sent email
        """
        if (
            to_addresses is None
            and cc_addresses is None
            and bcc_addresses is None
        ):
            raise ValueError(
                "One of to_addresses, cc_addresses, or bcc_addresses must be provided"
            )

        if plain_text is None and html is None:
            raise ValueError("Either plain_text or html must be provided")

        if (
            plain_text is not None
            and html is not None
            and not alternative_content
        ):
            raise ValueError(
                "alternative_content must be True if both plain_text and html are provided"
            )

        if attachment_ids is not None and attachments_raw is not None:
            raise ValueError(
                "Only one of attachment_ids or attachments_raw can be provided"
            )

        if message_type != MessageType.new and existing_email_id is None:
            raise ValueError(
                "existing_email_id must be provided if message_type is not 'new'"
            )

        if subject is None and existing_email_id is None:
            raise ValueError(
                "subject must be provided if existing_email_id is None"
            )

        if attachments_raw is not None and len(attachments_raw) > 0:
            logger.info("Uploading attachments to attachments pool")
            attachment_ids = []
            for filename, file, content_type in attachments_raw:
                attachment_ids.append(
                    self.add_attachment_to_pool(file, filename, content_type)
                )
            logger.info(
                f"Uploaded {len(attachment_ids)} attachments to attachments pool"
            )

        payload: dict[str, Any] = {
            "inbox_id": inbox_id,
            "subject": subject,
            "idempotency_key": idempotency_key,
            "plain_text": plain_text,
            "html": html,
            "alternative_content": alternative_content,
            "existing_email_id": existing_email_id,
            "message_type": message_type,
            "open_and_click_tracking": open_and_click_tracking,
        }
        if to_addresses is not None:
            payload["to_addresses"] = [
                {"address": address, "name": None} for address in to_addresses
            ]
        if cc_addresses is not None:
            payload["cc_addresses"] = [
                {"address": address, "name": None} for address in cc_addresses
            ]
        if bcc_addresses is not None:
            payload["bcc_addresses"] = [
                {"address": address, "name": None} for address in bcc_addresses
            ]
        if reply_to_addresses is not None:
            payload["reply_to_addresses"] = [
                {"address": address, "name": None}
                for address in reply_to_addresses
            ]
        if attachment_ids is not None:
            payload["attachment_ids"] = attachment_ids

        url = os.path.join(self.base_url, "email", "send")
        response = self._base_sync_request(
            "POST",
            url,
            json=payload,
        )
        return response.json()["id"]

    async def send_email_async(
        self,
        inbox_id: str,
        subject: Optional[str] = None,
        to_addresses: Optional[list[str]] = None,
        cc_addresses: Optional[list[str]] = None,
        bcc_addresses: Optional[list[str]] = None,
        reply_to_addresses: Optional[list[str]] = None,
        idempotency_key: Optional[str] = None,
        plain_text: Optional[str] = None,
        html: Optional[str] = None,
        alternative_content: bool = False,
        existing_email_id: Optional[str] = None,
        message_type: MessageType = MessageType.new,
        attachment_ids: Optional[list[str]] = None,
        attachments_raw: Optional[
            list[tuple[str, bytes, Optional[str]]]
        ] = None,
        open_and_click_tracking: Optional[bool] = None,
    ) -> str:
        """
        Async version of send_email

        Send an email from one of your inboxes.

        Args:
            inbox_id: The ID of the inbox to send the email from
            subject: The subject line of the email. Can only be None if existing_email_id is provided and the email is a reply or forward.
            to_addresses: List of recipient email addresses. One of to_addresses, cc_addresses, or bcc_addresses must be provided. Defaults to None
            cc_addresses: List of CC recipient email addresses. One of to_addresses, cc_addresses, or bcc_addresses must be provided. Defaults to None
            bcc_addresses: List of BCC recipient email addresses. One of to_addresses, cc_addresses, or bcc_addresses must be provided. Defaults to None
            reply_to_addresses: List of Reply-To email addresses. Defaults to None
            idempotency_key: Optional unique identifier for the email. If the same request is sent multiple times with the same key, only the first email will be sent. Defaults to None
            plain_text: Optional plain text content of the email. Can be None if the email is only available in HTML. Either plain_text or html must be provided.
            html: Optional HTML content of the email. Can be None if the email is only available in plain text. Either plain_text or html must be provided.
            alternative_content: If True, html and plain_text are alternative representations of the same content. If both are provided, this must be True. Defaults to False.
            existing_email_id: Optional BotMailRoom ID of the email to reply to or forward. None if this is a new email. Defaults to None
            message_type: Type of message ("new", "reply", or "forward"). Defaults to "new"
            attachment_ids: List of attachment IDs from the attachments pool to include in the email. Only this or attachments_raw can be provided. Defaults to None
            attachments_raw: List of tuples containing the filename, file bytes, and MIME type of each attachment to include in the email. Only this or attachment_ids can be provided. Defaults to None
            open_and_click_tracking: If `true`, the inbox will track opens and clicks for emails sent from the inbox. If None, the inbox's default setting will be used. Defaults to None

        Returns:
            The ID of the sent email
        """
        if (
            to_addresses is None
            and cc_addresses is None
            and bcc_addresses is None
        ):
            raise ValueError(
                "One of to_addresses, cc_addresses, or bcc_addresses must be provided"
            )

        if plain_text is None and html is None:
            raise ValueError("Either plain_text or html must be provided")

        if (
            plain_text is not None
            and html is not None
            and not alternative_content
        ):
            raise ValueError(
                "alternative_content must be True if both plain_text and html are provided"
            )

        if attachment_ids is not None and attachments_raw is not None:
            raise ValueError(
                "Only one of attachment_ids or attachments_raw can be provided"
            )

        if message_type != MessageType.new and existing_email_id is None:
            raise ValueError(
                "existing_email_id must be provided if message_type is not 'new'"
            )

        if subject is None and existing_email_id is None:
            raise ValueError(
                "subject must be provided if existing_email_id is None"
            )

        if attachments_raw is not None and len(attachments_raw) > 0:
            logger.info("Uploading attachments to attachments pool")
            attachment_coros = []
            for filename, file, content_type in attachments_raw:
                attachment_coros.append(
                    self.add_attachment_to_pool_async(
                        file, filename, content_type
                    )
                )
            attachment_ids = await asyncio.gather(*attachment_coros)
            logger.info(
                f"Uploaded {len(attachment_ids)} attachments to attachments pool"
            )

        payload: dict[str, Any] = {
            "inbox_id": inbox_id,
            "subject": subject,
            "idempotency_key": idempotency_key,
            "plain_text": plain_text,
            "html": html,
            "alternative_content": alternative_content,
            "existing_email_id": existing_email_id,
            "message_type": message_type,
            "open_and_click_tracking": open_and_click_tracking,
        }
        if to_addresses is not None:
            payload["to_addresses"] = [
                {"address": address, "name": None} for address in to_addresses
            ]
        if cc_addresses is not None:
            payload["cc_addresses"] = [
                {"address": address, "name": None} for address in cc_addresses
            ]
        if bcc_addresses is not None:
            payload["bcc_addresses"] = [
                {"address": address, "name": None} for address in bcc_addresses
            ]
        if reply_to_addresses is not None:
            payload["reply_to_addresses"] = [
                {"address": address, "name": None}
                for address in reply_to_addresses
            ]
        if attachment_ids is not None:
            payload["attachment_ids"] = attachment_ids

        url = os.path.join(self.base_url, "email", "send")
        response = await self._base_async_request(
            "POST",
            url,
            json=payload,
        )
        return response.json()["id"]

    def get_outbound_emails(
        self,
        search_term: Optional[str] = None,
        inbox_ids: Optional[list[str]] = None,
        limit: int = 100,
    ) -> list[OutboundEmailOverview]:
        """
        Get a list of all outbound emails for the user - only returns the metadata of the outbound emails

        Args:
            search_term: The search term to filter by. Filters across email content, subject, and attachment filenames. Defaults to None.
            inbox_ids: The inbox IDs to filter by. Defaults to None.
            limit: The maximum number of emails to return. Defaults to 100.

        Returns:
            A list of OutboundEmailOverview objects.
        """
        url = os.path.join(self.base_url, "email", "outbound")
        params: dict[str, Any] = {
            "limit": limit,
        }
        if search_term is not None:
            params["search_term"] = search_term
        if inbox_ids is not None:
            params["inbox_ids"] = inbox_ids
        response = self._base_sync_request("GET", url, params=params)
        return [OutboundEmailOverview(**email) for email in response.json()]

    async def get_outbound_emails_async(
        self,
        search_term: Optional[str] = None,
        inbox_ids: Optional[list[str]] = None,
        limit: int = 100,
    ) -> list[OutboundEmailOverview]:
        """
        Async version of get_outbound_emails

        Get a list of all outbound emails for the user - only returns the metadata of the outbound emails

        Args:
            search_term: The search term to filter by. Filters across email content, subject, and attachment filenames. Defaults to None.
            inbox_ids: The inbox IDs to filter by. Defaults to None.
            limit: The maximum number of emails to return. Defaults to 100.

        Returns:
            A list of OutboundEmailOverview objects.
        """
        url = os.path.join(self.base_url, "email", "outbound")
        params: dict[str, Any] = {
            "limit": limit,
        }
        if search_term is not None:
            params["search_term"] = search_term
        if inbox_ids is not None:
            params["inbox_ids"] = inbox_ids
        response = await self._base_async_request("GET", url, params=params)
        return [OutboundEmailOverview(**email) for email in response.json()]

    def get_outbound_email_content(self, email_id: str) -> EmailContent:
        """
        Get the metadata and content of an outbound email. Only attachment metadata is included, use the get_outbound_email_attachment method to get the raw attachment.

        Args:
            email_id: The ID of the outbound email to get the content of.

        Returns:
            An EmailContent object
        """
        url = os.path.join(self.base_url, "email", "outbound", email_id)
        response = self._base_sync_request("GET", url)
        return EmailContent(**response.json())

    async def get_outbound_email_content_async(
        self, email_id: str
    ) -> EmailContent:
        """
        Async version of get_outbound_email_content

        Get the metadata and content of an outbound email. Only attachment metadata is included, use the get_outbound_email_attachment method to get the raw attachment.

        Args:
            email_id: The ID of the outbound email to get the content of.

        Returns:
            An EmailContent object
        """
        url = os.path.join(self.base_url, "email", "outbound", email_id)
        response = await self._base_async_request("GET", url)
        return EmailContent(**response.json())

    def get_outbound_email_attachment(
        self, email_id: str, attachment_id: str
    ) -> bytes:
        """
        Get a raw attachment from an outbound email.

        Args:
            email_id: The ID of the outbound email to get the attachment from.
            attachment_id: The ID of the attachment to get.

        Returns:
            The raw attachment as bytes.
        """
        url = os.path.join(
            self.base_url,
            "email",
            "outbound",
            email_id,
            "attachment",
            attachment_id,
        )
        response = self._base_sync_request("GET", url)
        return response.content

    async def get_outbound_email_attachment_async(
        self, email_id: str, attachment_id: str
    ) -> bytes:
        """
        Async version of get_outbound_email_attachment

        Get a raw attachment from an outbound email.

        Args:
            email_id: The ID of the outbound email to get the attachment from.
            attachment_id: The ID of the attachment to get.

        Returns:
            The raw attachment as bytes.
        """
        url = os.path.join(
            self.base_url,
            "email",
            "outbound",
            email_id,
            "attachment",
            attachment_id,
        )
        response = await self._base_async_request("GET", url)
        return response.content

    def get_tools(
        self,
        tool_schema_type: ToolSchemaType = ToolSchemaType.openai,
        tools_to_include: Optional[list[str]] = None,
    ) -> list[dict]:
        """
        Get the tools in the correct format for the given tool schema type.

        Args:
            tool_schema_type: [`openai`, `claude`] The type of tool schema to use. Defaults to `openai`.
            tools_to_include: List of tool names to include. If None, all tools are included. Defaults to None.
                Available tools:
                    - `botmailroom_create_inbox`
                    - `botmailroom_send_email`
                    - `botmailroom_get_email`
                    - `botmailroom_get_email_content`
                    - `botmailroom_get_email_attachment`
                    - `botmailroom_get_domains`
                    - `botmailroom_get_inboxes`
                    - `botmailroom_wait_for_email`

        Returns:
            List of tools in the correct schema to pass to the LLM.
        """

        # retrieve tools from cache if available
        tools = self._tools[tool_schema_type]
        if tools is None:
            tools = self._base_sync_request(
                "GET",
                os.path.join(self.base_url, "tools"),
            ).json()
            self._tools[tool_schema_type] = tools

        # filter tools if requested
        if tools_to_include is not None:
            tools_to_use = []
            for tool in tools:
                if (
                    ToolSchemaType.claude == tool_schema_type
                    and tool["name"] in tools_to_include
                ):
                    tools_to_use.append(tool)
                elif (
                    ToolSchemaType.openai == tool_schema_type
                    and tool["function"]["name"] in tools_to_include
                ):
                    tools_to_use.append(tool)
        else:
            tools_to_use = tools
        return [tool for tool in tools_to_use]

    def wait_for_email(self, time_in_seconds: int) -> str:
        """
        Wait a certain amount of time before returning. Primarily used as a tool call.

        Args:
            time_in_seconds: The number of seconds to wait

        Returns:
            "done waiting"
        """
        sleep(time_in_seconds)
        return "done waiting"

    async def wait_for_email_async(self, time_in_seconds: int) -> str:
        """
        Async version of wait_for_email

        Wait a certain amount of time before returning. Primarily used as a tool call.

        Args:
            time_in_seconds: The number of seconds to wait

        Returns:
            "done waiting"
        """
        await asyncio.sleep(time_in_seconds)
        return "done waiting"

    def _serialize_tool_output(
        self,
        output: Union[str, BaseModel, list[BaseModel]],
        enforce_str_output: bool,
    ) -> Any:
        if enforce_str_output:
            # check if a pydantic object or list of pydantic objects
            if isinstance(output, list):
                if len(output) > 0 and isinstance(output[0], BaseModel):
                    return json.dumps([obj.model_dump() for obj in output])
            elif isinstance(output, BaseModel):
                return output.model_dump_json()
        return output

    def execute_tool(
        self, tool_name: str, tool_args: dict, enforce_str_output: bool = False
    ) -> Any:
        """
        Execute a tool call.

        Args:
            tool_name: The name of the tool to execute
            tool_args: The arguments to pass to the tool
            enforce_str_output: If True, the output will be converted to a JSON string if it is a pydantic object or list of pydantic objects. Defaults to False.

        Returns:
            The output of the tool
        """
        # remove botmailroom_prefix from tool_name
        tool_name = tool_name.replace("botmailroom_", "")
        output = getattr(self, tool_name)(**tool_args)
        return self._serialize_tool_output(output, enforce_str_output)

    async def execute_tool_async(
        self, tool_name: str, tool_args: dict, enforce_str_output: bool = False
    ) -> Any:
        """
        Async version of execute_tool

        Args:
            tool_name: The name of the tool to execute
            tool_args: The arguments to pass to the tool
            enforce_str_output: If True, the output will be converted to a JSON string if it is a pydantic object or list of pydantic objects. Defaults to False.

        Returns:
            The output of the tool
        """
        # remove botmailroom_prefix from tool_name
        tool_name = tool_name.replace("botmailroom_", "")

        # add async suffix to tool_name if not already present
        if not tool_name.endswith("_async"):
            tool_name = f"{tool_name}_async"
        output = await getattr(self, tool_name)(**tool_args)
        return self._serialize_tool_output(output, enforce_str_output)


class BotMailRoomWebhookVerificationError(Exception):
    pass


def verify_webhook_signature(
    signature_header: str,
    payload_bytes: bytes,
    webhook_secret: str,
    max_age: Optional[timedelta] = None,
) -> EmailPayload:
    """
    Verify the signature of a webhook payload.

    Args:
        signature_header: The signature header from the webhook request
        payload_bytes: The payload from the webhook request
        webhook_secret: The webhook secret for the inbox
        max_age: The maximum age of the payload. If None, no age check is performed. Defaults to None.

    Returns:
        The parsed payload
    """
    hash_object = hmac.new(
        webhook_secret.encode("utf-8"),
        msg=payload_bytes,
        digestmod=hashlib.sha256,
    )

    expected_signature = hash_object.hexdigest()
    signatures_match = hmac.compare_digest(
        expected_signature, signature_header
    )
    if not signatures_match:
        raise BotMailRoomWebhookVerificationError("Signature mismatch")

    payload = EmailPayload(**json.loads(payload_bytes))
    if max_age is not None:
        age = datetime.now() - datetime.fromisoformat(payload.timestamp)
        if age < timedelta(minutes=-1):
            # timestamp is in the future
            raise BotMailRoomWebhookVerificationError(
                "Timestamp is in the future"
            )
        if age > max_age:
            # timestamp is too old
            raise BotMailRoomWebhookVerificationError("Timestamp is too old")

    return payload
