import logging
import os
from conf import setting

def toLog(log_type,msg):
    logger=logging.getLogger(log_type)
    logger.setLevel(setting.LOG_LEVEL)

    # tofile
    file_path=os.path.join(setting.BASE_DIR,"log",setting.LOG_TYPE[log_type])

    fh=logging.FileHandler(file_path)
    fh.setLevel(setting.LOG_LEVEL)

    log_file_format=logging.Formatter(setting.FILE_FORMAT)
    log_file_format.datefmt=setting.DATE_FORMAT     # 时间格式

    fh.setFormatter(log_file_format)

    logger.addHandler(fh)

    # tostream
    sh=logging.StreamHandler()
    sh.setLevel(setting.LOG_LEVEL)
    log_stream_format=logging.Formatter(setting.STREAM_FORMAT)
    log_stream_format.datefmt=setting.DATE_FORMAT     # 时间格式
    sh.setFormatter(log_stream_format)
    logger.addHandler(sh)

'''
%(name)s            Name of the logger (logging channel)
    %(levelno)s         Numeric logging level for the message (DEBUG, INFO,
                        WARNING, ERROR, CRITICAL)
    %(levelname)s       Text logging level for the message ("DEBUG", "INFO",
                        "WARNING", "ERROR", "CRITICAL")
    %(pathname)s        Full pathname of the source file where the logging
                        call was issued (if available)
    %(filename)s        Filename portion of pathname
    %(module)s          Module (name portion of filename)
    %(lineno)d          Source line number where the logging call was issued
                        (if available)
    %(funcName)s        Function name
    %(created)f         Time when the LogRecord was created (time.time()
                        return value)
    %(asctime)s         Textual time when the LogRecord was created
    %(msecs)d           Millisecond portion of the creation time
    %(relativeCreated)d Time in milliseconds when the LogRecord was created,
                        relative to the time the logging module was loaded
                        (typically at application startup time)
    %(thread)d          Thread ID (if available)
    %(threadName)s      Thread name (if available)
    %(process)d         Process ID (if available)
    %(message)s         The result of record.getMessage(), computed just as
                        the record is emitted
'''
