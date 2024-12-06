from odoo import _, fields, models, api
from odoo.exceptions import ValidationError
from sinli.subject import Subject
from sinli.common.encoded_values import OrderType
from sinli.doctype import DocumentType
from sinli import Document
import re, base64
from datetime import datetime, time

class SinliDialog(models.TransientModel):
    _name = 'sinli.dialog'
    _description = 'SINLI Dialog'

    message = fields.Text(string='Message', readonly=True, required=True)


class SinliMessage(models.Model):
    _name = 'sinli.message'
    _description = 'SINLI message'
    _rec_name = 'type'

    _inherit = 'mail.thread'

    sender_email = fields.Char('Sender email')
    sender = fields.Many2one(
        'res.partner', 'Sender', ondelete='set null',
        domain=[('speak_sinli', '=', True)],
        help="Sender contact, if not exists it's empty.")

    date = fields.Datetime(
        'Date', default=fields.Datetime.now(),
        help="Date of the message.")
    
    import_date = fields.Datetime('Import date', required=False)
    import_user = fields.Many2one(
        'res.partner', 'Import user', ondelete='set null',
        help="User that imported the message.")

    type = fields.Char('Type of message', required=True)

    imported = fields.Boolean('Imported', default=False, 
                              help="True if the message was imported.")
    
    valid_format = fields.Boolean('Valid format', default=False, 
                              help="True if the message has a valid format.")

    message_main_attachment_id = fields.Many2one('ir.attachment', 'Attachment of the message', copy=False)

    generated_document = fields.Reference(string="Generated Document", selection=[
            ('sale.order', 'Orden de Venta'),
            ('purchase.order', 'Orden de Compra'),
            ('stock.return.picking', 'Devolución')
        ],
        help="References to the document generated after import.")

    # Overrides mail_thread message_new that is called by the mailgateway
    @api.model
    def message_new(self, msg_dict, custom_values=None):
        print("*************************** ENTRA NUEVO MENSAJE")
        if custom_values is None:
            custom_values = {}

        email_from = msg_dict.get('from')
        mail_subject = msg_dict.get('subject')
        valid_format = False

        readable_subject = Subject.from_str(mail_subject)
        if readable_subject.is_valid():
            msg_dict["subject"] = mail_subject
            valid_format = True


        # Get the email from address    
        email_pattern = r'[\w.+-]+@[\w.-]+'
        email_from = re.search(email_pattern, email_from).group(0)

        values = {
            'type': mail_subject,
            'sender_email': email_from,
            'valid_format': valid_format,
            'date': fields.Datetime.now(),
        }

        # Get the partner from the mail if any, else partner will be empty
        partner = self.env['res.partner'].search([('sinli_email', 'ilike', email_from)], limit=1)
        if partner:
            values['sender'] = partner.id

        custom_values.update(values)
        return super(SinliMessage, self).message_new(msg_dict, custom_values=custom_values)

    def import_sinli_message(self):
        if not self.sender: raise ValidationError("It is not possible to import an order without a contact.")

        decoded_bytes = base64.b64decode(self.message_main_attachment_id.datas)
        decoded_text = decoded_bytes.decode('windows-1252')

        sinli_message = Document.from_str(decoded_text)
        dialog_message = ""

        # Check sinli ID match for sender(client) and receiver(company)
        if (sinli_message.long_id_line.FROM and sinli_message.long_id_line.TO):
            if (sinli_message.long_id_line.FROM != self.sender.sinli_id):
                dialog_message = _("Sender's SINLI ID (%s) does not match the SINLI ID for %s.") % (sinli_message.long_id_line.FROM, self.sender.sinli_email)
            elif (sinli_message.long_id_line.TO != self.env.company.partner_id.sinli_id):
                dialog_message = _("Receiver SINLI ID (%s) does not match the company's SINLI ID.") % sinli_message.long_id_line.TO
        else:
            dialog_message = _("The message does not have SINLI ID for receiver/sender.")

        if not dialog_message:
            # Process import of SINLI SaleOrders
            if sinli_message.doctype_code == DocumentType.PEDIDO.name:
                dialog_message = self.import_sale_order(sinli_message)

            # Process import of SINLI import products
            elif (sinli_message.doctype_code == DocumentType.LIBROS.name):
                dialog_message = self.import_products(sinli_message)

            else:
                dialog_message = _("No valid message type detected for import.")

            # Process other SINLI messages
            # TO DO

        sinli_dialog = self.env['sinli.dialog'].create({
            'message': dialog_message,
        })

        # Return dialog containing the information about the import proccess status
        return {
            'name': 'SINLI Import',
            'type': 'ir.actions.act_window',
            'res_model': 'sinli.dialog',
            'view_id': self.env.ref('sinli.sinli_dialog_view_form').id,
            'view_mode': 'form',
            'target': 'new',
            'res_id': sinli_dialog.id,
        }

    def import_sale_order(self, sinli_message):
        order_lines = [] 
        not_imported_products = []

        for line in sinli_message.doc_lines:
            if (line.TYPE == "D"): # Sale Order line
                formated_isbn = re.sub(r"[-\s]", "", line.ISBN)

                # Search for books with equal ISBN (formatting the ISBN with only numbers)
                self.env.cr.execute("""
                    SELECT id FROM product_template
                    WHERE REGEXP_REPLACE(isbn_number, '[-\s]', '', 'g') = %s
                    LIMIT 1
                """, (formated_isbn,))
                
                product_id = self.env.cr.fetchone()
                if product_id:
                    # If the product is found we add it to the sale order, else we throw a error with the name of the product
                    product = self.env['product.template'].browse(product_id[0])
                    if product:
                        order_lines.append((0, 0, {
                            'product_id': product.product_variant_ids[0].id,
                            'product_uom_qty': line.QUANTITY,
                            'price_unit': line.PRICE,
                        }))
                else:
                    not_imported_products.append(line.TITLE)

            elif (line.TYPE == "C"):  # Sale Order header
                if line.ORDER_DATE:
                    date = fields.Date.from_string(line.ORDER_DATE)
                    date_and_time = datetime.combine(date, time())
                    date_order = fields.Datetime.to_string(date_and_time)   
                else:
                    date_order = fields.Datetime.now()

                # Set pricelist
                if (
                    (self.sender.property_product_pricelist.is_deposit_pricelist() 
                    == (line.ORDER_TYPE == OrderType.DEPOSIT)) 
                    or not line.ORDER_TYPE
                ):
                    pricelist_id = self.sender.property_product_pricelist.id
                else:
                    if line.ORDER_TYPE == OrderType.FIRM:
                        pricelist_id = self.env.company.default_pricelist_firm_sale.id
                    elif line.ORDER_TYPE == OrderType.DEPOSIT:
                        pricelist_id = self.env.company.default_pricelist_deposit_sale.id
                    elif line.ORDER_TYPE == OrderType.FAIRE:
                        pricelist_id = self.env.company.default_pricelist_fair_sale.id
                    elif line.ORDER_TYPE == OrderType.OTHER:
                        pricelist_id = self.env.company.default_pricelist_other_sale.id

                # Check if pricelist is set
                if not pricelist_id:
                    dialog_message = _("Please config the default pricelist for each type of sale order in the company settings.")
                    return dialog_message

        # Create draft sale order
        sale_order = self.env['sale.order'].create({
            'partner_id': self.sender.id,
            'date_order': date_order,
            'order_line': order_lines,
            'pricelist_id': pricelist_id
        })

        if sale_order:
            self.generated_document = sale_order
            self.imported = True
            self.import_date = fields.Datetime.now()
            self.import_user = self.env.user.id

            # Add reference to sale order notes
            sinli_reference_message = _(
                "Order created from SINLI message: <a href=# data-oe-model='{model}' data-oe-id='{id}'>{id}</a>"
            ).format(
                model=self._name,
                id=self.id,
            )
            sale_order.message_post(body=sinli_reference_message)

            if not not_imported_products:
                dialog_message = _("Order imported successfully: %s") % sale_order.name
            else:
                dialog_message = _("Order imported successfully: %s. But the following products were not imported: \n %s") % (
                    sale_order.name, "\n".join(not_imported_products)
                )
        else:
            dialog_message = _("There was an error importing the order")
        return dialog_message

    def import_products(self, sinli_message):
        imported_books = []
        not_imported_books = []

        for book_line in sinli_message.lines_by_type["Book"]:
            # Search for products with equal ISBN (formatting the ISBN with only numbers)
            self.env.cr.execute("""
                SELECT id FROM product_template
                WHERE REGEXP_REPLACE(isbn_number, '[-\s]', '', 'g') = %s
                LIMIT 1
            """, (re.sub(r"[-\s]", "", book_line.ISBN_INVOICE),))
            
            product_id = self.env.cr.fetchone()
            # If product is found we do not create a new one
            if product_id:
                not_imported_books.append(book_line.TITLE_FULL)
                continue

            # If product does not exist we create a new one
            isbn = re.sub(r"[-\s]", "", book_line.ISBN_INVOICE)
            new_book = self.env['product.template'].create({
                'name': book_line.TITLE_FULL,
                'type': "product",
                'categ_id': 5,
                'list_price': book_line.PRICE_PV,
                'isbn_number': isbn,
                'barcode': isbn,
                'purchase_ok': True,
                'sale_ok': True,
                # TO DO: Author?     
            })

            # Create provider info
            self.env['product.supplierinfo'].create({
                'product_tmpl_id': new_book.id,
                'name': self.sender.id,
                'price': book_line.PRICE_PVP,
                'min_qty': 0
            })

            # Search for authors, if not found we create a new one
            if book_line.AUTHORS:
                for author_name in book_line.AUTHORS.split(","):
                    author_contact = self.env['res.partner'].search([
                        ('name', '=ilike', author_name),
                        ('is_author', '=', True)
                    ], limit=1)
                    if not author_contact:
                        author_contact = self.env['res.partner'].create({
                            'name': author_name,
                            'is_author': True
                        })
                    new_book.author_name += author_contact

            imported_books.append(new_book.name)

        dialog_message = _("Import complete. Books successfully imported: \n %s \nBooks that already exist and were not imported: \n %s") % (
            "\n".join(imported_books), "\n".join(not_imported_books)
        )
        self.imported = True
        return dialog_message
    
