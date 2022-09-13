import re
import pandas as pd


def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    list1 = []
    for name in dates:
        if name[5] == '2' and name[6] == '1':
            v = name.replace('21,', '2021,')
            list1.append(v)
        if name[4] == '2' and name[5] == '1':
            v = name.replace('21,', '2021,')
            list1.append(v)
        if name[5] == '2' and name[6] == '2':
            v = name.replace('22,', '2022,')
            list1.append(v)
        if name[4] == '2' and name[5] == '2':
            v = name.replace('22,', '2022,')
            list1.append(v)
        if name[6] == '2' and name[7] == '1':
            v = name.replace('21,', '2021,')
            list1.append(v)
    df = pd.DataFrame({'user_message': messages, 'message_date': list1})
    # convert message_date type

    df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%Y, %H:%M - ')
    df.rename(columns={'message_date': 'date'}, inplace=True)
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period
    return df