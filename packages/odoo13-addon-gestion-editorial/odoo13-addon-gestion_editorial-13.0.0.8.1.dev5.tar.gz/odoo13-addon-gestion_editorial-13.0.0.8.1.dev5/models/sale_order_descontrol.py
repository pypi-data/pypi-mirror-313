from odoo import models, fields, api

class EditorialSaleOrder(models.Model):
    """ Extend sale.order template for editorial management """

    _description = "Editorial Sale Order"
    _inherit = 'sale.order'  # odoo/addons/sale/models/sale.py

    is_deposit_sale_order = fields.Boolean(
        compute='_compute_is_deposit_sale_order',
        string="Is deposit sale order"
    )

    is_client_default_pricelist = fields.Boolean(
        compute='_compute_is_client_default_pricelist',
    )

    @api.onchange("pricelist_id")
    def _compute_is_client_default_pricelist(self):
        for record in self:
            record.is_client_default_pricelist = (
                self.pricelist_id == self.partner_id.property_product_pricelist
            )

    def _compute_is_deposit_sale_order(self):
        for record in self:
            record.is_deposit_sale_order = record.pricelist_id.is_deposit_pricelist()

    @api.onchange('order_line')
    def default_pricelist_when_order_line(self):
        if self.order_line:
            if self.pricelist_id.route_id:
                for line in self.order_line:
                    line.route_id = self.pricelist_id.route_id.id

    @api.onchange('pricelist_id')
    def default_pricelist_when_pricelist_id(self):
        if self.order_line:
            if self.pricelist_id.route_id:
                for line in self.order_line:
                    line.route_id = self.pricelist_id.route_id.id
                    line.price_unit = line._get_display_price(line.product_id)


class EditorialSaleOrderLine(models.Model):
    """ Extend sale.order.line template for editorial management """
    _description = "Editorial Sale Order Line"
    _inherit = 'sale.order.line' # odoo/addons/sale/models/sale.py

    product_barcode = fields.Char(
        string='Código de barras / ISBN',
        related='product_id.barcode', readonly=True
    )
    product_list_price = fields.Float(
        string='PVP',
        related='product_id.list_price',
        readonly=True
    )
    in_stock_qty = fields.Float(
        string='In stock', 
        compute='_compute_in_stock_qty'
    )
    in_distribution_qty = fields.Float(
        string='In distribution',
        compute='_compute_in_distribution_qty'
    )

    @api.depends('product_id')
    def _compute_in_stock_qty(self):
        for record in self:
            if record.product_id:
                record.in_stock_qty = record.product_id.on_hand_qty
            else:
                record.in_stock_qty = 0

    @api.depends('product_id')
    def _compute_in_distribution_qty(self):
        for record in self:
            if record.product_id:
                record.in_distribution_qty = record.product_id.in_distribution_qty
            else:
                record.in_distribution_qty = 0