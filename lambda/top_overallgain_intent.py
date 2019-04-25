import time
import logging
import json
import ihbot_config as ihbot
import ihbot_helpers as helpers
import ihbot_userexits as userexits

# SELECT statement for Top query
TOP_SELECT  = "SELECT {}, overall_gain FROM my_portfolio  "
TOP_JOIN    = " "
TOP_WHERE   = " AND LOWER({}) LIKE LOWER('%{}%') " 
TOP_ORDERBY = " ORDER BY overall_gain desc" 
TOP_DEFAULT_COUNT = '3'

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
        return top_intent_handler(event, session_attributes)


def top_intent_handler(intent_request, session_attributes):
    method_start = time.perf_counter()

    logger.debug('<<IHBot>> top_intent_handler: session_attributes = ' + json.dumps(session_attributes))
    
    session_attributes['greetingCount'] = '1'
    session_attributes['resetCount'] = '0'
    session_attributes['finishedCount'] = '0'
    session_attributes['lastIntent'] = 'Top_Intent'

    # Retrieve slot values from the current request
    slot_values = session_attributes.get('slot_values')

    try:
        slot_values = helpers.get_slot_values(slot_values, intent_request)
    except ihbot.SlotError as err:
        return helpers.close(session_attributes, 'Fulfilled', {'contentType': 'PlainText','content': str(err)})   

    logger.debug('<<IHBot>> "top_intent_handler(): slot_values: %s', slot_values)

    # Retrieve "remembered" slot values from session attributes
    slot_values = helpers.get_remembered_slot_values(slot_values, session_attributes)
    logger.debug('<<IHBot>> "top_intent_handler(): slot_values afer get_remembered_slot_values: %s', slot_values)

    if slot_values.get('count') is None:
        slot_values['count'] = TOP_DEFAULT_COUNT

    if slot_values.get('dimension') is None:
        if len(ihbot.DIMENSIONS.keys()) > 0:
            response_string = 'Please tell me a dimension, for example, "top five '
            for counter, item in enumerate(ihbot.DIMENSIONS.keys()):
                if counter == 0:
                    response_string += item + '".'
                elif counter == 1:
                    response_string += '  I can also report on ' + item
                    if len(ihbot.DIMENSIONS.keys()) == 2:
                        response_string += '.'
                elif counter < (len(ihbot.DIMENSIONS.keys()) - 1):
                    response_string += ', ' + item
                else:
                    if len(ihbot.DIMENSIONS.keys()) == 3:
                        response_string += ' and ' + item + '.'
                    else:
                        response_string += ', and ' + item + '.'
        else:
            response_string = 'Please tell me a dimension, for example, "top five months".'

        return helpers.close(session_attributes, 'Fulfilled', {'contentType': 'PlainText','content': response_string})   

    # If switching dimension, forget the prior remembered value for that dimension
    dimension_slot = ihbot.DIMENSIONS.get(slot_values.get('dimension')).get('slot')
    if dimension_slot is not None:
        slot_values[dimension_slot] = None
        logger.debug('<<IHBot>> "top_intent_handler(): cleared dimension slot: %s', dimension_slot)

    # store updated slot values
    logger.debug('<<IHBot>> "top_intent_handler(): calling remember_slot_values_NEW: %s', slot_values)
    helpers.remember_slot_values(slot_values, session_attributes)

    # Check for minimum required slot values
    if slot_values.get('dimension') is None:
        return helpers.close(session_attributes, 'Fulfilled',
            {'contentType': 'PlainText', 'content': "Sorry, I didn't understand that.  Try \"Top 5 venues for all rock and pop\"."})  

    # Build and execute query 
    try:
        # the SELECT clause is for a particular dimension e.g., top 5 {states}...
        # Example: "SELECT {}, SUM(s.amount) ticket_sales FROM sales s, event e, venue v, category c, date_dim ed  "
        select_clause = TOP_SELECT.format(ihbot.DIMENSIONS.get(slot_values.get('dimension')).get('column'))
    except KeyError:
        return helpers.close(session_attributes, 'Fulfilled',
            {'contentType': 'PlainText', 'content': "Sorry, I don't know what you mean by " + slot_values['dimension']})
            
    # add JOIN clauses 
    where_clause = TOP_JOIN

    # add WHERE clause for each non empty slot
    for dimension in ihbot.DIMENSIONS:
        slot_key = ihbot.DIMENSIONS.get(dimension).get('slot')
        if slot_values[slot_key] is not None:
            value = userexits.pre_process_query_value(slot_key, slot_values[slot_key])
            where_clause += TOP_WHERE.format(ihbot.DIMENSIONS.get(dimension).get('column'), value)

    try:
        # the GROUP BY is by dimension, and the ORDER by is the aggregated fact
        # Example: " GROUP BY {} ORDER BY ticket_sales desc"
        order_by_group_by = TOP_ORDERBY.format(ihbot.DIMENSIONS.get(slot_values.get('dimension')).get('column'))
        order_by_group_by += " LIMIT {}".format(slot_values.get('count'))
    except KeyError:
        return helpers.close(
            session_attributes,
            'Fulfilled',
            {
                'contentType': 'PlainText',
                'content': "Sorry, I don't know what you mean by " + dimension
            }
        )  

    query_string = select_clause + where_clause + order_by_group_by
    logger.debug('<<IHBot>> Athena Query String = ' + query_string)            

    # execute Athena query
    response = helpers.execute_athena_query(query_string)

    # Build response text for Lex
    response_string = ''
    result_count = len(response['ResultSet']['Rows']) - 1
    
    if result_count < int(slot_values.get('count', 0)):
        if result_count == 0:
            response_string += "There weren't any " + slot_values.get('dimension') + " "
        elif result_count == 1:
            response_string += "There was only 1. "
        else:
            response_string += "There were only " + str(result_count) + ". "

    if result_count == 0:
        pass
    elif result_count == 1:
        try:
            response_string += 'The top ' + ihbot.DIMENSIONS.get(slot_values.get('dimension')).get('singular')
        except KeyError:
            response_string += 'The top ' + slot_values.get('dimension')
    else:
        response_string += 'The top ' + str(result_count) + ' ' + slot_values.get('dimension')
  
    # add the English versions of the WHERE clauses
    for dimension in ihbot.DIMENSIONS:
        slot_key = ihbot.DIMENSIONS[dimension].get('slot')
        logger.debug('<<IHBot>> pre top5_formatter[%s] = %s', slot_key, slot_values.get(slot_key))
        if slot_values.get(slot_key) is not None:
            # the DIMENSION_FORMATTERS perform a post-process functions and then format the output
            # Example:  {... 'venue_state': {'format': ' in the state of {}',  'function': get_state_name}, ...}
            if userexits.DIMENSION_FORMATTERS.get(slot_key) is not None:
                output_text = userexits.DIMENSION_FORMATTERS[slot_key]['function'](slot_values.get(slot_key))
                output_text = userexits.DIMENSION_FORMATTERS[slot_key]['format'].lower().format(output_text)
                response_string += ' ' + output_text
                logger.debug('<<IHBot>> top5_formatter[%s] = %s', slot_key, output_text)

    if result_count == 0:
        pass
    elif result_count == 1:
        response_string += ' was '
    else:
        response_string += ' were '
    
    # add the list of top X dimension values to the response text
    if result_count > 0:
        remembered_value = None    
        for counter, item in enumerate(response['ResultSet']['Rows']):
            if counter > 0:
                if counter > 1:
                    response_string += '; and ' if counter == result_count else '; '
                if result_count > 1:
                    response_string += str(counter) + ', '
                    
                value = userexits.post_process_dimension_output(slot_values.get('dimension'), item['Data'][0]['VarCharValue'])
                response_string += value
    
                remembered_value = item['Data'][0]['VarCharValue']

    response_string += '.'

    logger.debug('<<IHBot>> response_string = ' + response_string) 

    # If result count = 1, remember the value for future questions
    if result_count == 1:
        slot_name = ihbot.DIMENSIONS.get(slot_values.get('dimension')).get('slot')
        slot_values[slot_name] = remembered_value

        # store updated query attributes
        helpers.remember_slot_values(slot_values, session_attributes)

    method_duration = time.perf_counter() - method_start
    method_duration_string = 'method time = %.0f' % (method_duration * 1000) + ' ms'
    logger.debug('<<IHBot>> "Method duration is: ' + method_duration_string) 
    
    logger.debug('<<IHBot>> top_intent_handler() - sessions_attributes = %s, response = %s', session_attributes, {'contentType': 'PlainText','content': response_string})

    return helpers.close(session_attributes, 'Fulfilled', {'contentType': 'PlainText','content': response_string})   
