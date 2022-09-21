import datetime
# convert the timestamp to datetime object with the UTC+10
def timestamp_to_datetime_with_timezone(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).replace(tzinfo=datetime.timezone.utc).astimezone(datetime.timezone(datetime.timedelta(hours=10)))

# test above function
print(timestamp_to_datetime_with_timezone(1579098983))


