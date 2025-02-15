from odoo import models, fields, api, _
from datetime import timedelta
import requests


class FarmWeatherData(models.Model):
    _name = 'farm.weather.data'
    _description = 'Farm Weather Data'
    _inherit = ['mail.thread']

    farm_id = fields.Many2one('farm.farm', string='Farm')
    date = fields.Date(string='Date', tracking=True)  # التاريخ
    temp = fields.Char(string='Temperature', tracking=True)  # درجة الحرارة
    humidity = fields.Char(string='Humidity', tracking=True)  # الرطوبة
    weather_description = fields.Char(string='Weather Description', tracking=True)  # الوصف
    sunrise = fields.Char(string='Sunrise Time', tracking=True)  # شروق الشمس
    sunset = fields.Char(string='Sunset Time', tracking=True)  # غروب الشمس
    wind_speed = fields.Char(string='Wind Speed', tracking=True)  # سرعة الرياح
    wind_direction = fields.Char(string='Wind Direction', tracking=True)  # اتجاه الرياح
    precip = fields.Char(string='Precip', tracking=True)  # الامطار
    precip_probability = fields.Char(string='precip forecast', tracking=True)  # احتمالية الامطار
    snow = fields.Char(string='Snow', tracking=True)  # الثلوج
    uv_index = fields.Char(string='UV Index', tracking=True)  # مؤشر الأشعة فوق البنفسجية
    cloud_cover = fields.Char(string='Cloud Cover', tracking=True)  # تغطية السحب
    dew = fields.Char(string='Dew', tracking=True)  # درجة الندى
    visibility = fields.Char(string='Visibility', tracking=True)  # الرؤية
    pressure = fields.Char(string='Pressure', tracking=True)  # الضغط الجوي
    full_name = fields.Char(string='Full Name', compute='_compute_full_name', store=True)

    disable_temp = fields.Boolean(string='Disable Temperature', tracking=True)  # درجة الحرارة
    disable_humidity = fields.Boolean(string='Disable Humidity', tracking=True)  # الرطوبة
    disable_weather_description = fields.Boolean(string='Disable Weather Description', tracking=True)  # الوصف
    disable_sunrise = fields.Boolean(string='Disable Sunrise Time', tracking=True)  # شروق الشمس
    disable_sunset = fields.Boolean(string='Disable Sunset Time', tracking=True)  # غروب الشمس
    disable_wind_speed = fields.Boolean(string='Disable Wind Speed', tracking=True)  # سرعة الرياح
    disable_wind_direction = fields.Boolean(string='Disable Wind Direction', tracking=True)  # اتجاه الرياح
    disable_precip = fields.Boolean(string='Disable Precipitation', tracking=True)  # الأمطار
    disable_precip_probability = fields.Boolean(string='Disable Precipitation Probability',
                                                tracking=True)  # احتمالية الأمطار
    disable_snow = fields.Boolean(string='Disable Snow', tracking=True)  # الثلوج
    disable_uv_index = fields.Boolean(string='Disable UV Index', tracking=True)  # مؤشر الأشعة فوق البنفسجية
    disable_cloud_cover = fields.Boolean(string='Disable Cloud Cover', tracking=True)  # تغطية السحب
    disable_dew = fields.Boolean(string='Disable Dew Point', tracking=True)  # درجة الندى
    disable_visibility = fields.Boolean(string='Disable Visibility', tracking=True)  # الرؤية
    disable_pressure = fields.Boolean(string='Disable Atmospheric Pressure', tracking=True)  # الضغط الجوي
    weather_data_hour_line_ids = fields.One2many('farm.weather.data.hours.line', 'farm_weather_data_id',
                                                 string='Hour Data Lines')

    @api.depends('farm_id.name', 'date')
    def _compute_full_name(self):
        for record in self:
            if record.farm_id.name and record.date:
                record.full_name = f"{record.farm_id.name} - {record.date}"
            else:
                record.full_name = record.farm_id.name or record.date

    def action_get_weather_data(self):
        for record in self:
            config = self.env['farm.configuration'].search([('farm_id', '=', record.farm_id.id)], limit=1)
            if config:
                api_key = config.api_key
                if not api_key:
                    return {'error': 'There is No Api Key Configured To This Farm'}
                latitude = config.latitude
                if not latitude:
                    return {'error': 'There is No Latitude Configured To This Farm'}
                longitude = config.longitude
                if not longitude:
                    return {'error': 'There is No Longitude Configured To This Farm'}

                # Prepare the API request URL
                url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{latitude},{longitude}/{record.date}?key={api_key}"
                response = requests.get(url)

                if response.status_code == 200:
                    weather_data = response.json()

                    if 'days' in weather_data and weather_data['days']:
                        day_data = weather_data['days'][0]

                        # Convert temperature from Fahrenheit to Celsius
                        temp_fahrenheit = day_data.get('temp', 0.0)
                        temp_celsius = (temp_fahrenheit - 32) * 5 / 9
                        record.temp = f"{round(temp_celsius, 2)} °C"  # Add °C symbol to temperature
                        record.humidity = f"{day_data.get('humidity', 0.0)} %"  # Add % symbol to humidity
                        record.sunrise = f"{day_data.get('sunrise', 0.0)} AM"
                        record.sunset = f"{day_data.get('sunset', 0.0)} AM"
                        record.weather_description = day_data.get('description', 'No description')
                        record.wind_speed = day_data.get('windspeed', 0.0)
                        record.wind_direction = day_data.get('winddir', 0.0)
                        record.precip = day_data.get('precip', 0.0)
                        record.precip_probability = day_data.get('precipprob', 0.0)
                        record.snow = day_data.get('snow', 0.0)
                        record.uv_index = day_data.get('uvindex', 0.0)
                        record.cloud_cover = day_data.get('cloudcover', 0.0)
                        record.dew = day_data.get('dew', 0.0)
                        record.visibility = day_data.get('visibility', 0.0)
                        record.pressure = day_data.get('pressure', 0.0)

                        if 'hours' in day_data:
                            for hour_data in day_data['hours']:
                                temp_fahrenheit = hour_data.get('temp', 0.0)
                                temp_celsius = (temp_fahrenheit - 32) * 5 / 9
                                date_time_str = str(hour_data.get('datetime', 0.0))

                                # Remove any existing record with the same farm_weather_data_id and date_time
                                self.env['farm.weather.data.hours.line'].search([
                                    ('farm_weather_data_id', '=', record.id),
                                    ('date_time', '=', date_time_str)
                                ]).unlink()

                                self.env['farm.weather.data.hours.line'].create({
                                    'farm_weather_data_id': record.id,
                                    'date_time': str(hour_data.get('datetime', 0.0)),
                                    'temp': str(round(temp_celsius, 2)),
                                    # Convert to Celsius and round it to 2 decimal places
                                    'humidity': str(hour_data.get('humidity', 0.0)),
                                    'wind_speed': str(hour_data.get('windspeed', 0.0)),
                                    'wind_direction': str(hour_data.get('winddir', 0.0)),
                                    'precip': str(hour_data.get('precip', 0.0)),
                                    'precip_probability': str(hour_data.get('precipprob', 0.0)),
                                    'snow': str(hour_data.get('snow', 0.0)),
                                    'uv_index': str(hour_data.get('uvindex', 0.0)),
                                    'cloud_cover': str(hour_data.get('cloudcover', 0.0)),
                                    'dew': str(hour_data.get('dew', 0.0)),
                                    'visibility': str(hour_data.get('visibility', 0.0)),
                                    'pressure': str(hour_data.get('pressure', 0.0)),
                                })

                        else:
                            raise ValueError(_('No Returned Hours'))

                        return weather_data
                    else:
                        return {'error': 'No daily weather data found for the given date'}
                else:
                    return {
                        'error': 'Failed to fetch weather data. The API key may be incorrect or there is an issue with the website'}
            else:
                return {'error': 'No configuration found for this farm'}

    @api.model
    def cron_fetch_weather_data(self):
        today = fields.Date.today()

        # Get all farm configurations
        farm_configs = self.env['farm.configuration'].search([])

        for config in farm_configs:
            farm = config.farm_id
            if not farm:
                continue  # Skip if no related farm

            # Check if a record already exists for today
            existing_record = self.search([('farm_id', '=', farm.id), ('date', '=', today)], limit=1)

            if existing_record:
                new_date = today + timedelta(days=1)  # Use tomorrow's date if today’s record exists
            else:
                new_date = today  # Use today's date if no record exists

            # Create new weather data record
            new_record = self.create({
                'farm_id': farm.id,
                'date': new_date
            })

            if new_record:
                new_record.action_get_weather_data()
                print(f"Weather data fetched for {farm.name} on {new_date}")

    class FarmWeatherDataHoursLine(models.Model):
        _name = 'farm.weather.data.hours.line'
        _description = 'Farm Weather Data Hourly Line'

        farm_weather_data_id = fields.Many2one('farm.weather.data', string='Farm', required=True)
        date_time = fields.Char(string='Hour', tracking=True)  # الساعه
        temp = fields.Char(string='Temperature', tracking=True)  # درجة الحرارة
        humidity = fields.Char(string='Humidity', tracking=True)  # الرطوبة
        wind_speed = fields.Char(string='Wind Speed', tracking=True)  # سرعة الرياح
        wind_direction = fields.Char(string='Wind Direction', tracking=True)  # اتجاه الرياح
        precip = fields.Char(string='Precip', tracking=True)  # الامطار
        precip_probability = fields.Char(string='Precipitation Forecast', tracking=True)  # احتمالية الامطار
        snow = fields.Char(string='Snow', tracking=True)  # الثلوج
        uv_index = fields.Char(string='UV Index', tracking=True)  # مؤشر الأشعة فوق البنفسجية
        cloud_cover = fields.Char(string='Cloud Cover', tracking=True)  # تغطية السحب
        dew = fields.Char(string='Dew', tracking=True)  # درجة الندى
        visibility = fields.Char(string='Visibility', tracking=True)  # الرؤية
        pressure = fields.Char(string='Pressure', tracking=True)  # الضغط الجوي
