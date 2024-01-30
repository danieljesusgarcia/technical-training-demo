from odoo import fields, models
class EstateProperty(models.Model):
   _name = 'estate.property'
   name = fields.Char('Propietat Immobiliària', required=True)
   description = fields.Text('Descripció')
   postcode = fields.Char('Codi Postal')
   date_availability = fields.Date('Data de disponibilitat',copy=False)
   selling_price = fields.Float('Preu de venda')
   bedrooms = fields.Integer('Habitacions')
   active = fields.Boolean(default=True)
   state = fields.Selection([('New', 'Nou'), ('Offer Received', 'Oferta Rebuda'),('Offer Accepted', 'Oferta Acceptada'), ('Sold', 'Venuda'),('Canceled', 'Cancel·lada')],default='New',copy=False,required = True)   

