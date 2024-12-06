from odoo import models, fields

class EditorialProductPricelist(models.Model):
    """ Extend product pricelist model for editorial management """

    _description = "Editorial Product Pricelist"
    _inherit = 'product.pricelist'

    route_id = fields.Many2one('stock.location.route', string='Ruta')


    def is_deposit_pricelist(self):
        return self in self.get_deposit_pricelists()

    def get_deposit_pricelists(self):
        # Search for the deposit order route
        first_rule = self.env['stock.rule'].search([
            ('location_src_id', '=', self.env.ref("stock.stock_location_stock").id),
            ('location_id', '=', self.env.company.location_venta_deposito_id.id)
        ], limit=1)

        second_rule = self.env['stock.rule'].search([
            ('location_src_id', '=', self.env.company.location_venta_deposito_id.id),
            ('location_id', '=', self.env.ref("stock.stock_location_customers").id)
        ], limit=1)
        
        if first_rule and second_rule:
            route = self.env['stock.location.route'].search([
                ('rule_ids', 'in', [first_rule.id, second_rule.id])
            ], limit=1)

            if route:
                # Search for all the pricelist with deposit route
                pricelists = self.env['product.pricelist'].search([
                    ('route_id', '=', route.id)
                ])
                return pricelists

        return []