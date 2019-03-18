# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class PaymentMode(models.Model):
    _name = "l10n_br.payment.mode"
    _description = 'Modo de Pagamento'
    _order = 'name'

    name = fields.Char(string='Name', required=True, translate=True)
    type = fields.Selection(
        [('receivable', 'Recebível'), ('payable', 'Pagável')],
        string="Tipo de Transação", default='receivable')
    company_id = fields.Many2one(
        'res.company', string='Company', ondelete='restrict')
    active = fields.Boolean(string='Active', default=True)
    journal_id = fields.Many2one(
        'account.journal', string="Journal",
        domain=[('type', 'in', ('cash', 'bank'))])
    # TODO Remove this fields latter on, from now on we use just journal_id
    bank_account_id = fields.Many2one(
        'res.partner.bank', string="Bank Account", ondelete='restrict')
    l10n_br_environment = fields.Selection(
        [('test', 'Teste'),
         ('production', 'Produção')],
        string='Ambiente',
        default='production'
    )
    is_default = fields.Boolean(string="Padrão em Faturas?")

    @api.multi
    @api.constrains("is_default")
    def _check_is_default(self):
        search_defaults = self.search([('is_default', '=', True)])
        if len(search_defaults) > 1:
            raise ValidationError(_("Only one payment mode can be default"))
