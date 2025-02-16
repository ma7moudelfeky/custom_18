# -*- coding: utf-8 -*-
{
    'name': 'Weather Forecast',
    'version': '1.0',
    'summary': 'Excellent Solution Weather Forecast',
    'sequence': 1,
    'description': """
                    Weather Forecast
                    ====================
                    The Weather Forecast module integrates real-time weather data into Odoo using the visualcrossing website APIs.
                    It allows users to fetch and display current weather conditions, forecasts, and other meteorological information for specific locations.
                    """,
    'category': 'Weather',
    'author': "Excellent Solution",
    'maintainer': 'Eng Mohamed Momtaz',
    'support': 'eng.m.momtaz1@gmail.com',
    'depends': ['base', 'mail'],

    'data': [
        "security/farm_security.xml",
        "security/ir.model.access.csv",
        "views/farm_farm_views.xml",
        "views/farm_weather_data_views.xml",
        "views/farm_configuration_views.xml",
        "views/farm_weather_data__fields_config_views.xml",
        'data/ir_cron.xml',
    ],
    'license': 'LGPL-3',
}
