import pandas as pd
from geopy.distance import geodesic
from datetime import datetime, timedelta
import plotly.express as px
import requests
import os
import plotly.graph_objects as go


def calculate_distance(lat, lon, df_deviceid_file_path, distance, row_lat='lat', row_lon='lon', deviceid='device_id', sensor_type=None):
    # Read the device data from the CSV file
    df_deviceid = pd.read_csv(df_deviceid_file_path)
    
    # Drop rows with missing lat or lon values
    df_deviceid = df_deviceid.dropna(subset=[row_lat, row_lon], how='all')
    if sensor_type == 'air':
        df_deviceid = df_deviceid[df_deviceid['sensor'].str.contains('pm2_5', na=False)].reset_index(drop=True)
        
    # Ensure latitude and longitude values are within valid ranges
    min_lat = -90
    max_lat = 90
    min_lon = -180
    max_lon = 180
    df_deviceid[row_lat] = df_deviceid[row_lat].apply(lambda x: min(max(min_lat, x), max_lat))
    df_deviceid[row_lon] = df_deviceid[row_lon].apply(lambda x: min(max(min_lon, x), max_lon))

    # Create a function to calculate the distance
    def calculate_distance_row(row):
        device_location = (row[row_lat], row[row_lon])
        target_location = (lat, lon)
        distance = geodesic(device_location, target_location).kilometers
        return distance

    # Add a column to store the distances
    df_deviceid['distance_km'] = df_deviceid.apply(calculate_distance_row, axis=1)

    # Filter out data within one kilometer
    filtered_df = df_deviceid[df_deviceid['distance_km'] <= distance]

    # Get the list of device IDs
    lst_device_id = filtered_df[deviceid].to_list()

    return lst_device_id

def filter_data_for_device(result_lst_device_id, time, df_device_file_path, row_time='localTime', row_deviceid='deviceId', sensor='pm2_5', ten_minutes_before_after=4):
    def get_date_hour_min(time_diff, base_time):
        # 計算新時間
        new_time = base_time + timedelta(minutes=time_diff)

        # 格式化日期和時間
        str_date = new_time.strftime("%Y-%m-%d")
        str_hour = new_time.strftime("%H")
        str_minute = new_time.strftime("%M")[0]

        return str_date, str_hour, str_minute

    def filter_time(df, time):
        user_input_time = pd.to_datetime(time)
        half_hour_offset = pd.DateOffset(minutes=30)
        start_time = user_input_time - half_hour_offset
        end_time = user_input_time + half_hour_offset
        df[row_time] = pd.to_datetime(df[row_time])
        filtered_data = df[(df[row_time] >= start_time) & (df[row_time] <= end_time)].reset_index(drop=True)
        return filtered_data

    def filter_deviceid(df, result_lst_device_id):
        df = df[df[row_deviceid].isin(result_lst_device_id)].reset_index(drop=True)
        return df

    df_all = pd.DataFrame()
    base_time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')

    for i in range(-10 * ten_minutes_before_after, 10 * ten_minutes_before_after, 10):
        str_date, str_hour, str_minute = get_date_hour_min(i, base_time)
        str_url = f'{df_device_file_path}/{str_date}/10mins_{str_date}_{str_hour}_{str_minute}.csv.gz'
        try:
            df = pd.read_csv(str_url, compression='gzip')
            df_all = pd.concat([df_all, df], ignore_index=True)
        except:
            pass
    df_all = filter_time(df_all, time)
    df_all = filter_deviceid(df_all, result_lst_device_id)
    df_all = df_all[df_all['sensorId'] == sensor].reset_index(drop=True)
    return df_all
    

def create_custom_color_scale(color_dict):
    scale = []
    max_value = max(item['v'] for item in color_dict)  # 獲取最大數值
    for item in color_dict:
        # 將每個色彩值對應到其數值範圍（從0到1之間），並反轉色彩順序
        scale.append([item['v'] / max_value, item['color']])
    return scale[::-1]  # 反轉色彩尺度列表


def find_color_for_value(value, color_dict):
    for color_info in sorted(color_dict, key=lambda x: x['v']):
        if value <= color_info['v']:
            return color_info['color']
    return '#FFFFFF'  # 如果沒有合適的顏色，使用白色作為預設值


def create_pm25_map(df, lat, lon, file_path, row_value='value', row_deviceId='deviceId', row_lat='lat', row_lon='lon',
                    row_time='localTime', labeled_center_lat_lon=True, plot_animation=False):
    df[row_value] = df[row_value].astype(float)
    # Filter data
    if not plot_animation:
        df = df.loc[df.groupby(row_deviceId)[row_value].idxmax()]

    pm2_5_color_dict = [
        {"v": 500.4, "color": "#000000"},
        {"v": 450.5, "color": "#301E12"},
        {"v": 400.5, "color": "#3C230F"},
        {"v": 350.5, "color": "#49280D"},
        {"v": 300.5, "color": "#552E0A"},
        {"v": 250.5, "color": "#623307"},
        {"v": 230.5, "color": "#682c1f"},
        {"v": 210.5, "color": "#6d2537"},
        {"v": 190.5, "color": "#731d4e"},
        {"v": 170.5, "color": "#781666"},
        {"v": 150.5, "color": "#7e0f7e"},
        {"v": 131.3, "color": "#970f6a"},
        {"v": 112.1, "color": "#b10f56"},
        {"v": 92.9, "color": "#ca0e43"},
        {"v": 73.7, "color": "#e30e30"},
        {"v": 54.5, "color": "#fc0e1c"},
        {"v": 50.7, "color": "#fc241d"},
        {"v": 46.9, "color": "#fc3b1f"},
        {"v": 43.1, "color": "#fd5220"},
        {"v": 39.3, "color": "#fd6822"},
        {"v": 35.5, "color": "#fd7e23"},
        {"v": 31.5, "color": "#fd9827"},
        {"v": 27.5, "color": "#feb12b"},
        {"v": 23.5, "color": "#fecb30"},
        {"v": 19.5, "color": "#ffe534"},
        {"v": 15.5, "color": "#fffd38"},
        {"v": 12.4, "color": "#d4fd36"},
        {"v": 9.3, "color": "#a9fd34"},
        {"v": 6.2, "color": "#7EFD32"},
        {"v": 3.1, "color": "#53FD30"},
        {"v": 0, "color": "#29fd2e"}
    ]
    custom_color_scale = create_custom_color_scale(pm2_5_color_dict)

    df = df.sort_values(by=['localTime']).reset_index(drop=True)
    start_time = df['localTime'].min()
    end_time = df['localTime'].max()
    title_text = f"地圖展示自 {start_time} 到 {end_time} 間各監測站點PM2.5濃度的最高值及發生時間，中間以藍框標記的點位為你所關注的地點"

    # Create scatter mapbox
    if not plot_animation:
        fig = px.scatter_mapbox(df, lat=row_lat, lon=row_lon, color=row_value, range_color=(0, 500.4),
                                hover_data=[row_time, row_deviceId, row_value], zoom=7, size=[15] * len(df[row_lat]),
                                size_max=15, color_continuous_scale=custom_color_scale, title=f'此靜態{title_text}')
    else:
        fig = px.scatter_mapbox(df, lat=row_lat, lon=row_lon, color=row_value, range_color=(0, 500.4),
                                hover_data=[row_time, row_deviceId, row_value], zoom=7, size=[15] * len(df[row_lat]),
                                size_max=15, color_continuous_scale=custom_color_scale, title=f'此動態{title_text.replace("的最高","")}', animation_frame='localTime')

    fig.update_layout(mapbox_style='open-street-map')  # carto-positron

    if labeled_center_lat_lon:
        # Extract color for the specific point
        specific_point = df.query(f"{row_lat} == {lat} & {row_lon} == {lon}")
        if not specific_point.empty:
            specific_value = specific_point[row_value].iloc[0]
            specific_color = find_color_for_value(specific_value, pm2_5_color_dict)
        else:
            specific_color = '#FFFFFF'  # Default to white if no data

        # Add a blue border around the marker
        fig.add_trace(go.Scattermapbox(
            lat=[lat],
            lon=[lon],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=24,  # Slightly larger to create a border effect
                color='blue'  # Blue border
            )
        ))

        # Add the original data point on top of the border
        fig.add_trace(go.Scattermapbox(
            lat=[lat],
            lon=[lon],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=20,  # Original size
                color=specific_color  # Original or default color
            )
        ))

    initial_center = {"lat": lat, "lon": lon}  # Example coordinates
    initial_zoom = 14  # Example zoom level
    fig.update_layout(mapbox_center=initial_center, mapbox_zoom=initial_zoom)
    fig.update_layout(margin={'r': 0, 'l': 0, 'b': 0})
    # Save to html
    fig.write_html(file_path, include_plotlyjs=True)

    return file_path

def clean_data(data_dict, start_time, end_time):
    # 這裡確保傳入的是字典中的資料列表
    data_list = data_dict['data']

    # 過濾資料
    cleaned_data_list = [item for item in data_list if
                         start_time <= datetime.strptime(item['time'], "%Y-%m-%d %H:%M:%S") <= end_time]
    # 更新字典
    cleaned_data_dict = {
        'count': len(cleaned_data_list),
        'data': cleaned_data_list
    }

    return cleaned_data_dict

def get_cwb_wind_data(int_lat, int_lon, str_datetime):
    event_loc = (int_lat, int_lon)
    event_time = datetime.strptime(str_datetime, "%Y-%m-%d %H:%M:%S")

    # 建立一個特定時間點用於判斷
    time_threshold = datetime.strptime("2023-11-15 13:00:00", "%Y-%m-%d %H:%M:%S")

    time_clean_start_threshold = datetime.strptime("2023-11-15 00:00:00", "%Y-%m-%d %H:%M:%S")
    time_clean_end_threshold = datetime.strptime("2023-11-16 00:00:00", "%Y-%m-%d %H:%M:%S")

    t = (event_time + timedelta(minutes=-event_time.minute, seconds=-event_time.second))
    str_result = "無氣象署測站資料"
    for _ in range(3):
        start_time, end_time = t, (t + timedelta(hours=1))
        print('start_time', start_time)

        # 如果 start_time 或 end_time 大於設定的時間點，則減少 8 小時
        if start_time > time_threshold and end_time > time_threshold:
            start_time -= timedelta(hours=8)
            end_time -= timedelta(hours=8)

        formatted_start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
        formatted_end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")

        t = t - timedelta(hours=1)
        cwb_api = f'https://aiot.moenv.gov.tw/_/api/v2/epa_station/wind?fields=wind_direct%2Cwind_speed&sources=中央氣象局&min_lat=-90&max_lat=90&min_lon=-180&max_lon=180&start_time={formatted_start_time}&end_time={formatted_end_time}'
        response = requests.get(cwb_api)
        j = response.json()

        try:
            if event_time > time_clean_start_threshold and event_time < time_clean_end_threshold:
                j = clean_data(j, t, (t + timedelta(hours=2)))
        except:
            pass

        if len(j['data']) != 0:
            nearest_site, nearest_dist = None, None
            for i in range(len(j['data'])):
                site_loc = (j['data'][i]['lat'], j['data'][i]['lon'])
                dist = geodesic(event_loc, site_loc).km
                if nearest_dist is None or dist < nearest_dist:
                    nearest_site, nearest_dist = j['data'][i], dist
            str_result = f"以下為距離最近的氣象署測站資料:\n測站: {nearest_site['name']}(距離{nearest_dist:.2f}公里)\n資料時間: {nearest_site['time']}\n風向: {nearest_site['wind_direct']}\n風速: {nearest_site['wind_speed']}"
            break
        else:
            continue
    return str_result


def get_national_station_air_quality_data(start_time, end_time, area, fields='aqi,pm2_5'):
	start_time = start_time.replace(" ", "%20")
	end_time = end_time.replace(" ", "%20")
	area = area.replace("縣", "").replace("市", "").replace("臺", "台")
	api_url = f"https://aiot.moenv.gov.tw/_/api/v2/epa_station/rawdata?fields={fields}&start_time={start_time}&end_time={end_time}&area={area}"
	response = requests.get(api_url)

	return response.json()


if __name__ == '__main__':
    # Example of calculate_distance usage:
    lon = 121.3208
    lat = 25.046
    df_deviceid_file_path = '/Users/apple/Desktop/project_device_table_20231017.csv'
    result_lst_device_id = calculate_distance(lat, lon, df_deviceid_file_path, 1, sensor_type='air')
    print(result_lst_device_id)
    
    # Example of filter_data_for_device_time usage:
    df_device_file_path = '/Users/apple/Desktop/iot_data'
    time = '2023-11-15 08:35:00'
    df = filter_data_for_device(result_lst_device_id, time,df_device_file_path)
    print(df.localTime.min())
    print(df.localTime.max())
    print(df.columns)
    
    file_path = '/Users/apple/Desktop/test.html'
    url = create_pm25_map(df,lat, lon, file_path, row_value='value', row_deviceId='deviceId', row_lat='lat', row_lon='lon', row_time='localTime')
    print(url)
    
    str_wind_result = get_cwb_wind_data(lat, lon, time)
    print(str_wind_result)
