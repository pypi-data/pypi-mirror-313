from enum import Enum
from typing import Optional

from pydantic import BaseModel


class ToolSchemaType(str, Enum):
    openai = "openai"
    claude = "claude"


class EmailStatus(str, Enum):
    valid = "valid"
    invalid_to_address = "invalid_to_address"
    not_allowed_from_address = "not_allowed_from_address"
    not_allowed_cc_address = "not_allowed_cc_address"
    not_allowed_bcc_address = "not_allowed_bcc_address"
    blocked_from_address = "blocked_from_address"
    spf_fail = "spf_fail"
    dkim_fail = "dkim_fail"
    dmarc_fail = "dmarc_fail"


class EmailAddress(BaseModel):
    address: str
    name: Optional[str]


class EmailWebhookLog(BaseModel):
    id: str
    status_code: Optional[int]
    response_body: Optional[str]
    created_at: str


class EmailOverview(BaseModel):
    id: str
    status: EmailStatus
    status_message: Optional[str]
    user_mark_status: bool
    inbox_id: str
    to_addresses: list[EmailAddress]
    cc_addresses: list[EmailAddress]
    bcc_addresses: list[EmailAddress]
    reply_to_addresses: list[EmailAddress]
    from_address: EmailAddress
    subject: str
    date: str
    latest_webhook_log: Optional[EmailWebhookLog]


class OutboundEmailEvent(BaseModel):
    event_type: str
    date: str


class OutboundEmailStatus(str, Enum):
    pending = "pending"
    sent = "sent"


class MessageType(str, Enum):
    forward = "forward"
    reply = "reply"
    new = "new"


class OutboundEmailOverview(BaseModel):
    id: str
    status: OutboundEmailStatus
    inbox_id: str
    to_addresses: list[EmailAddress]
    cc_addresses: list[EmailAddress]
    bcc_addresses: list[EmailAddress]
    reply_to_addresses: list[EmailAddress]
    from_address: EmailAddress
    subject: str
    date: str
    message_type: MessageType
    open_and_click_tracking: bool
    latest_event: Optional[OutboundEmailEvent]


class EmailAttachmentMetadata(BaseModel):
    filename: str
    content_type: str
    content_encoding: Optional[str]
    content_id: Optional[str]
    id: str


class EmailContent(BaseModel):
    id: str
    to_addresses: list[EmailAddress]
    from_address: EmailAddress
    cc_addresses: list[EmailAddress]
    bcc_addresses: list[EmailAddress]
    reply_to_addresses: list[EmailAddress]
    subject: str
    date: str
    plain_text: Optional[str]
    html: Optional[str]
    alternative_content: bool
    attachments: list[EmailAttachmentMetadata]
    previous_emails: Optional[list["EmailContent"]]
    prompt: str
    thread_prompt: str


class EmailPayload(EmailContent):
    timestamp: str


class WebhookAuthenticationType(str, Enum):
    signing_secret = "signing_secret"
    bearer_token = "bearer_token"


class ControlFromAddress(BaseModel):
    addresses: list[str]
    domains: list[str]


class Inbox(BaseModel):
    id: str
    name: str
    email_address: str
    allow_cc: bool
    allow_bcc: bool
    spf_pass_required: bool
    dkim_pass_required: bool
    dmarc_pass_required: bool
    allowed_from_addresses: Optional[ControlFromAddress]
    blocked_from_addresses: Optional[ControlFromAddress]
    webhook_url: Optional[str]
    webhook_authentication_type: Optional[WebhookAuthenticationType]
    updated_at: str
    webhook_secret_preview: Optional[str]


class InboxConfigurationResponse(BaseModel):
    id: str
    webhook_secret: Optional[str]


class DNSRecordStatus(str, Enum):
    success = "SUCCESS"
    pending = "PENDING"
    failed = "FAILED"
    not_started = "NOT_STARTED"
    temporary_failure = "TEMPORARY_FAILURE"


class DomainDNSRecord(BaseModel):
    type: str
    name: str
    value: str
    priority: Optional[int]
    status: DNSRecordStatus


class Domain(BaseModel):
    id: str
    domain: str
    dns_records: list[DomainDNSRecord]
    created_at: str
