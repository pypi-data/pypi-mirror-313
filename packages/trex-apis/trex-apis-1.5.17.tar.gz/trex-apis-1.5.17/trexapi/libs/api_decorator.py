'''
Created on 22 Apr 2024

@author: jacklok
'''
import logging

logger = logging.getLogger('lib')

def elapsed_time_trace(debug=False, trace_key=None):
    def wrapper(fn):
        import time
        def elapsed_time_trace_wrapper(*args, **kwargs):
            start = time.time()
            result      = fn(*args, **kwargs)
            end = time.time()
            elapsed_time = end - start
            trace_name      = trace_key or fn.func_name
            first_argument  = args[0] if args else None
            logger.info('==================== Start Elapsed Time Trace %s(%s) ===========================', trace_name, first_argument)
            logger.info('elapsed time=%s', ("%.2gs" % (elapsed_time)))
            logger.info('================================================================================')
            return result

        return elapsed_time_trace_wrapper
    return wrapper
