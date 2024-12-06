from odoo import models, fields, api, _
from odoo.exceptions import UserError

class EditorialPicking(models.Model):
    """ Extend stock.picking template for editorial management """

    _description = "Editorial Stock Picking"
    _inherit = 'stock.picking'  # odoo/addons/stock/models/stock_picking.py

    @api.depends(
            'state',
            'move_lines',
            'move_lines.state',
            'move_lines.package_level_id',
            'move_lines.move_line_ids.package_level_id'
        )
    def _compute_move_without_package(self):
        for picking in self:
            for move in self.move_lines:
                for ml in move.move_line_ids:
                    # If owner_id is equal we don't need to change anything so we don't call write method
                    if ml.owner_id != self.partner_id:
                        ml.owner_id = self.partner_id
            picking.move_ids_without_package = picking._get_move_ids_without_package()

    # DDAA: Derechos de autoría
    # Cuando se valida un stock.picking, se comprueba que la Localización de
    # destino es Partner Locations (con id 5), para hacer la compra de
    # derechos de autoría. También se ha de comprobar cuando se hace un
    # movimiento con origen Partner Locations (que representa una devolución).
    def generate_picking_ddaa(self):
        if self.env.company.module_editorial_ddaa and \
            self.env.ref("stock.stock_location_customers").id in \
                (self.location_dest_id.id, self.location_id.id):
            # Para las líneas que contengan un libro que tenga derechos de
            # autoría. Busca una purchase order a ese autor con la línea con
            # el derecho de autoría, si no, créala
            book_lines = self.move_line_ids_without_package.filtered(
                lambda line: self.env.company.is_category_genera_ddaa_or_child(
                    line.product_id.categ_id
                )
            )
            if book_lines:
                for book_line in book_lines:
                    if self.location_dest_id.id == self.env.ref("stock.stock_location_customers").id:
                        ddaa_qty = book_line.qty_done
                    else:
                        ddaa_qty = 0 - book_line.qty_done  # For refunds the qty_done is negative

                    book_line.product_id.product_tmpl_id.generate_ddaa(ddaa_qty)

    def button_validate(self):
        self.generate_picking_ddaa()
        return super(EditorialPicking, self).button_validate()


class EditorialStockMoveLine(models.Model):
    """ Extend stock.move.line for editorial management """

    _description = "Editorial Stock Move Line"
    # https://github.com/OCA/OCB/blob/13.0/addons/stock/models/stock_move_line.py
    _inherit = 'stock.move.line'

    product_barcode = fields.Char(
        string='Código de barras / ISBN',
        related='product_id.barcode', readonly=True
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('location_id') == 8:
                vals['qty_done'] = vals.get('product_uom_qty')
        return super(EditorialStockMoveLine, self).create(vals_list)


class EditorialStockMove(models.Model):
    """ Extend stock.move template for editorial management """

    _description = "Editorial Stock Move"
    _inherit = 'stock.move'  # odoo/addons/stock/wizard/stock_move.py

    product_barcode = fields.Char(
        string='Código de barras / ISBN',
        related='product_id.barcode',
        readonly=True
    )


class EditorialStockImmediateTransfer(models.TransientModel):

    """ Extend stock.immediate.transfer for editorial management """

    _description = "Editorial Stock Immediate Transfer"
    # odoo/addons/stock/models/stock_immediate_transfer.py
    _inherit = 'stock.immediate.transfer'

    def process(self):
        pick_to_backorder = self.env['stock.picking']
        pick_to_do = self.env['stock.picking']
        for picking in self.pick_ids:
            # If still in draft => confirm and assign
            if picking.state == 'draft':
                picking.action_confirm()
                if picking.state != 'assigned':
                    picking.action_assign()
                    if picking.state != 'assigned':
                        raise UserError(_("Could not reserve all requested products. Please use the \'Mark as Todo\' button to handle the reservation manually."))

            for move in picking.move_lines.filtered(lambda m: m.state not in ['done', 'cancel']):
                for move_line in move.move_line_ids:
                    move_line.qty_done = move_line.product_uom_qty
            if picking._check_backorder():
                pick_to_backorder |= picking
                continue
            pick_to_do |= picking

        # Process every picking that do not require a backorder,
        # then return a single backorder wizard for every other ones.
        if pick_to_do:
            pick_to_do.generate_picking_ddaa()
            pick_to_do.action_done()
        if pick_to_backorder:
            return pick_to_backorder.action_generate_backorder_wizard()
        return False
