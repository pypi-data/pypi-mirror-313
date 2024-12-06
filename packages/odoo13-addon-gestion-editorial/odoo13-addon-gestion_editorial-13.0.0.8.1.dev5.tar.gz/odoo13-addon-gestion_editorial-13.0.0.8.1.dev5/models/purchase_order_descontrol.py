from odoo import models, fields, api, exceptions


class EditorialPurchaseOrder(models.Model):
    """ Extend purchase.order template for editorial management """
    _description = "Editorial Purchase Order"
    _inherit = 'purchase.order' # odoo/addons/purchase/models/purchase.py
    
    available_products = fields.Many2many('product.product', string='Productos disponibles', compute='_compute_available_products')

    # Calculates the products that can be added to the purchase order according to the provider.
    @api.onchange('partner_id')
    def _compute_available_products(self):
        self.available_products = self.env['product.product'].search([
            '|',
            ('seller_ids.name.id', '=', self.partner_id.id),
            ('limited_visibility_by_provider', '=', False)
        ])
    
    @api.onchange('partner_id')
    def _set_default_purchase_type(self):
        if self.partner_id.default_purchase_type.id:
            self.picking_type_id = self.partner_id.default_purchase_type
        else:
            self.picking_type_id = self._default_picking_type()

    # Prevents products with type "Service" from being purchased by "Compra en depósito" 
    def button_confirm(self):
        if self.picking_type_id.id == self.env.company.stock_picking_type_compra_deposito_id.id:
            service_products = []
            for line in self.order_line:
                product = line.product_id
                if product.type == 'service':
                    service_products.append(product.name)

            if len(service_products) > 0:
                msg = "Los productos con tipo 'Servicio' no pueden ser vendidos mediante compra en depósito. Por favor, selecciona compra en firme o elimina de tu pedido los siguientes productos:"
                for product in service_products:
                    msg += "\n* " + str(product)
                raise exceptions.UserError(msg)

        return super().button_confirm()


class EditorialPurchaseOrderLine(models.Model):
    """ Extend purchase.order.line template for editorial management """

    _description = "Editorial Purchase Order Line"
    _inherit = 'purchase.order.line' # odoo/addons/purchase/models/purchase.py

    product_barcode = fields.Char(string='Código de barras / ISBN', related='product_id.barcode', readonly=True)
    liquidated_qty = fields.Float(string='Liquidated', default=0.0)
    is_liquidated = fields.Boolean(string='Esta liquidado', default=False)

    @api.constrains('qty_received')
    def _onchange_qty_received(self):
        for record in self:
            if record.order_id.picking_type_id.id == self.env.company.stock_picking_type_compra_deposito_id.id:
                record.update({'is_liquidated': record.liquidated_qty >= record.qty_received})

            #liquidated_qty siempre sera igual a qty_received si es una compra en firme
            else:
                if record.qty_received != record.liquidated_qty:
                    record.write({'liquidated_qty': record.qty_received})
                record.write({'is_liquidated': True})

    @api.constrains('liquidated_qty')
    def _update_liquidated_qty(self):
        for record in self:
            record.write({'is_liquidated': record.liquidated_qty >= record.qty_received})
