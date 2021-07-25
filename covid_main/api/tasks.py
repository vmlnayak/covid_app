import uuid
import plotly.express as px
import pandas as pd
from celery import shared_task

from django.core.mail import EmailMultiAlternatives

from django.template.loader import render_to_string

from api.utils import email_attach_image

@shared_task
def email_image(time_line, to_email, name):
    """
    Generate Image based on data and send email as background job using celery task.
    :params
    time_line, to_email, name, return
    """
    df = pd.DataFrame(time_line)
    fig = px.bar(df, x="date", y="new_confirmed", title='Corona Case in India')
    image_data = fig.to_image(format="png")
    html_content = render_to_string("email.html", context={'name': name})
    email = EmailMultiAlternatives("Covid data graph.", 'Body', 'from@example.com', [to_email])
    email.attach_alternative(html_content, "text/html")
    email_attach_image(email, uuid.uuid4().hex, image_data)
    email.send()
