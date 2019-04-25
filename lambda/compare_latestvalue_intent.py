
import time
import logging
import json
import ihbot_config as ihbot
import ihbot_helpers as helpers
import ihbot_userexits as userexits

COMPARE_CONFIG = {
    'stocks':     {'1st': 'one_stock',    '2nd': 'another_stock',    'error': 'Sorry, try "Compare stock 1 versus stock2 2'},
    }

# SELECT statement for Compare query
COMPARE_SELECT = "SELECT {}, (p.latest_value) lv FROM my_portfolio p"
COMPARE_WHERE = " AND LOWER({}) LIKE LOWER('%{}%') "  
COMPARE_ORDERBY = " ORDER BY lv DESC "

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def lambda_handler(event, context):
    logger.debug('<<IHBot>> Lex event info = ' + json.dumps(event))

    session_attributes = event['sessionAttributes']
    logger.debug('<<IHBot>> lambda_handler: session_attributes = ' + json.dumps(session_attributes))

    config_error = helpers.get_ihbot_config()
    if config_error is not None:
        return helpers.close(session_attributes, 'Fulfilled',
            {'contentType': 'PlainText', 'content': config_error})   
    else:
        return compare_intent_handler(event, session_attributes)


def compare_intent_handler(intent_request, session_attributes):
    method_start = time.perf_counter()
    
    logger.debug('<<IHBot>> compare_intent_handler: session_attributes = ' + json.dumps(session_attributes))

    session_attributes['greetingCount'] = '1'
    session_attributes['resetCount'] = '0'
    session_attributes['finishedCount'] = '0'
    session_attributes['lastIntent'] = None    # "switch" handling done in Compare_Intent

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
    
    for key,config in COMPARE_CONFIG.items():
        if slot_values.get(config['1st']):
            if slot_values.get(config['2nd']) is None:
                return helpers.close(session_attributes, 'Fulfilled', {'contentType': 'PlainText', 'content': config['error'] })
            
            slot_values['dimension'] = key
            slot_values[ihbot.DIMENSIONS[key]['slot']] = None
            
            the_1st_dimension_value = slot_values[config['1st']].lower()
            the_2nd_dimension_value = slot_values[config['2nd']].lower()

            break

    # Build and execute query
    select_clause = COMPARE_SELECT.format(ihbot.DIMENSIONS[slot_values['dimension']]['column'])
    where_clause = ""

    the_1st_dimension_value = userexits.pre_process_query_value(ihbot.DIMENSIONS[key]['slot'], the_1st_dimension_value)
    the_2nd_dimension_value = userexits.pre_process_query_value(ihbot.DIMENSIONS[key]['slot'], the_2nd_dimension_value)
    where_clause += "   AND (LOWER(" + ihbot.DIMENSIONS[slot_values['dimension']]['column'] + ") LIKE LOWER('%" + the_1st_dimension_value + "%') OR "
    where_clause +=         "LOWER(" + ihbot.DIMENSIONS[slot_values['dimension']]['column'] + ") LIKE LOWER('%" + the_2nd_dimension_value + "%')) " 

    logger.debug('<<IHBot>> compare_sales_intent_request - building WHERE clause') 
    for dimension in ihbot.DIMENSIONS:
        slot_key = ihbot.DIMENSIONS.get(dimension).get('slot')
        if slot_values[slot_key] is not None:
            logger.debug('<<IHBot>> compare_sales_intent_request - calling userexits.pre_process_query_value(%s, %s)', 
                         slot_key, slot_values[slot_key])  
            value = userexits.pre_process_query_value(slot_key, slot_values[slot_key])
            where_clause += COMPARE_WHERE.format(ihbot.DIMENSIONS.get(dimension).get('column'), value)

    order_by_group_by = COMPARE_ORDERBY.format(ihbot.DIMENSIONS[slot_values['dimension']]['column'])

    query_string = select_clause + where_clause + order_by_group_by
    
    logger.debug('<<IHBot>> Athena Query String = ' + query_string)  
    
    response = helpers.execute_athena_query(query_string)

    # Build response string
    response_string = ''
    result_count = len(response['ResultSet']['Rows']) - 1

    # add the English versions of the WHERE clauses
    counter = 0
    for dimension in ihbot.DIMENSIONS:
        slot_key = ihbot.DIMENSIONS[dimension].get('slot')
        logger.debug('<<IHBot>> pre compare_sale_formatter[%s] = %s', slot_key, slot_values.get(slot_key))
        if slot_values.get(slot_key) is not None:
            # the DIMENSION_FORMATTERS perform a post-process function and then format the output
            # Example:  {... 'venue_state': {'format': ' in the state of {}',  'function': get_state_name}, ...}
            if userexits.DIMENSION_FORMATTERS.get(slot_key) is not None:
                output_text = userexits.DIMENSION_FORMATTERS[slot_key]['function'](slot_values.get(slot_key))
                if counter == 0:
                    response_string += userexits.DIMENSION_FORMATTERS[slot_key]['format'].format(output_text)
                else:
                    response_string += ', ' + userexits.DIMENSION_FORMATTERS[slot_key]['format'].lower().format(output_text)
                counter += 1
                logger.debug('<<IHBot>> compare_sales_formatter[%s] = %s', slot_key, output_text)

    if (result_count == 0):
        if len(response_string) > 0:
            response_string += ', '
        response_string += "I didn't find any results for the " + slot_values['dimension']
        response_string += " " + userexits.post_process_dimension_output(key, the_1st_dimension_value)
        response_string += " and " + userexits.post_process_dimension_output(key, the_2nd_dimension_value) + "."

    elif (result_count == 1):
        if len(response_string) > 0:
            response_string += ', there '
        else:
            response_string += 'There '
        response_string += 'is only one ' + ihbot.DIMENSIONS[slot_values['dimension']]['singular'] + '.'
        
    elif (result_count == 2):
        # put the results into a dict for easier reference by name
        result_set = {}
        result_set.update( { response['ResultSet']['Rows'][1]['Data'][0]['VarCharValue'].lower() : [
                             response['ResultSet']['Rows'][1]['Data'][0]['VarCharValue'],  
                             float(response['ResultSet']['Rows'][1]['Data'][1]['VarCharValue']) ] } )
        result_set.update( { response['ResultSet']['Rows'][2]['Data'][0]['VarCharValue'].lower() : [
                             response['ResultSet']['Rows'][2]['Data'][0]['VarCharValue'],  
                             float(response['ResultSet']['Rows'][2]['Data'][1]['VarCharValue']) ] } )

        logger.debug('<<IHBot>> compare_intent_handler - result_set = %s', result_set) 

        the_1st_dimension_string = result_set[the_1st_dimension_value.lower()][0]
        the_1st_dimension_string = userexits.post_process_dimension_output(key, the_1st_dimension_string)
        the_2nd_dimension_string = result_set[the_2nd_dimension_value.lower()][0]
        the_2nd_dimension_string = userexits.post_process_dimension_output(key, the_2nd_dimension_string)

        if len(response_string) == 0:
            response_string = 'latest_value for ' + the_1st_dimension_string + ' were '
        else:
            response_string += ', latest_value for ' + the_1st_dimension_string + ' were '

        the_1st_amount = result_set[the_1st_dimension_value.lower()][1]
        the_2nd_amount = result_set[the_2nd_dimension_value.lower()][1]
        
        the_1st_amount_formatted = '{:,.0f}'.format(the_1st_amount)
        the_2nd_amount_formatted = '{:,.0f}'.format(the_2nd_amount)
        
        if (the_1st_amount == the_2nd_amount):
            response_string += 'the same as for ' + the_2nd_dimension_string + ', $' + the_2nd_amount_formatted
        else:
            if (the_1st_amount < the_2nd_amount):
                percent_different = (the_1st_amount - the_2nd_amount) / the_2nd_amount * -1
                higher_or_lower = 'lower'
            else:
                percent_different = (the_1st_amount - the_2nd_amount) / the_2nd_amount
                higher_or_lower = 'higher'

            response_string += '{:.0%}'.format(percent_different) + ' ' + higher_or_lower + ' than for ' + the_2nd_dimension_string
            response_string += ': $' + the_1st_amount_formatted + ' as opposed to $' + the_2nd_amount_formatted + '.'

    else:  # >2, should not occur
        response_string = 'I seem to have a problem, I got back ' + str(result_count) + ' ' + dimension + '.'
    
    logger.debug('<<IHBot>> response_string = ' + response_string) 

    method_duration = time.perf_counter() - method_start
    method_duration_string = 'method time = %.0f' % (method_duration * 1000) + ' ms'
    logger.debug('<<IHBot>> "Method duration is: ' + method_duration_string) 

    return helpers.close(session_attributes, 'Fulfilled', {'contentType': 'PlainText','content': response_string})   
