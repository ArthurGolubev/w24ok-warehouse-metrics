from loguru import logger

class ReportError(Exception):
    def __init__(self, where=None, message=None, Traceback=None, period=None):
        self.where = where
        self.message = message
        self.Traceback = Traceback
        self.period = period

    def __str__(self):
        if self.Traceback: logger.critical(f'\n\n\n\nCRITICAL:\n\n{self.Traceback}\nPeriod:\n{self.period}\n#w24ok #Reports')
        if self.where: logger.error(f'\n\n FROM:\n{self.where}\nPeriod:\n{self.period}\n#w24ok #Reports')
        if self.message: logger.error(f'\n\nMessage:\n{self.message}\nPeriod:\n{self.period}\n#w24ok #Reports')