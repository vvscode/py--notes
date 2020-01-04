import os
import gzip
import datetime

print('Start working')

logs = os.listdir('logs')

today_date = datetime.date.today()

all_dates = []
for i in range(30):
    new_date = today_date - datetime.timedelta(i)
    new_date_string = new_date.strftime("%d/%b/%Y")
    all_dates.append(new_date_string)
print(all_dates)


def analyzer(line):
    if 'Googlebot' not in line:
        return
    if not any([dat in line for dat in all_dates]):
        return
    log_data = line.split()
    print(log_data)
    ip = log_data[0]
    url = log_data[6]
    scaned = log_data[3][1:]

    with open('results.csv', 'a') as f:
        f.write(f'{ip}\t{scaned}\t{url}\n')


for log in logs:
    if '.gz' in log:
        with gzip.open(f'logs/{log}', 'rb') as f:
            for line in f:
                line = line.decode()
                analyzer(line)
    else:
        with open(f'logs/{log}', 'r') as f:
            for line in f:
                analyzer(line)

print('Logs analyzing DONE!')
