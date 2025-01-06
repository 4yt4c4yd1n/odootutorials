from odoo import api, fields, models, exceptions, tools

class TestModel(models.Model):
    _name = "estate_property"
    _description = "Test Model"

    name = fields.Char(required=True, default="Unknown")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([('north','North'), ('west', 'West'), ('south','South'), ('east','East')])
    last_seen = fields.Datetime("Last Seen", default=fields.Datetime.now, readonly=True)
    active = fields.Boolean(default=True)
    status = fields.Selection([('New','New'), ('OfferReceieved', 'Offer Recieved'), ('Offer Accepted','Offer Accepted'), ('Sold','Sold'), ('Cancelled','Cancelled')])
    property_type_id = fields.Many2one("estate_property_type")
    salesman = fields.Many2one("res.users")
    buyer = fields.Many2one("res.partner", readonly=True)
    tag_ids = fields.Many2many("estate_property_tag")
    offer_ids = fields.One2many("estate_property.offers", "property_id")
    property_type_id = fields.Many2one("estate_property_type", string="Property Type", readonly=True)
    sequence = fields.Integer("Sequence", default=10)

    _sql_constraints = [
        ('positive_price', 'CHECK(expected_price > 0)', 'The expected price should be strictly positive'),
    ]


    # I disagree that the selling price can't be 0
    @api.constrains('selling_price')
    def _check_selling_price(self):
        if self.status == 'Offer Accepted' and tools.float_compare(self.selling_price, self.expected_price*0.9, precision_rounding=5) <= 0:
            raise exceptions.ValidationError("No lowballs")

    total_area = fields.Integer(compute="_compute_total")

    @api.depends("total_area")
    def _compute_total(self):
        for record in self:
            record.total_area = self.living_area + self.garden_area

    best_price = fields.Integer(compute="_compute_best", default="0", store=True)

    @api.depends("best_price")
    def _compute_best(self):
        for record in self:
            for offer in record.offer_ids:
                record.best_price = offer.price if record.best_price < offer.price else record.best_price

    @api.onchange("garden")
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = "north"
            else:
                record.garden_area = None
                record.garden_orientation = None

    def mark_as_sold(self):
        for record in self:
            if record.status == "Cancelled":
                raise exceptions.UserError("Cancelled properties cannot be sold")
            record.status = "Sold"
        return True
    
    def mark_as_cancelled(self):
        for record in self:
            if record.status == "Sold":
                raise exceptions.UserError("Sold properties cannot be cancelled")
            record.status = "Cancelled"
        return True