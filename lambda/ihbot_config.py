
ORIGINAL_VALUE = 0
TOP_RESOLUTION = 1

SLOT_CONFIG = {
    'one_company':      {'type': TOP_RESOLUTION, 'remember': False, 'error': 'I couldn\'t find an company called "{}".'},
    'another_company':       {'type': TOP_RESOLUTION, 'remember': False,'error': 'I couldn\'t find an company called "{}".'},

    'particular_date':       {'type': ORIGINAL_VALUE, 'remember': True},
    'one_date':      {'type': ORIGINAL_VALUE, 'remember': False},
    'another_date':         {'type': ORIGINAL_VALUE, 'remember': False},
    'count':            {'type': ORIGINAL_VALUE, 'remember': False},
    'particular_company':        {'type': TOP_RESOLUTION, 'remember': True,'error': 'I couldn\'t find an company called "{}".'},
    'one_stock':    {'type': TOP_RESOLUTION, 'remember': False, 'error': 'I couldn\'t find a stock called "{}".'},
    'another_stock':        {'type': TOP_RESOLUTION, 'remember': False, 'error': 'I couldn\'t find a stock called "{}".'},
    'particular_stock':    {'type': TOP_RESOLUTION, 'remember': True, 'error': 'I couldn\'t find an stock called "{}".'},
    }

DIMENSIONS = {
    'companies':     {'slot': 'company_name',  'column':'c.company_name',  'singular': 'company'},
    'stocks':     {'slot': 'company_name', 'column': 'p.company_name', 'singular': 'stock'}
}


class SlotError(Exception):
    pass

