import os
import email
import imaplib

from datetime import datetime

from django.conf import settings


ATTACHMENTS_DIR = os.path.join(settings.BASE_DIR, "tmp", "email_attachments")

XML_CONTENT_TYPE = (
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)


class GMailMessage(object):
    def __init__(self, msg_id, msg):
        self._msg_id = msg_id
        self._msg = msg

    def has_attachments(self):
        return self._msg.is_multipart()

    def get_datetime(self):
        date_str = self._msg.get("date")

        if not date_str:
            return None

        date_data = email.utils.parsedate_tz(date_str)

        if not date_data:
            return None

        return datetime.fromtimestamp(email.utils.mktime_tz(date_data))

    def get_attachments(self, content_types):
        if not self.has_attachments():
            return []

        for part in self._msg.walk():
            if part.get_content_type() in content_types:
                open(part.get_filename(), "wb").write(
                    part.get_payload(decode=True)
                )

            if (
                part.get_content_maintype() == "multipart"
                or part.get("Content-Disposition") is None
                or not part.get_filename()
            ):
                continue

            file_name = part.get_filename()
            file_path = os.path.join(ATTACHMENTS_DIR, file_name)

            if not os.path.isfile(file_path):
                fp = open(file_path, "wb")
                fp.write(part.get_payload(decode=True))
                fp.close()

            try:
                os.remove(part.get_filename())
            except Exception as e:
                print("Failed to remove temporary file: {}".format(e))

            yield {"name": file_name, "path": file_path}


class GMailInbox(object):
    def __init__(self, login, password):
        imap = imaplib.IMAP4_SSL("imap.gmail.com")
        imap.login(login, password)
        imap.select("inbox")

        self._imap = imap

    def find(self, **kwargs):
        query_parts = []

        if "from_uid" in kwargs:
            query_parts.append("UID {}:*".format(kwargs["from_uid"]))

        if "sender" in kwargs:
            query_parts.append('FROM "{}"'.format(kwargs["sender"]))

        print(query_parts)
        print(" ".join(query_parts))

        result, data = self._imap.uid("search", None, " ".join(query_parts))

        if result != "OK":
            raise Exception("Bad response: {}".format(result))

        with_attachments = kwargs.get("with_attachments")

        for msg_id in data[0].split():
            result, data = self._imap.uid("fetch", msg_id, "(RFC822)")

            if result != "OK":
                raise Exception("Can not read message: {}".format(result))

            msg = email.message_from_bytes(data[0][1])

            message = GMailMessage(msg_id, msg)

            if (
                with_attachments is not None
                and with_attachments
                and not message.has_attachments()
            ):
                continue

            yield message

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.close()

    def close(self):
        self._imap.close()
        self._imap.logout()
