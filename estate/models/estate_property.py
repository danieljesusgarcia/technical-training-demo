from odoo import fields, models
from odoo import api
from odoo.exceptions import UserError

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
   buyer_id = fields.Many2one('res.partner', string='Comprador')
   tag_ids = fields.Many2many('estate.property.tag', string='Etiquetes')
   offer_ids = fields.One2many('estate.property.offer','property_id', string='Ofertes')    
   avgPrice = fields.Float('Preu per m2',compute='_calcular_preu_per_metre')
   expected_selling_price = fields.Float('Preu esperat')
   area = fields.Float('Superfície')


   @api.depends('expected_selling_price','area')
   def _calcular_preu_per_metre(self):
       for record in self:
           if record.area > 0 :
               record.avgPrice = record.expected_selling_price/record.area
           else:
               record.avgPrice = None

   def cancellarPropietat(self):
       for record in self:
           if not record.state == 'Sold':
               record.state = 'Canceled'
           else:
               raise UserError('No es pot cancel·lar una propietat venuda')
       return True
