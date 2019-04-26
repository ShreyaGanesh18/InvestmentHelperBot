import time
import logging
import json
import ihbot_config as ihbot
import ihbot_helpers as helpers
import ihbot_userexits as userexits

# SELECT statement for query
COUNT_SELECT = "SELECT quantity FROM my_portfolio "
COUNT_JOIN = "  "
COUNT_WHERE = " AND LOWER({}) LIKE LOWER('%{}%') "   
COUNT_PHRASE = 'Quantity bought'

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def lambda_handler(event, context):
    logger.debug('<<IHBot>> Lex event info = ' + json.dumps(event))

    config_error = helpers.get_ihbot_config()

    session_attributes = event['sessionAttributes']
    logger.debug('<<IHBot>> lambda_handler: session_attributes = ' + json.dumps(session_attributes))

    if config_error is not None:
        return helpers.close(session_attributes, 'Fulfilled',
            {'contentType': 'PlainText', 'content': config_error})   
    else:
        return count_intent_handler(event, session_attributes)


def count_intent_handler(intent_request, session_attributes):
    method_start = time.perf_counter()
    
    logger.debug('<<IHBot>> count_intent_handler: intent_request = ' + json.dumps(intent_request))
    logger.debug('<<IHBot>> count_intent_handler: session_attributes = ' + json.dumps(session_attributes))
    
    session_attributes['greetingCount'] = '1'
    session_attributes['resetCount'] = '0'
    session_attributes['finishedCount'] = '0'
    session_attributes['lastIntent'] = 'Count_Intent'

    # Retrieve slot values from the current request
    slot_values = session_attributes.get('slot_values')

    try:
        slot_values = helpers.get_slot_values(slot_values, intent_request)
    except ihbot.SlotError as err:
        return helpers.close(session_attributes, 'Fulfilled', {'contentType': 'PlainText','content': str(err)})   
    
    logger.debug('<<IHBot>> "count_intent_handler(): slot_values: %s', slot_values)

    # Retrieve "remembered" slot values from session attributes
    slot_values = helpers.get_remembered_slot_values(slot_values, session_attributes)
    logger.debug('<<IHBot>> "count_intent_handler(): slot_values afer get_remembered_slot_values: %s', slot_values)

    # Remember updated slot values
    helpers.remember_slot_values(slot_values, session_attributes)
    
    # build and execute query
    select_clause = COUNT_SELECT
    where_clause = COUNT_JOIN
    for dimension in ihbot.DIMENSIONS:
        slot_key = ihbot.DIMENSIONS.get(dimension).get('slot')
        if slot_values[slot_key] is not None:
            value = userexits.pre_process_query_value(slot_key, slot_values[slot_key])
            where_clause += COUNT_WHERE.format(ihbot.DIMENSIONS.get(dimension).get('column'), value)
    
    query_string = select_clause + where_clause
    
    response = helpers.execute_athena_query(query_string)

    result = response['ResultSet']['Rows'][1]['Data'][0]
    if result:
        count = result['VarCharValue']
    else:
        count = 0

    logger.debug('<<IHBot>> "Count value is: %s' % count) 

    # build response string
    if count == 0:
        response_string = 'There were no {}'.format(COUNT_PHRASE)
    else:
        response_string = 'There were {} {}'.format(count, COUNT_PHRASE)

    # add the English versions of the WHERE clauses
    for dimension in ihbot.DIMENSIONS:
        slot_key = ihbot.DIMENSIONS[dimension].get('slot')
        logger.debug('<<IHBot>> pre top5_qtformatter[%s] = %s', slot_key, slot_values.get(slot_key))
        if slot_values.get(slot_key) is not None:
            # the DIMENSION_FORMATTERS perform a post-process functions and then format the output
            # Example:  {... 'venue_state': {'format': ' in the state of {}',  'function': get_state_name}, ...}
            if userexits.DIMENSION_FORMATTERS.get(slot_key) is not None:
                output_text = userexits.DIMENSION_FORMATTERS[slot_key]['function'](slot_values.get(slot_key))
                response_string += ' ' + userexits.DIMENSION_FORMATTERS[slot_key]['format'].lower().format(output_text)
                logger.debug('<<IHBot>> dimension_qtformatter[%s] = %s', slot_key, output_text)

    response_string += '.'

    return helpers.close(session_attributes, 'Fulfilled', {'contentType': 'PlainText','content': response_string})   
