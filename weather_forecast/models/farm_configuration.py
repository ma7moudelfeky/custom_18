from odoo import models, fields

class FarmConfiguration(models.Model):
    _name = 'farm.configuration'
    _description = 'Farm Configuration'
    _inherit = ['mail.thread']

    farm_id = fields.Many2one('farm.farm', string='Farm', required=True, tracking=True)
    longitude = fields.Float(string='Longitude', tracking=True, related='farm_id.longitude')
    latitude = fields.Float(string='Latitude', tracking=True, related='farm_id.latitude')
    api_key = fields.Char(string='API Key', tracking=True, related='farm_id.api_key')

    _sql_constraints = [
        ('unique_farm_id', 'unique(farm_id)', 'The farm has already been configured!')
    ]
