from odoo import models, fields, api
from odoo.exceptions import ValidationError


class FarmWeatherDataFieldsConfig(models.Model):
    _name = 'farm.weather.data.fields.config'
    _description = 'Farm Weather Data Fields Configuration'
    _inherit = ['mail.thread']

    farm_id = fields.Many2one('farm.farm', string='Farm', required=True)

    temp = fields.Boolean(string='Disable Temperature', tracking=True)  # درجة الحرارة
    humidity = fields.Boolean(string='Disable Humidity', tracking=True)  # الرطوبة
    weather_description = fields.Boolean(string='Disable Weather Description', tracking=True)  # الوصف
    sunrise = fields.Boolean(string='Disable Sunrise Time', tracking=True)  # شروق الشمس
    sunset = fields.Boolean(string='Disable Sunset Time', tracking=True)  # غروب الشمس
    wind_speed = fields.Boolean(string='Disable Wind Speed', tracking=True)  # سرعة الرياح
    wind_direction = fields.Boolean(string='Disable Wind Direction', tracking=True)  # اتجاه الرياح
    precip = fields.Boolean(string='Disable Precipitation', tracking=True)  # الأمطار
    precip_probability = fields.Boolean(string='Disable Precipitation Probability', tracking=True)  # احتمالية الأمطار
    snow = fields.Boolean(string='Disable Snow', tracking=True)  # الثلوج
    uv_index = fields.Boolean(string='Disable UV Index', tracking=True)  # مؤشر الأشعة فوق البنفسجية
    cloud_cover = fields.Boolean(string='Disable Cloud Cover', tracking=True)  # تغطية السحب
    dew = fields.Boolean(string='Disable Dew Point', tracking=True)  # درجة الندى
    visibility = fields.Boolean(string='Disable Visibility', tracking=True)  # الرؤية
    pressure = fields.Boolean(string='Disable Atmospheric Pressure', tracking=True)  # الضغط الجوي

    _sql_constraints = [
        ('unique_farm_id', 'unique(farm_id)', 'Each farm can only have one weather data fields configuration!')
    ]

    @api.constrains('farm_id')
    def _check_unique_farm_id(self):
        for record in self:
            existing_config = self.search([('farm_id', '=', record.farm_id.id), ('id', '!=', record.id)])
            if existing_config:
                raise ValidationError('Each farm can only have one weather data configuration!')

    @api.onchange(
        'temp', 'humidity', 'weather_description', 'sunrise', 'sunset',
        'wind_speed', 'wind_direction', 'precip', 'precip_probability',
        'snow', 'uv_index', 'cloud_cover', 'dew', 'visibility', 'pressure'
    )
    def _onchange_sync_farm_fields(self):
        if self.farm_id:
            # Correct the search query by accessing self.farm_id.id
            farm_weather_data_ids = self.env['farm.weather.data'].search([('farm_id', '=', self.farm_id.id)]).ids

            if farm_weather_data_ids:
                for rec in self.env['farm.weather.data'].browse(farm_weather_data_ids):
                    rec.disable_temp = self.temp
                    rec.disable_humidity = self.humidity
                    rec.disable_weather_description = self.weather_description
                    rec.disable_sunrise = self.sunrise
                    rec.disable_sunset = self.sunset
                    rec.disable_wind_speed = self.wind_speed
                    rec.disable_wind_direction = self.wind_direction
                    rec.disable_precip = self.precip
                    rec.disable_precip_probability = self.precip_probability
                    rec.disable_snow = self.snow
                    rec.disable_uv_index = self.uv_index
                    rec.disable_cloud_cover = self.cloud_cover
                    rec.disable_dew = self.dew
                    rec.disable_visibility = self.visibility
                    rec.disable_pressure = self.pressure

