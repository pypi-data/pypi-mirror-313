def get_trend(
    keywords: list = None,  # ["AI", "Python", "Data Science"]
    timezone: str = "Europe/Berlin",  # minutes differ from UTC
    cat=0,
    timeframe="today 12-m",
    geo="DE",
    gprop="",
    **kwargs
):
    from pytrends.request import TrendReq
    from pytrends.exceptions import TooManyRequestsError
    import pytz
    from datetime import datetime
    import time
    import requests
    from urllib3.util.retry import Retry

    if isinstance(timezone, str):
        stadt = pytz.timezone(timezone)
        current_time = datetime.now(stadt)  # This will be timezone-aware
        # Convert the timezone-aware datetime to naive UTC datetime
        naive_time = current_time.astimezone(pytz.utc).replace(tzinfo=None)
        tz_offset = stadt.utcoffset(naive_time).seconds // 60  # in minutes
    elif isinstance(timezone, int):
        tz_offset = timezone

    # Initialize TrendReq with correct timezone offset
    pytrends = TrendReq(hl="en-US", tz=tz_offset )
    
    # Ensure that keywords are in list form
    if isinstance(keywords, str):
        keywords = [keywords]

    pytrends.build_payload(keywords, cat=cat, timeframe=timeframe, geo=geo, gprop=gprop)

    res = {}
    # Try fetching data with error handling
    for func_name, fetch_func in [
        ("interest_over_time", pytrends.interest_over_time),
        ("related_topics", pytrends.related_topics),
        ("related_queries", pytrends.related_queries),
        ("categories", pytrends.categories)
    ]:
        try:
            print(f"Fetching {func_name}...")
            res[func_name] = fetch_func()
            print(f"done: {func_name}")
        except TooManyRequestsError:
            print(f"Too many requests error for {func_name}. Retrying...")
            time.sleep(5)  # Delay to avoid spamming the server
            if retries > 0:
                return get_trend(keywords, timezone, cat, timeframe, geo, gprop, retries=retries-1)
            res[func_name] = None
        except requests.exceptions.RequestException as e:
            print(f"Request error for {func_name}: {e}")
            res[func_name] = None
        except Exception as e:
            print(f"Error fetching {func_name}: {e}")
            res[func_name] = None

    return res
