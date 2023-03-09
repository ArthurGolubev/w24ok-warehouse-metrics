import os
import redis

from loguru import logger
from ReportV2 import Report
from datetime import datetime, timedelta

def archive_report(warh):
    redis_ = redis.Redis(host='redis-service-node-port', port='6379', db='0')
    re = redis_.hgetall(f"{warh}")
    if re:
        logger.info(f"{re=}")
        start_date_download     = datetime.strptime(re[b'start'].decode("utf-8"), "%Y/%m/%d")
        end_date_download       = datetime.strptime(re[b'end'].decode("utf-8"),     "%Y/%m/%d")
        if start_date_download != end_date_download and start_date_download < end_date_download:
            start = start_date_download + timedelta(days=1)
            if start + timedelta(days=6) > end_date_download:
                end = end_date_download
            else:
                end = start + timedelta(days=6)
            period = {
                "start": start,
                "end": end
            }
            if start != end:
                return period
            else:
                return None

if __name__ == "__main__":
    logger.info(f'{__name__}')
    if os.getenv('period'):
        period = archive_report(warh=os.getenv('WARH'))
        if period:    
            r = Report(period=period)
            r.get_report()
            r.clear_data()
            r.send_data()
            logger.info(f"{r.clear_data_=}")
    else:
        r = Report()
        r.get_report()
        r.clear_data()
        r.send_data()
        logger.info(f"{r.clear_data_=}")
