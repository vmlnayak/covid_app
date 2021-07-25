import json
import pandas as pd
from django.utils import timezone
from datetime import timedelta
from email.mime.image import MIMEImage


def email_attach_image(email, img_content_id, image_data):
    """
    Attach Image to email message.
    """
    img = MIMEImage(image_data)
    img.add_header('Content-ID', '<%s>' % img_content_id)
    img.add_header('Content-Disposition', 'inline')
    email.attach(img)
    return email


def get_data_with_date_range(start_date, end_date, time_line):
    """
    This method will get covid data in accordance with date range.
    """
    if not (start_date and end_date):
        today = timezone.datetime.now()
        start_date = (today - timedelta(days=15)).strftime("%Y-%m-%d")
        end_date = today.strftime("%Y-%m-%d")

    data = pd.DataFrame(time_line)
    data['date'] = pd.to_datetime(data['date'])
    after_start_date = data["date"] >= start_date
    before_end_date = data["date"] <= end_date
    between_two_dates = after_start_date & before_end_date
    data = data.loc[between_two_dates]
    data['date'] = data['date'].dt.strftime("%Y-%m-%d")
    return json.loads(data.to_json(orient='records'))

