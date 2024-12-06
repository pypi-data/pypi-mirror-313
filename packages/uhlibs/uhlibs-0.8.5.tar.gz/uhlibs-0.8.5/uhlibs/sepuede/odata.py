import logging

log = logging.getLogger(__name__)


def _entity_to_dict(entity, entity_class):
    properties = [ p["name"] for p in entity_class.__odata_schema__["properties"] ]
    entity_dict = dict([ (p, getattr(entity, p)) for p in properties ])
    return entity_dict

def _entities_to_dicts(entities, entity_class):
    entity_dicts = [ _entity_to_dict(e, entity_class) for e in entities ]
    return entity_dicts

# https://dev.azure.com/burstingsilver/UniteHere/_wiki/wikis/UniteHere.wiki/1393/ActivitiesWithStepAndDetails
def getActivitiesWithStepAndDetails(odata_svc, activityId):
    ActivitiesWithStepAndDetails = odata_svc.entities["ActivitiesWithStepAndDetails"]
    query = odata_svc.query(ActivitiesWithStepAndDetails)
    entities = query.filter(ActivitiesWithStepAndDetails.ID == activityId).all()
    dicts = _entities_to_dicts(entities, ActivitiesWithStepAndDetails)
    return dicts

def getActivityIdsForStrikeName(odata_svc, strikeName):
    """return 2-tuple (dailyActivityId, weeklyActivityId) for strikeName

    If either activity with the expected name does not exist in the db, raises RuntimeError"""
    dailyActivityName = f"{strikeName} daily"
    weeklyActivityName = f"{strikeName} weekly"
    dailyActivityId = weeklyActivityId = None

    entity = odata_svc.entities["Activity"]
    query = odata_svc.query(entity)
    crit = (entity.DESCRIPTION_EN == dailyActivityName) | (entity.DESCRIPTION_EN == weeklyActivityName)
    activities = query.filter(crit).all()
    for activity in activities:
        if activity.DESCRIPTION_EN == dailyActivityName:
            dailyActivityId = activity.ID
        elif activity.DESCRIPTION_EN == weeklyActivityName:
            weeklyActivityId = activity.ID

    if not dailyActivityId or not weeklyActivityId:
        log.warning(" ".join([
            "Could not find Activity Ids for names:",
            f"'{dailyActivityName}':{dailyActivityId}",
            f"'{weeklyActivityName}':{weeklyActivityId}",
        ]))
    return dailyActivityId, weeklyActivityId

def getActivityIdsSet(odata_svc, activityId):
    """returns list of 3-tuples: (activityId, activityStepId, activityStepDetailId)"""
    Activity = odata_svc.entities["Activity"]
    query = odata_svc.query(Activity)
    Q = f"$filter=ID eq {activityId}&$expand=steps($select=ID;$expand=details($select=ID))"
    rows = query.raw(Q)
    ids = []
    for activity in rows:
        for step in activity["Steps"]:
            stepId = step["ID"]
            for detail in step["Details"]:
                detailId = detail["ID"]
                ids.append((activityId, stepId, detailId))
    return set(ids)

def getActivityStepsforActivityId(odata_svc, activityId):
    """returns list of dicts, one representing each ActivityStep"""
    # [{'ID': 130, 'ACTIVITY_ID': 22, 'ACTION_TYPE_ID': 29, 'DESCRIPTION_EN':
    #   '10/09/2023', 'DESCRIPTION_ES': '10/09/2023', 'ACTION_DATE':
    #   '2023-10-09T00:00:00Z', 'SORT_ORDER': 1, 'WORKER_COUNT': 3}, ...]
    Activity = odata_svc.entities["Activity"]
    query = odata_svc.query(Activity)
    steps = query.filter(Activity.ID == activityId) \
                 .expand(Activity.Steps) \
                 .select(Activity.Steps) \
                 .first()['Steps']
    return steps

# 404. But most errors are 404. Is endpoint not queryable?
def getActivityStepDetailsForActivityStepIds(odata_svc, activityStepId):
    """"returns dict keyed on ActivityStepId, values are lists of dicts
        representing ActivityStepDetails"""
    ActivityStep = odata_svc.entities["ActivityStep"]
    query = odata_svc.query(ActivityStep)
    result = query.filter(ActivityStep.ID == activityStepId) \
                  .expand(ActivityStep.Details) \
                  .select(ActivityStep.ID,ActivityStep.Details) \
                  .all()
    return result

def getRecentActivities(odata_svc, limit=24):
    """returns a list of dicts, each representing a Activity"""
    rows = []
    entity = odata_svc.entities["Activity"]
    query = odata_svc.query(entity).order_by(entity.ID.desc()).limit(limit)
    for row in query:
        rows.append({
            "id": row.ID,
            "activity_date": row.ACTIVITY_DATE,
            "desc_en": row.DESCRIPTION_EN,
        })
    return rows
