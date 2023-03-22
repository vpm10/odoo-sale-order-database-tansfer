import xmlrpc.client
from odoo import models, fields

"""this model transfer sale order from one database to another targeted 
database"""


class FetchSo(models.Model):
    _name = 'fetch.so'
    _description = 'Fetch Data'
    _rec_name = 'from_database'

    from_database = fields.Char(string='Database 1',
                                help='Give the name of Database from where'
                                     ' you the data need to be fetch')
    to_database = fields.Char(string='Database 2',
                              help='Give the name of Database where the data '
                                   'need to be transferred')
    url_from = fields.Char(string='URL 1')
    url_to = fields.Char(string='URL 2')
    user_name_1 = fields.Char(string='User Name 1')
    user_name_2 = fields.Char(string='User Name 2')
    password_db_1 = fields.Char(string='Password 1')
    password_db_2 = fields.Char(string='Password 2')

    def action_fetch_sale_order(self):
        """this function fetches data from a database and transfer the data to
                the targeted database"""
        url_db1 = self.url_from
        db_1 = self.from_database
        username_db_1 = self.user_name_1
        password_db_1 = self.password_db_1
        common_1 = xmlrpc.client.ServerProxy(
            '{}/xmlrpc/2/common'.format(url_db1))
        models_1 = xmlrpc.client.ServerProxy(
            '{}/xmlrpc/2/object'.format(url_db1))
        common_1.version()

        url_db2 = self.url_to
        db_2 = self.to_database
        username_db_2 = self.user_name_2
        password_db_2 = self.password_db_2
        common_2 = xmlrpc.client.ServerProxy(
            '{}/xmlrpc/2/common'.format(url_db2))
        models_2 = xmlrpc.client.ServerProxy(
            '{}/xmlrpc/2/object'.format(url_db2))
        common_2.version()

        uid_db1 = common_1.authenticate(db_1, username_db_1, password_db_1, {})
        uid_db2 = common_2.authenticate(db_2, username_db_2, password_db_2, {})

        """To fetch required fields from the database"""
        db_15_so = models_1.execute_kw(db_1, uid_db1, password_db_1,
                                       'sale.order', 'search_read', [[]], {
                                           'fields': ['partner_id', 'state',
                                                      'order_line']
                                       })

        db_16_so = models_2.execute_kw(db_2, uid_db2, password_db_2,
                                       'sale.order', 'search_read', [[]], {
                                           'fields': ['partner_id', 'state',
                                                      'order_line'],
                                       })

        res_lst_16 = []
        for order in db_16_so:
            partner_id_16 = (order['partner_id'][0])
            order_line_16 = (order['order_line'])
            state_16 = (order['state'])
            data_16 = [partner_id_16, order_line_16, state_16]
            res_lst_16.append(data_16)

        res_lst_15 = []
        for sale in db_15_so:
            state_15 = (sale['state'])
            partner_id_15 = (sale['partner_id'][0])
            order_line_15 = (sale['order_line'])
            data_15 = [partner_id_15, order_line_15, state_15]
            if data_15 not in res_lst_16:
                res_lst_15.append(sale)

        """fetching required data from sale order line"""
        if res_lst_15:
            db_15_ol = models_1.execute_kw(db_1, uid_db1, password_db_1,
                                           'sale.order.line', 'search_read',
                                           [[]], {
                                               'fields': [
                                                   'name',
                                                   'customer_lead',
                                                   'product_template_id',
                                                   'product_uom_qty',
                                                   'price_unit',
                                                   'order_id',
                                                   'product_id']
                                           })

            """creating the sale order in the new database"""
            res_dct = {}
            for res in res_lst_15:
                for key in res:
                    if key == 'order_line':
                        continue
                    elif key == 'partner_id':
                        customer = res[key][0]
                        res_dct.update({key: customer})
                    else:
                        res_dct.update({key: res[key]})
            models_2.execute_kw(db_2, uid_db2, password_db_2,
                                'sale.order', 'create', [res_dct])

            """creating sale order line in created sale order"""
            for so in res_lst_15:
                for sol in db_15_ol:
                    if sol['order_id'][0] == so['id']:
                        models_2.execute_kw(db_2, uid_db2, password_db_2,
                                            'sale.order.line', 'create',
                                            [{'order_id': so['id'],
                                             'product_id':
                                              sol['product_id'][0],
                                              'product_uom_qty':
                                                  sol['product_uom_qty']
                                              }]
                                            )

        db_16_so_new = models_2.execute_kw(db_2, uid_db2, password_db_2,
                                           'sale.order', 'search_read', [[]], {
                                               'fields':
                                                   ['partner_id', 'state',
                                                    'order_line']})

        if db_16_so != db_16_so_new:
            return {
                'effect': {
                    'fadeout': 'medium',
                    'message': 'Transfer Completed',
                    'type': 'rainbow_man'}
            }
        else:
            return {
                'effect': {
                    'fadeout': 'medium',
                    'message': 'Nothing to transfer',
                    'type': 'rainbow_man'}
            }
