
ORIGINAL_VALUE = 0
TOP_RESOLUTION = 1

SLOT_CONFIG = {
    'one_company':      {'type': TOP_RESOLUTION, 'remember': True, 'error': 'I couldn\'t find an company called "{}".'},
    'another_company':       {'type': TOP_RESOLUTION, 'remember': True,'error': 'I couldn\'t find an company called "{}".'},

    'particular_date':       {'type': ORIGINAL_VALUE, 'remember': True},
    'one_date':      {'type': ORIGINAL_VALUE, 'remember': True},
    'another_date':         {'type': ORIGINAL_VALUE, 'remember': True},
    'count':            {'type': ORIGINAL_VALUE, 'remember': True},
    'particular_company':        {'type': TOP_RESOLUTION, 'remember': True,'error': 'I couldn\'t find an company called "{}".'},
    'one_stock':    {'type': TOP_RESOLUTION, 'remember': True, 'error': 'I couldn\'t find a stock called "{}".'},
    'another_stock':        {'type': TOP_RESOLUTION, 'remember': True, 'error': 'I couldn\'t find a stock called "{}".'},
    'particular_stock':    {'type': TOP_RESOLUTION, 'remember': True, 'error': 'I couldn\'t find an stock called "{}".'},
    }

DIMENSIONS = {
    'stocks':     {'slot': 'company_name',  'column':'p.company_name',  'singular': 'stock'},
    'firms':     {'slot': 'firm_name', 'column': 'c.company_name', 'singular': 'firm'}
}


class SlotError(Exception):
    pass

