import os
import sys
from datetime import datetime, timedelta
from pprint import pprint

from dotenv import load_dotenv

# Load env vars from a .env file
load_dotenv()

sys.path.insert(0, "")

from ezoff import *

res = create_service(
    14753,
    {
        "service[start_date]": "01/01/2018",
        "service_start_time": "08:00",
        "service[end_date]": "01/09/2018",
        "service_end_time": "15:15",
        "service_type_name": "Other",
        "service[description]": "This is a test service",
    },
)
print(res)
pass
