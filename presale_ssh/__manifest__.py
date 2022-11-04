{
'name':'Presale SSH',
'version': '15.0.1.0.0',
'author': 'Odoo PS',
'summary': 'Presale application',
'description':"""
        Presale order on a product
    """,
'category': 'Customization',
'depends': [
    'base',
    'sale_management',
    'mail',
    'contacts',
],
'data': [
    'data/ir_sequence_data.xml',
    'data/mail_template_data.xml',
    'data/presale_order_cron_data.xml',

    'security/groups.xml',
    'security/ir.model.access.csv',
    

    'views/presale_ssh_order_line_views.xml',
    'views/presale_ssh_order_views.xml',
    'views/sale_order_inherit_views.xml'
],
'installable': True,
'application': True,
'license': 'LGPL-3',
}
