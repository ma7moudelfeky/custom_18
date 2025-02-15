from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class FarmFarm(models.Model):
    _name = 'farm.farm'
    _description = 'Farm'
    _inherit = ['mail.thread']

    name = fields.Char(string='Farm', tracking=True)
    longitude = fields.Float(string='Longitude', tracking=True, required=True, )
    latitude = fields.Float(string='Latitude', tracking=True, required=True, )
    api_key = fields.Char(string='API Key', tracking=True, required=True, )
    farm_user = fields.Many2one('res.users', string='Weather User')

    @api.constrains('longitude', 'latitude')
    def _check_coordinates(self):
        for record in self:
            if record.longitude == 0.0 or record.latitude == 0.0:
                raise ValidationError(_("Longitude and Latitude cannot be 0.00."))

    _sql_constraints = [
        ('check_longitude_latitude', 'CHECK (longitude <> 0.0 AND latitude <> 0.0)',
         'Longitude and Latitude cannot be 0.00.')
    ]


