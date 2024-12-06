from odoo import api, fields, models, exceptions
from lxml import etree

class LiquidacionWizard(models.TransientModel):
    """ Wizard: Ayuda para seleccionar las stock.move.lines pendientes de liquidar """
    _name = 'liquidacion.wizard.descontrol'
    _description =  "Wizard Depósito"

    partner_id = fields.Many2one('res.partner', string='Cliente')
    liquidacion_id = fields.Many2one('account.move', string='Liquidación')
    liquidacion_type = fields.Selection(related='liquidacion_id.type')
    liquidacion_line_ids = fields.One2many('liquidacion.line.descontrol', 'liquidacion_wizard_id', string="Lineas de Liquidacion", copy=True)

    @api.onchange('partner_id')
    def _update_invoice_lines(self):
        for wizard in self:
            pendientes_liquidar_line_ids = wizard.liquidacion_id.get_deposito_lines(alphabetical_order=True)
            wizard.liquidacion_line_ids = None
            if self.partner_id.property_account_position_id:
                wizard.fiscal_position_id = self.partner_id.property_account_position_id

            for move_line in pendientes_liquidar_line_ids:
                wizard._update_liquidacion_line(move_line)

            if wizard.liquidacion_id.type == 'in_invoice' or wizard.liquidacion_id.type == 'in_refund':
                for liquidacion_line in wizard.liquidacion_line_ids:
                    products_sold = liquidacion_line.product_id.get_liquidated_sales_qty()
                    products_purchased_and_liquidated = liquidacion_line.product_id.get_liquidated_purchases_qty()
                    liquidacion_line.vendidos_sin_liquidar = max(0, products_sold - products_purchased_and_liquidated)
                    liquidacion_line.vendidos_sin_liquidar = min(liquidacion_line.vendidos_sin_liquidar, liquidacion_line.total_qty_disponibles)

    def _update_liquidacion_line(self, move_line):
        liquidacion_line_aux = self.liquidacion_line_ids.filtered(lambda line: line.product_id == move_line.product_id)
        if len(liquidacion_line_aux) <= 0:
            liquidacion_line = self.env['liquidacion.line.descontrol'].create({'liquidacion_wizard_id': self.id, 'product_id': move_line.product_id.id})
        else:
            liquidacion_line = liquidacion_line_aux[0]
        if self.liquidacion_id.type == 'out_invoice' or self.liquidacion_id.type == 'out_refund':
            total_product_uom_qty = liquidacion_line.total_product_uom_qty + move_line.product_uom_qty
            liquidacion_line.total_qty_done += move_line.qty_done
        elif self.liquidacion_id.type == 'in_invoice' or self.liquidacion_id.type == 'in_refund':
            total_product_uom_qty = liquidacion_line.total_product_uom_qty + move_line.qty_received
            liquidacion_line.total_qty_done += move_line.liquidated_qty
        liquidacion_line.update({'total_product_uom_qty': total_product_uom_qty})
        return liquidacion_line

    @api.onchange('liquidacion_line_ids')
    def _check_liquidacion_lines(self):
        for wizard in self:
            for liquidacion_line in wizard.liquidacion_line_ids:
                if liquidacion_line.total_qty_a_liquidar and liquidacion_line.total_qty_a_liquidar > 0.0:
                    if wizard.liquidacion_type in ['in_invoice', 'out_invoice', 'out_refund'] and liquidacion_line.total_qty_a_liquidar > liquidacion_line.total_qty_disponibles:
                        raise exceptions.ValidationError("La cantidad seleccionada no puede ser mayor que la cantidad disponible en depósito.")
                    elif wizard.liquidacion_type == 'in_refund' and liquidacion_line.total_qty_a_liquidar > liquidacion_line.total_qty_disponibles_devolver_dep_com:
                        raise exceptions.ValidationError("La cantidad a liquidar no puede ser mayor que la cantidad disponible para devolver.")
                    
    @api.model
    def default_get(self, fields):
        res = super(LiquidacionWizard, self).default_get(fields)
        res['partner_id'] = self.env.context.get('partner_id')
        res['liquidacion_id'] = self.env.context.get('liquidacion_id')
        return res

    def seleccionar_para_liquidar(self):
        for liquidacion_line in self.liquidacion_line_ids:
            if liquidacion_line.total_qty_a_liquidar > 0.0:
                if not self.liquidacion_id.pricelist_id:
                    #Utilizamos siempre el PVP independientemente de si es liquidacion de compra o venta
                    price_unit = liquidacion_line.product_id.list_price
                else:
                    price_unit = self.liquidacion_id.pricelist_id.get_product_price(
                        liquidacion_line.product_id, 1, self.partner_id
                    )
                quantity = liquidacion_line.total_qty_a_liquidar
                product = liquidacion_line.product_id
                partner = self.partner_id.id

                if self.liquidacion_type == 'in_invoice' or self.liquidacion_type == 'in_refund':
                    taxes = product.supplier_taxes_id
                else:
                    taxes = product.taxes_id

                taxes = self.liquidacion_id.fiscal_position_id.map_tax(
                    taxes, partner=self.partner_id
                )

                vals = {
                    'name': liquidacion_line.product_id.name,
                    'move_id': self.env.context.get('liquidacion_id'),
                    'partner_id': partner,
                    'product_id': product.id,
                    'journal_id': self.liquidacion_id.journal_id,
                    'quantity': quantity,
                    'price_unit': price_unit,
                    'tax_ids': taxes,
                }
                self.liquidacion_id.write({'invoice_line_ids': [(0,0,vals)]}) # = self.env['account.move.line'].new(vals)
        self.liquidacion_id._move_autocomplete_invoice_lines_values()
        self.liquidacion_id._recompute_payment_terms_lines()
        return {'type': 'ir.actions.act_window_close'}
    
    def select_all_liquidacion_lines(self):
        for liquidacion_line in self.liquidacion_line_ids:
            liquidacion_line.total_qty_a_liquidar = liquidacion_line.total_qty_disponibles
            if not self.liquidacion_id.pricelist_id:
                price_unit = liquidacion_line.product_id.list_price
            else:
                price_unit = self.liquidacion_id.pricelist_id.get_product_price(
                    liquidacion_line.product_id, 1, self.partner_id
                )
            quantity = liquidacion_line.total_qty_a_liquidar
            product = liquidacion_line.product_id
            partner = self.partner_id.id

            vals = {
                'name': liquidacion_line.product_id.name,
                'move_id': self.env.context.get('liquidacion_id'),
                'partner_id': partner,
                'product_id': product.id,
                'journal_id': self.liquidacion_id.journal_id,
                'quantity': quantity,
                'price_unit': price_unit,
                'tax_ids': product.taxes_id,
            }
            self.liquidacion_id.write({'invoice_line_ids': [(0,0,vals)]}) # = self.env['account.move.line'].new(vals)
        self.liquidacion_id._move_autocomplete_invoice_lines_values()
        self.liquidacion_id._recompute_payment_terms_lines()
        return {'type': 'ir.actions.act_window_close'}

class EditorialLiquidacionLine(models.TransientModel):
    """ Modelo de línea de liquidación"""
    _name = "liquidacion.line.descontrol"
    _description = "Linea Liquidacion Descontrol"

    # company_id = fields.Many2one(related='liquidacion_id.company_id', store=True, readonly=True)
    liquidacion_wizard_id = fields.Many2one('liquidacion.wizard.descontrol', "Liquidacion Wizard", index=True, ondelete="cascade")
    product_id = fields.Many2one('product.product', 'Producto')
    product_barcode = fields.Char('Código de barras / ISBN', related='product_id.barcode', store=True, readonly=True)
    product_name = fields.Char('Nombre', related='product_id.name', store=True, readonly=True)
    total_product_uom_qty = fields.Float('Total en Depósito', default=0.0, digits='Product Unit of Measure', required=True, copy=False)
    total_qty_done = fields.Float('Total Hecho', default=0.0, digits='Product Unit of Measure', copy=False)
    total_qty_disponibles = fields.Float('Total en depósito', default=0.0, digits='Product Unit of Measure', copy=False, compute="_compute_available")
    total_qty_disponibles_devolver_dep_com = fields.Float('Total disponible', default=0.0, digits='Product Unit of Measure', copy=False, compute="_compute_available_dep_com")
    total_qty_a_liquidar = fields.Float('A liquidar', default=0.0, digits='Product Unit of Measure', copy=False)
    vendidos_sin_liquidar = fields.Float('Vendidos sin liquidar', default=0.0, digits='Product Unit of Measure', copy=False, readonly=True)

    @api.depends('total_qty_done', 'total_product_uom_qty')
    def _compute_available(self):
        for record in self:
            record.total_qty_disponibles = record.total_product_uom_qty - record.total_qty_done

    @api.depends('total_qty_done', 'total_product_uom_qty')
    def _compute_available_dep_com(self):
        for record in self:
            record.product_id._compute_on_hand_qty()
            stock = record.product_id.on_hand_qty
            record.total_qty_disponibles_devolver_dep_com = min(record.total_qty_disponibles, stock)

    def fields_view_get(self, view_id=None, view_type='tree', toolbar=False, submenu=False):
        result = super(EditorialLiquidacionLine, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        if view_type == 'tree':
            doc = etree.XML(result['arch'])
            liquidacion_type = self._context.get('liquidacion_type')
            if liquidacion_type == 'out_refund' or liquidacion_type == 'in_refund':
                field_reference = doc.xpath("//field[@name='total_qty_a_liquidar']")
                field_reference[0].set("string", "A devolver")
                result['arch'] = etree.tostring(doc, encoding='unicode')
        return result
