"""
Author: Arthur Elmes
Date: 2021-05-23
General strategy to get health data into correct CSV format

Most data have dates stored as unix utc epoch We want a csv with the cols: activity, start_date [, end_date]
Start with heart rate

    Initialize empty CSV with correct cols
    Walk through directory of jsons
    For each json, parse and extract heart_rate, heart_rate_max, heart_rate_min, start_time, and end_time 2.1 Each json may have an arbitrary number of dictionary-like entries, all of which we want 2.2 Time is stored as int with 3 extra trailing zeros
    Convert unix time to yyyy-mm-dd hh:mm:ss or similar
    Add each entry to output_csv


"""


def samsung_date_converter(date_int):
    samsung_time = int(date_int / 1000)
    #TODO subtract timezone... will require reading daylight/normal from file?
    return datetime.utcfromtimestamp(samsung_time).strftime('%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    from datetime import datetime
    import os
    import json
    import sys
    import csv

    workspace_hr = "D:/sync/samsunghealth_arthur.elmes_202012031516/ \
                    /jsons/com.samsung.shealth.tracker.heart_rate"

    for root, dirs, files in os.walk(workspace_hr):
        for file in files:
            if file.endswith('.json'):
                # content = json.loads(file)
                # print(content)

                with open(os.path.join(root, file), 'r') as f:
                    lines = f.readlines()
                    data_json = json.loads(lines[0])
                    for item in data_json:
                        hr = item['heart_rate']
                        hr_max = item['heart_rate_max']
                        hr_min = item['heart_rate_min']
                        st_time = samsung_date_converter(item['start_time'])
                        en_time = samsung_date_converter(item['end_time'])
                        with open(os.path.join(workspace_hr, 'heartrate.csv'), 'a', newline='') as data_csv:
                            # print(data_csv)
                            writer = csv.writer(data_csv)
                            writer.writerow((hr, hr_max, hr_min, st_time, en_time))
