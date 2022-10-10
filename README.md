# PrittyLog

Simple logging module for python3+ based on the original logging.
Creates fancy .html log files.
!!! needs a logs folder in the same location as the MAIN python skript !!!


Import:
#imports and init's the base logger
import "subfolder".prittylog as prittylog

Init:
#configures the name of the module that should be logged, the Main .py should be set as Master(true) every following as false.
log = prittylog.prittylog("Modulename", True/False)

Finishing:
#closes the log (if Master) and generates the .html version of the log
log.end()


Examples:
log.info("SimpleLogMessage- optional escapesafe")
log.critical("SimpleLogMessage- optional escapesafe")
log.warning("SimpleLogMessage- optional escapesafe")
log.error("SimpleLogMessage- optional escapesafe")

"SimpleLogMessage" gets shown directly
everything after the "-" gets BASE64 encoded in python and decoded in the HTML (addictional Informations like a variable in Runtime)


Quickly developed in 5h but still quiet pritty ^^
