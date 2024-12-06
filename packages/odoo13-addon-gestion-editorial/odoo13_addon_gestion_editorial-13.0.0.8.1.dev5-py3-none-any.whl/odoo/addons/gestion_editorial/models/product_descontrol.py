from odoo import models, fields, api, exceptions

class EditorialProducts(models.Model):
    """ Extend product product for editorial management """

    _description = "Editorial Core Products"
    _inherit = 'product.product'

    on_hand_qty = fields.Float(compute='_compute_on_hand_qty', string='En almacén')
    liquidated_qty = fields.Float(compute='_compute_liquidated_sales_qty', string='Ventas liquidadas')
    liquidated_purchases_qty = fields.Float(compute='_compute_liquidated_purchases_qty', string='Compras liquidadas')
    owned_qty = fields.Float(compute='_compute_owned_qty', string='Existencias totales')
    in_distribution_qty = fields.Float(compute='_compute_in_distribution_qty', string='En distribución')
    purchase_deposit_qty = fields.Float(compute='_compute_purchase_deposit_qty', string='Depósito de compra')
    received_qty = fields.Float(compute='_compute_received_qty', string='Recibidos')

    def get_liquidated_sales_qty(self):
        return self.get_product_quantity_in_location(self.env.ref("stock.stock_location_customers").id)

    def get_all_child_locations(self, location_id):
        location = self.env['stock.location'].browse(location_id)
        child_locations = location.child_ids
        location_ids = [location.id] + [child.id for child in child_locations]
        
        for child_location in child_locations:
            location_ids += self.get_all_child_locations(child_location.id)

        return location_ids

    def get_product_quantity_in_location(self, location_id):
        location_ids = self.get_all_child_locations(location_id)

        quants = self.env['stock.quant'].search([
            ('product_id', '=', self.id), 
            ('location_id', 'in', location_ids)
        ])

        quantity = sum(quant.quantity for quant in quants)
        return quantity

    def get_received_qty(self):
        domain = [
            ('state', 'in', ['purchase', 'done']),
            ('product_id', '=', self.id)
        ]
        purchase_order_lines = self.env['purchase.order.line'].search(domain)
        return sum(purchase_order_lines.mapped('qty_received'))

    def get_liquidated_purchases_qty(self):
        domain = [
            ('state', 'in', ['purchase', 'done']),
            ('product_id', '=', self.id)
        ]
        purchase_order_lines = self.env['purchase.order.line'].search(domain)
        return sum(purchase_order_lines.mapped('liquidated_qty'))
    
    def get_liquidated_sales_qty_per_partner(self, partner_id):
        liquidated_sale_lines = self.env['stock.move.line'].search([
            ('owner_id', '=', partner_id),
            ('state', '=', 'done'),
            ('location_dest_id', '=', self.env.ref("stock.stock_location_customers").id),
            ('product_id', '=', self.id)
        ])
        liquidated_sales_qty = sum(line.qty_done for line in liquidated_sale_lines)

        returned_sale_lines = self.env['stock.move.line'].search([
            ('owner_id', '=', partner_id),
            ('state', '=', 'done'),
            ('location_id', '=', self.env.ref("stock.stock_location_customers").id),
            ('product_id', '=', self.id)
        ])
        returned_sales_qty = sum(line.qty_done for line in returned_sale_lines)
        return liquidated_sales_qty - returned_sales_qty
    @api.constrains('lst_price')
    def update_ddaa_orders_price(self):
        if self.env.company.product_category_ddaa_id == self.categ_id:
            # we use self.id.origin when function calling comes from product template
            product_id = self.id.origin if hasattr(self.id, 'origin') else self.id
            domain = [
                ('product_id', '=', product_id),
                ('state', '=', 'draft')
            ]
            ddaa_order_lines = self.env['purchase.order.line'].search(domain)
            for line in ddaa_order_lines:
                line.price_unit = self.lst_price

    def _compute_liquidated_purchases_qty(self):
        for product in self:
            product.liquidated_purchases_qty = product.get_liquidated_purchases_qty()

    def _compute_received_qty(self):
        for product in self:
            product.received_qty = product.get_received_qty()

    def _compute_purchase_deposit_qty(self):
        #Purchased on deposit but not settled
        for product in self:
            product.purchase_deposit_qty = product.received_qty - product.liquidated_purchases_qty

    def _compute_on_hand_qty(self):
        for product in self:
            product.on_hand_qty = product.get_product_quantity_in_location(self.env.ref("stock.stock_location_stock").id)

    def _compute_liquidated_sales_qty(self):
        for product in self:
            product.liquidated_qty = product.get_liquidated_sales_qty()

    def _compute_owned_qty(self):
        for product in self:
            product.owned_qty = product.on_hand_qty + product.in_distribution_qty

    def _compute_in_distribution_qty(self):
        for product in self:
            product.in_distribution_qty = product.get_product_quantity_in_location(self.env.company.location_venta_deposito_id.id)


class EditorialTemplateProducts(models.Model):
    """ Extend product template for editorial management """

    _description = "Editorial Template Products"
    _inherit = 'product.template'
    # we inherited product.template model which is Odoo/OpenERP built in model and edited several fields in that model.
    isbn_number = fields.Char(string="ISBN", copy=False, required=False,
                              help="International Standard Book Number \
                              (ISBN)")
    product_tags = fields.Many2many('product.template.tag', string='Product tag')
    purchase_ok = fields.Boolean('Can be Purchased', default=False)
    author_name = fields.Many2many("res.partner", string="Autores", required=False,
                                   help="Nombre del autor", domain="[('is_author','=',True)]")
    on_hand_qty = fields.Float(compute='_compute_on_hand_qty', string='En almacén')
    liquidated_qty = fields.Float(compute='_compute_liquidated_sales_qty', string='Ventas liquidadas')
    liquidated_purchases_qty = fields.Float(compute='_compute_liquidated_purchases_qty', string='Compras liquidadas')
    owned_qty = fields.Float(compute='_compute_owned_qty', string='Existencias totales')
    in_distribution_qty = fields.Float(compute='_compute_in_distribution_qty', string='En distribución')
    purchase_deposit_qty = fields.Float(compute='_compute_purchase_deposit_qty', string='Depósito de compra')
    received_qty = fields.Float(compute='_compute_received_qty', string='Recibidos')

    def _compute_on_hand_qty(self):
        for template in self:
            on_hand_qty = 0.0
            for product in template.product_variant_ids:
                on_hand_qty += product.get_product_quantity_in_location(self.env.ref("stock.stock_location_stock").id)
            template.on_hand_qty = on_hand_qty

    def _compute_liquidated_sales_qty(self):
        for template in self:
            liquidated_sales_qty = 0.0
            for product in template.product_variant_ids:
                liquidated_sales_qty += product.get_liquidated_sales_qty()
            template.liquidated_qty = liquidated_sales_qty

    def _compute_liquidated_purchases_qty(self):
        for template in self:
            liquidated_purchases_qty = 0.0
            for product in template.product_variant_ids:
                liquidated_purchases_qty += product.get_liquidated_purchases_qty()
            template.liquidated_purchases_qty = liquidated_purchases_qty

    def _compute_purchase_deposit_qty(self):
        for template in self:
            template.purchase_deposit_qty = template.received_qty - template.liquidated_purchases_qty

    def _compute_received_qty(self):
        for template in self:
            received_qty = 0.0
            for product in template.product_variant_ids:
                received_qty += product.get_received_qty()
            template.received_qty = received_qty

    def _compute_owned_qty(self):
        for template in self:
            template.owned_qty = template.on_hand_qty + template.in_distribution_qty

    def _compute_in_distribution_qty(self):
        for template in self:
            in_distribution_qty = 0.0
            for product in template.product_variant_ids:
                in_distribution_qty += product.get_product_quantity_in_location(self.env.company.location_venta_deposito_id.id)
            template.in_distribution_qty = in_distribution_qty

    @api.onchange('list_price')
    def update_ddaa_orders_price(self):
        if self.env.company.product_category_ddaa_id == self.categ_id:
            product_ids = self.product_variant_ids
            for product in product_ids:
                product.update_ddaa_orders_price()

    @api.constrains("isbn_number")
    def check_is_isbn13(self):
        for record in self:
            if record.isbn_number:
                n = record.isbn_number.replace("-", "").replace(" ", "")
                if len(n) != 13:
                    raise exceptions.ValidationError("El ISBN debe tener 13 dígitos")
                product = sum(int(ch) for ch in n[::2]) + sum(
                    int(ch) * 3 for ch in n[1::2]
                )
                if product % 10 != 0:
                    raise exceptions.ValidationError(
                        "El ISBN %s no es válido." % record.isbn_number
                    )
        # all records passed the test, don't return anything

    def generate_ddaa(self, ddaa_qty):
        if not self.env.company.module_editorial_ddaa or not self.genera_ddaa:
            return

        # check if the product already has ddaa
        ddaa = self.derecho_autoria
        if not ddaa:
            author = self.author_name
            if not author:
                return
            else:
                ddaa = self.env['product.template'].create({
                    'name': 'DDAA de ' + self.name,
                    'categ_id': self.env.company.product_category_ddaa_id.id,
                    'list_price': self.list_price * 0.1,
                    'type': 'service',
                    'sale_ok': False,
                    'purchase_ok': True,
                    'author_name': author,
                    'receptora_derecho_autoria': author,
                    'producto_referencia': [self.id],
                    'derecho_autoria': False,
                    "supplier_taxes_id": False
                })
        # If there are already ddaaa, use the field receptora_derecho_autoria
        if not ddaa.receptora_derecho_autoria:
            return
        domain = [
            ('partner_id', '=', ddaa.receptora_derecho_autoria.id),
            ('state', '=', 'draft'),
            ('partner_ref', '=', 'DDAA')
        ]
        compra_derechos_autoria = self.env['purchase.order'].search(domain, order='date_order desc')
        if not compra_derechos_autoria:
            # create sale.order to ddaa receiver
            compra_derechos_autoria = self.env['purchase.order'].create({
                'partner_id': ddaa.receptora_derecho_autoria.id,
                'partner_ref': 'DDAA',
                'picking_type_id': self.env.ref("stock.picking_type_in").id
            })
        elif len(compra_derechos_autoria) > 1:
            compra_derechos_autoria = compra_derechos_autoria[0]
        # search line and add or substract qty
        linea_libro_compra = compra_derechos_autoria.order_line.filtered(lambda line: line.product_id.product_tmpl_id.id == ddaa.id)
        if linea_libro_compra:
            if len(linea_libro_compra) > 1:
                linea_libro_compra = linea_libro_compra[0]
            linea_libro_compra.write({'product_qty': linea_libro_compra.product_qty + ddaa_qty})
        else:
            product_id = self.env['product.product'].search([('product_tmpl_id', '=', ddaa.id)])
            vals = {
                'name': ddaa.name,
                'order_id': compra_derechos_autoria.id,
                'product_id': product_id.id,
                'product_qty': ddaa_qty,
                'price_unit': ddaa.list_price,
                'product_uom': 1,
                'date_planned': compra_derechos_autoria.date_order,
                'display_type': False
            }
            compra_derechos_autoria.write({'order_line': [(0,0,vals)]})

    # DDAA: Derechos de autoría
    # When the category "All / Books" is selected (with id 5), the default values ​​are set:
    # Product that can be sold and bought is storable.
    @api.onchange("categ_id")
    def _onchange_uom(self):
        if self.categ_id:
            if self.categ_id.id == 5:  # category book
                self.sale_ok = True
                self.purchase_ok = True
                self.type = "product"
            elif self.categ_id.id == 11:  # category Digital Book
                self.sale_ok = True
                self.purchase_ok = True
                self.type = "consu"
            if (
                self.env.company.module_editorial_ddaa
                and self.env.company.is_category_genera_ddaa_or_child(self.categ_id)
            ):
                self.genera_ddaa = True
            else:
                self.genera_ddaa = False

    @api.onchange("categ_id")
    def _compute_view_show_fields(self):
        if self.env.company.module_editorial_ddaa:
            self.view_show_genera_ddaa_fields = (
                self.env.company.is_category_genera_ddaa_or_child(self.categ_id)
            )
            self.view_show_ddaa_fields = (
                self.categ_id == self.env.company.product_category_ddaa_id
            )
        else:
            self.view_show_genera_ddaa_fields = False
            self.view_show_ddaa_fields = False

    # DDAA: Copyright
    # Check one2one relation. Here between "producto_referencia" y "derecho_autoria"
    #
    # Note: we are creating the relationship between the templates.
    # Therefore, when we add the product to a stock.picking or a sale or purchase, we are actually adding the product  and not the template.
    # Please use product_tmpl_id to access the template of a product.
    producto_referencia = fields.One2many(
        "product.template",
        "derecho_autoria",
        string="Libro de referencia",
        help="Este campo se utiliza para relacionar el derecho de autoría con el libro",
    )

    # prod_ref = fields.Many2one("product.template", compute='compute_autoria', inverse='autoria_inverse', string="prod ref",
    #                             required=False)

    @api.model
    def _derecho_autoria_domain(self):
        return [("categ_id", "=", self.env.company.product_category_ddaa_id.id)]

    derecho_autoria = fields.Many2one(
        "product.template",
        domain=_derecho_autoria_domain,
        string="Producto ddaa",
        help="Este campo se utiliza para relacionar el derecho de autoría con el libro",
    )

    receptora_derecho_autoria = fields.Many2many(
        "res.partner",
        "receptora_autoria_product_template",
        "product_id",
        "partner_id",
        copy=False,
        string="Receptor derechos autoría",
        help="Nombre de la receptora de derechos de autoría",
    )

    genera_ddaa = fields.Boolean("Genera derechos de autoría", default=False)

    # @api.depends('producto_referencia')
    # def compute_autoria(self):
    #     if len(self.derecho_autorias) > 0:
    #         self.derecho_autoria = self.derecho_autorias[0]

    # def autoria_inverse(self):
    #     if len(self.derecho_autorias) > 0:
    #         # delete previous reference
    #         ddaa = self.env['product.template'].browse(self.derecho_autorias[0].id)
    #         ddaa.producto_referencia = False
    #     # set new reference
    #     self.derecho_autoria.producto_referencia = self

    view_show_genera_ddaa_fields = fields.Boolean(
        "Muestra los campos asociados a categorías que generan ddaa",
        compute="_compute_view_show_fields",
        default=False,
    )
    view_show_ddaa_fields = fields.Boolean(
        "Muestra los campos asociados a la categoría ddaa",
        compute="_compute_view_show_fields",
        default=False,
    )

    limited_visibility_by_provider = fields.Boolean(
        "Visibilidad limitada por proveedor", 
        help="El producto solo será visible en compras para los proveedores configurados",
        default=lambda self: self.env.company.visibility_limited_by_supplier
    )

    # DDAA: Copyright
    # A product associated with the category representing the DDAA is created
    @api.model_create_multi
    def create(self, vals_list):
        templates = super(EditorialTemplateProducts, self).create(vals_list)
        company = self.env.company
        if company.module_editorial_ddaa and vals_list:
            vals = vals_list[0]
            category_id = self.env["product.category"].browse(vals.get("categ_id"))
            if (
                company.is_category_genera_ddaa_or_child(category_id)
                and vals.get("genera_ddaa") == True
            ):
                self.env["product.template"].create(
                    {
                        "name": "DDAA de " + vals.get("name"),
                        "categ_id": company.product_category_ddaa_id.id,
                        "list_price": vals.get("list_price") * 0.1,
                        "type": "service",
                        "sale_ok": False,
                        "purchase_ok": True,
                        "author_name": vals.get("author_name"),
                        "receptora_derecho_autoria": vals.get("author_name"),
                        "producto_referencia": [templates.id],
                        "derecho_autoria": False,
                        "supplier_taxes_id": False
                    }
                )
        return templates
    

class EditorialProductTags(models.Model):
    """ Editorial product tags management """

    _description = 'Editorial product tags'
    _name = 'product.template.tag'
    _rec_name = 'name'

    name = fields.Char(string='Product tag', required=True)
