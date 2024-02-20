from odoo import fields, models
from odoo import api
from odoo.exceptions import UserError,ValidationError

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
   salesperson_id = fields.Many2one('res.users', string='Comercial')
   tag_ids = fields.Many2many('estate.property.tag', string='Etiquetes')
   offer_ids = fields.One2many('estate.property.offer','property_id', string='Ofertes')    
   avgPrice = fields.Float('Preu per m2',compute='_calcular_preu_per_metre')
   expected_selling_price = fields.Float('Preu esperat')
   area = fields.Float('Superfície')

   _sql_constraints = [
       ('check_positive_expected_selling_price', 'CHECK(expected_selling_price >= 0)',
        'El preu esperat ha de ser positiu.'),('check_more_than_1000_selling_price', 'CHECK(selling_price >= 1000)',
        'El preu de venda ha de ser més de 1000.')
   ]

   _sql_constraints = [                                                                                             
   ('name_uniq', 'unique(name)', "El nom d'una propietat ha de ser únic"),                                                                                                  
   ]

   @api.constrains('selling_price','expected_selling_price')
   def _check_selling_price_vs_expected(self):
       for record in self:
           if record.selling_price < record.expected_selling_price*0.9:
               raise ValidationError("El preu de venda no pot ser inferior al 90% del preu esperat")    
               
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

   @api.ondelete(at_uninstall=False)
   def _unlink_if_property_new_or_canceled(self):
       if any(property.state not in ([ 'New', 'Canceled']) for property in self):
           raise UserError("No es pot eliminar una propietat que no és nova o cancel·lada")       
