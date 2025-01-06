from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate_property_type"
    _description = "Estate Property Type"
    _order = "id desc"

    name = fields.Char(required=True, default="Unknown")
    property_ids = fields.One2many("estate_property", "property_type_id", string="Properties")
    

    _sql_constraints = [
        ('unique_type', 'UNIQUE(name)', 'Property type should be unique')
    ]
    