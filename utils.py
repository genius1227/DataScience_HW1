import json
import pandas as pd
import numpy as np

#create temperature.csv with weather information
def create_tem_csv():
    f = open('C-B0024-002.json',encoding="utf-8")
    json_data = json.load(f)
    average = 0.0
    df_dict = {}
    idx = 0
    ds_list = []
    for i in json_data['cwbopendata']['dataset']['location']:
        idx += 1
        tmp_list = []
        loc_name  = i['locationName'].split(',')[0]
        day_time = 0
        day_average_tmp = 0.0
        for n in i['weatherElement'][0]['time']:
            day_time += 1
            day_average_tmp += float(n['weatherElement'][1]['elementValue']['value'])
            if day_time == 24:
                if idx == 1:
                    ds_list.append(n['obsTime'].split(' ')[0].replace('-', ''))
                tmp_list.append(round(day_average_tmp / 24, 1))
                day_average_tmp = 0.0
                day_time = 0

        if idx == 1:
            df_dict['ds'] = ds_list
        if len(tmp_list) < 366:
            for x in range(366-len(tmp_list)):
                tmp_list.append('')
        df_dict[loc_name] = tmp_list
        print(loc_name)

    pdtest = pd.DataFrame(df_dict)
    pdtest.to_csv('./temperature.csv', index=False)


#create new_temperature.csv with weather forecast
f = open('whether_forecast.json',encoding="utf-8")
json_data = json.load(f)

idx = True
day_list = []
output_list = []
for i in json_data['cwbdata']['resources']['resource']['data']['agrWeatherForecasts']['weatherForecasts']['location']:
    tmp_list = []
    for day in range(7):
        if idx == True:
            day_list.append(i['weatherElements']['MaxT']['daily'][day]['dataDate'].replace('-', ''))
        tmp_list.append( round(( float(i['weatherElements']['MaxT']['daily'][day]['temperature']) + float(i['weatherElements']['MinT']['daily'][day]['temperature'])) / 2, 2))
    idx = False
    output_list.append(tmp_list)

output_list = np.array(output_list)
output_list = np.insert(output_list[:3], -1, values=np.around(np.mean(output_list[3:], axis=0), decimals=1), axis=0)
ds = pd.DataFrame(day_list, columns=['ds'])
df = pd.DataFrame(output_list.T, columns=['North', 'Mid', 'South', 'East'])
df = pd.concat([ds, df], axis=1)

tmp_csv = pd.read_csv('temperature.csv')
tmp_csv = pd.concat([tmp_csv, df], ignore_index=True)
tmp_csv.to_csv('./new_temperature.csv', index=False)