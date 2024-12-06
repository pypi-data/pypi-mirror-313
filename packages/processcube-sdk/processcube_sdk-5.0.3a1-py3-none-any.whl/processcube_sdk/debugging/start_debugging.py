import logging

from processcube_sdk.configuration.config_accessor import ConfigAccessor

logger = logging.getLogger("processcube.debugging")

debugger_started = False

def start_debugging():

    global debugger_started
    if debugger_started:
        return

    debugger_started = True
    
    ConfigAccessor.ensure_from_env()
    debugging_enabled = ConfigAccessor.current().get('debugging', 'enabled', default=False)

    logger.info(f"Debugging is enabled: {debugging_enabled}")

    if debugging_enabled: # only import the debugger, if debugging is enabled
        try:
            debugpy.__version__ # only import if not already imported
        except:
            import debugpy 

        log_to = ConfigAccessor.current().get('debugging', 'log_to', default='stdout')
        #debugpy.log_to(log_to)

        hostname = ConfigAccessor.current().get('debugging', 'hostname', default='localhost')
        port = ConfigAccessor.current().get('debugging', 'port', default=5678)

        logger.info(f"Debugger listen on: Hostname={hostname}, Port={port}")
        debugpy.listen((hostname, port))
        
        wait_for_client = ConfigAccessor.current().get('debugging', 'wait_for_client', default=False)
        if wait_for_client:
            logger.info(f"Debugging is waiting for client to connect ...")
            debugpy.wait_for_client()
            logger.info(f"Debugging is client connected")
        else:
            logger.info(f"Debugging is running without waiting for client to connect, but you can connect to the debugger and set breakpoints!")
