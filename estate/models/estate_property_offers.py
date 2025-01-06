from datetime import datetime
from odoo import api, fields, models, exceptions

class EstatePropertyOffers(models.Model):
    _name = "estate_property.offers"
    _table = "estate_property_offers"
    _description = "Estate Property Tag"

    price = fields.Float()
    status = fields.Selection([('accepted','Accepted'), ('refused', 'Refused'), ('recieved', 'Recieved')], copy=False, default='recieved')
    partner_id = fields.Many2one("res.partner")
    property_id = fields.Many2one("estate_property")
    validity = fields.Integer(default="7")
    date_deadline = fields.Date(compute="_compute_date", inverse="_inverse_date")
    create_date = fields.Date(default=fields.Date.today(), readonly=True)

    _sql_constraints = [
        ('positive_price', 'CHECK(price > 0)', 'The offer should be strictly positive'),
    ]

    @api.depends("validity")
    def _compute_date(self):
        for record in self:
            record.date_deadline = fields.Date.add(record.create_date, days=record.validity)

    def _inverse_date(self):
        d1=datetime.strptime(str(self.create_date),'%Y-%m-%d') 
        for record in self:

            d2=datetime.strptime(str(self.date_deadline),'%Y-%m-%d')
            record.validity = (d2-d1).days

    def accept_offer(self):
        if self.property_id.status == 'Offer Accepted':
            raise exceptions.UserError(f"Another offer was accepted.\nOffer of ${self.property_id.selling_price} by {self.property_id.buyer.name}")
        elif self.property_id.status == 'Sold':
            raise exceptions.UserError("Property already sold")
        
        self.property_id.status = 'Offer Accepted'
        self.status = "accepted"
        self.property_id.buyer = self.partner_id
        self.property_id.selling_price = self.price
            

    def reject_offer(self):
        for record in self:
            if record.status == "accepted":
                self.property_id.status = 'OfferReceieved'
                self.property_id.buyer = None
                self.property_id.selling_price = 0
            record.status = "refused"