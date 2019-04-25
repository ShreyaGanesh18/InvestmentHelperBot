
import time
import logging



logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# adjust dimension values as necessary prior to inserting into where clause
def pre_process_query_value(key, value):
    logger.debug('<<IHBot>> pre_process_query_value(%s, %s)', key, value)
    value = value.replace("'", "''")    # don't allow any 's in WHERE clause

    logger.debug('<<IHBot>> pre_process_query_value() - returning key=%s, value=%s', key, value)
       
    return value

