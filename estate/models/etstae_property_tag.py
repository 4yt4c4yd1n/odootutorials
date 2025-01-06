from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate_property_tag"
    _description = "Estate Property Tag"

    name = fields.Char(required=True, default="Unknown")
    color = fields.Integer()
    
    _sql_constraints = [
        ('unique_tag', 'UNIQUE(name)', 'Property tag should be unique')
    ]