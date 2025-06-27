from pymongo import MongoClient
from datetime import datetime

#Initialize MongoDB connection

client = MongoClient("mongodb://localhost:27017/")
db = client["cti_dashboard"]
ioc_collection = db["ioc_data"]

#IOC Data

def insert_ioc(ioc_entry):
    """
    Inserts a new IOC entry into MongoDB.
    Example ioc_entry = {
        'value': '1.2.3.4',
        'type': 'ip',
        'tags': ['malicious'],
        'date_added': datetime.utcnow(),
        'source': 'VirusTotal',
        'threat_level': 'high'
    }
    """
    existing = ioc_collection.find_one({'value': ioc_entry['value']})
    if not existing:
        ioc_collection.insert_one(ioc_entry)
        return True
    return False

#Check if IOC Exist

def check_ioc(value):
    """
    Checks if an IOC already exists.
    """
    return ioc_collection.find_one({'value': value})

#Tag/Annotate an IOC

def add_tag_to_ioc(ioc_value, tag):
    """
    Adds a tag to an existing IOC.
    """
    ioc_collection.update_one(
        {'value': ioc_value},
        {'$addToSet': {'tags': tag}}  # avoid duplicate tags
    )

#Data for chart generation 

def get_trend_data(days=7):
    """
    Returns threat counts for the last `days` days.
    Output: List of (date, count) tuples
    """
    from datetime import timedelta

    today = datetime.utcnow().date()
    trend = []

    for i in range(days):
        day = today - timedelta(days=i)
        next_day = day + timedelta(days=1)

        count = ioc_collection.count_documents({
            "date_added": {"$gte": datetime.combine(day, datetime.min.time()),
                           "$lt": datetime.combine(next_day, datetime.min.time())}
        })
        trend.append((str(day), count))

    return trend[::-1]  # from oldest to newest

#Get all IOC's or by type

def get_all_iocs():
    return list(ioc_collection.find())

def get_iocs_by_type(ioc_type):
    return list(ioc_collection.find({'type': ioc_type}))

