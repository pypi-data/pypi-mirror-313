### Examples:
Send email:
```
from djmail import mail_managers
mail_managers(
    _('New product price offer #{}').format(obj.id),
    render_to_string('offers/email.html', context)
)
```
Email template:
```
{% extends 'email.html' %}

{% load i18n %}


{% block content %}
    content...
{% endblock %}
```
