from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List


class EmailManager:
    status = False

    def __init__(self, **xtra_args):
        self._required_init_fields = set()
        self._required_init_fields.add("_username")
        self._required_init_fields.add("_send_emails")
        for field in self._required_init_fields:
            value = xtra_args.get(field, None)
            if value is None:
                raise ValueError(f"[{self.__class__.__name__}] Field {field} is required")
            setattr(self, field, value)

    @property
    def origin(self):
        return self._username

    @property
    def can_send_emails(self):
        return self._send_emails

    def init_connection(self, **kwargs):
        raise NotImplementedError("Method not implemented")

    def send_email(
        self,
        cc: List[str] = None,
        bcc: List[str] = None,
        attachment_path: List[str] = None,
        *,
        to: List[str],
        subject: str,
        body: str,
        body_subtype="plain",
    ):
        if attachment_path is None:
            attachment_path = []
        if bcc is None:
            bcc = []
        if cc is None:
            cc = []
        if not self.can_send_emails:
            return {}
        if not isinstance(attachment_path, list):
            raise ValueError("attachment_path must be a list")
        origin, to, content = self._generate_email_data(
            to=to,
            cc=cc,
            bcc=bcc,
            subject=subject,
            body=body,
            attachment_path=attachment_path,
            body_subtype=body_subtype,
        )
        response = self._send_email(origin, to, content)
        return response

    def _send_email(self, origin, to, content, **xtra_args):
        raise NotImplementedError("Method not implemented")

    def _generate_email_data(self, *, to, cc, bcc, subject, body, attachment_path=None, body_subtype):
        origin = self.origin
        if not isinstance(to, list):
            to = [to]
        msg = self._generate_MIME_content(origin=origin, to=to, cc=cc, bcc=bcc, subject=subject, body=body, body_subtype=body_subtype)
        msg = self._attach_file_to_MIME(msg, attachment_path)
        return origin, to + cc + bcc, msg

    def _generate_MIME_content(self, *, origin, to, cc, bcc, subject, body, body_subtype):
        msg = MIMEMultipart()
        msg["From"] = origin
        msg["To"] = ", ".join(to)
        msg["Cc"] = ", ".join(cc)
        msg["Subject"] = subject
        msg.attach(MIMEText(body, body_subtype))
        return msg

    def _attach_file_to_MIME(self, msg, attachments):
        if attachments:
            for file_attachment in attachments:
                with open(file_attachment, "rb") as file:
                    attachment = MIMEBase("application", "octet-stream")
                    attachment.set_payload(file.read())
                encoders.encode_base64(attachment)
                filename = file_attachment.split("\\")[-1].split("/")[-1]
                attachment.add_header("Content-Disposition", f"attachment; filename= {filename}")
                msg.attach(attachment)
        return msg
