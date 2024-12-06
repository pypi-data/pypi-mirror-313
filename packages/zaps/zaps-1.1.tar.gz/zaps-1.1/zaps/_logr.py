from distfit import distfit
import logging

# distfit module calls root logger and configures a console 
# handler with custom formatting so we force format on that 
# handler and skip creating another one for the internal logger
logging.basicConfig(format = ('%(name)s **%(levelname)s** %(message)s'), force = True) 

# create logger for internal use
_z_log = logging.getLogger('[zaps]') # parent logger for zaps and child of root
_z_log.setLevel(logging.INFO)