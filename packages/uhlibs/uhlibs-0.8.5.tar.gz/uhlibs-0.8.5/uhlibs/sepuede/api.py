import json
import logging

import requests

log = logging.getLogger(__name__)


class SePuedeApiSessionError(RuntimeError):
    pass

# override https://github.com/psf/requests/blob/main/src/requests/sessions.py
class SePuedeApiSession(requests.Session):

    def __init__(self, api_base_url, api_key):
        # requests.Session.__init__() takes no *args, **kwargs
        super().__init__()

        # verify that /api is present at the end of the provided URL:
        if api_base_url.endswith("/api"):
            self.api_base_url = api_base_url
        else:
            self.api_base_url = api_base_url + '/api'

        # add ApiKey to headers
        self.headers.update({"ApiKey": api_key})

    def request(self, method, url, **kwargs):
        if url[0] != '/':
            raise SePuedeApiSessionError(f"url should be relative to {self.api_base_url}; got {url}")
        api_url = ''.join([self.api_base_url, url])
        log.debug(f"{method} {url} -> {api_url} {kwargs}")
        return super().request(method, api_url, **kwargs)


def getActivityParticipation(sepuede_api, activityType, stepOrDetailId):
    """returns json list of ActivityParticipation records

    {
        'type': 'Step',
        'stepDetailId': 130,
        'workerId': '545',
        'responseString': None,
        'responseBoolean': None,
        'responseDate': None,
        'responseNumber': None,
        'responseDecimal': None,
        'responseOption': None,
        'responseOptions': None
    }

    activityType is Step|Detail"""
    params = {'type': activityType, 'stepDetailId': stepOrDetailId}
    http_response = sepuede_api.get('/ActivityParticipation', params=params)
    json_response = json.loads(http_response.text)
    return json_response

def getStrikeWalkDetailsForActivity(sepuede_api, detailId):
    """returns dict keyed on (type, detailId, workerId)

    values are dicts containing responseNumber & responseString fields

    {('Detail', 205, 915): {'responseNumber': 2.0, 'responseString': '1.85'}, ...}

    type part of the key is always 'Detail'"""
    def _reshape(rows):
        data = {}
        # responseNumber & responseString are only 2 values with data
        COLS = ['responseString', 'responseNumber']
        for row in rows:
            key = (row['type'], row['stepDetailId'], row['workerId'])
            val = {}
            for col in COLS:
                val[col] = row[col]
            data[key] = val
        return data

    details = getActivityParticipation(sepuede_api, "Detail", detailId)
    details = _reshape(details)
    return details

def insertActivityParticipation(sepuede_api, stepId, detailId, workerId, hoursWalked):
    # worker may or may not already have a record associating them with step
    # if they do, this request will return 409 Conflict & we can ignore it
    step_activity = {
        'type': 'Step',
        'stepDetailId': stepId,
        'workerId': workerId,
    }
    response = sepuede_api.post('/ActivityParticipation', data=step_activity)
    log.info(f"insert {step_activity}: {response.status_code}")

    detail_activity = {
        'type': 'Detail',
        'stepDetailId': detailId,
        'workerId': workerId,
        'responseString': "{:.2f}".format(hoursWalked),
        'responseNumber': round(hoursWalked, 2),
    }
    response = sepuede_api.post('/ActivityParticipation', data=detail_activity)
    if response.status_code == 409:
        # shouldn't happen when called from sync_strike_walks, not sure if
        # there are other contexts where this should raise an exception?
        log.warning(f"insert {detail_activity}: {response.status_code}")
    else:
        log.info(f"insert {detail_activity}: {response.status_code}")

def updateActivityDetailParticipation(sepuede_api, detailId, workerId, hoursWalked):
    # there is no data associated with steps that might be updated, only need to update detail
    detail_activity = {
        'type': 'Detail',
        'stepDetailId': detailId,
        'workerId': workerId,
        'responseString': "{:.2f}".format(hoursWalked),
        'responseNumber': round(hoursWalked, 2),
    }
    # endpoint supports PUT & PATCH, requires (type, stepDetailId, workerId)
    response = sepuede_api.patch('/ActivityParticipation', data=detail_activity)
    log.info(f"patch {detail_activity}: {response.status_code}")

