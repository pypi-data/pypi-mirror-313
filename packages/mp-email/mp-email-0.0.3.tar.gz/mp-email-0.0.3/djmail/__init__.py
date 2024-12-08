from django.conf import settings
from django.core import mail
from django.template.loader import render_to_string


def get_default_email_context():
    return {
        "domain": settings.DOMAIN,
        "debug": settings.DEBUG,
    }


def render_email(template, context=None):
    email_context = get_default_email_context()
    if context is not None:
        email_context.update(context)

    return render_to_string(template, email_context)


def mail_managers(subject, **kwargs):
    return send_mail(
        subject, [manager[1] for manager in settings.MANAGERS], **kwargs
    )


def send_mail(
    subject,
    recipient_list,
    html=None,
    template=None,
    context=None,
    attachments=None,
):
    email = mail.EmailMultiAlternatives(
        subject=subject.strip(),
        body="",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=recipient_list,
    )

    if attachments:
        for attachment in attachments:
            email.attach(*attachment)

    if html is None:
        html = render_email(template, context)

    email.attach_alternative(html, "text/html")
    email.send(fail_silently=False)

    return email
