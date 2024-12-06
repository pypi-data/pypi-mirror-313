import argparse
from decimal import Decimal
import logging

from uhlibs.sepuede.api import (
    getStrikeWalkDetailsForActivity,
    insertActivityParticipation,
    updateActivityDetailParticipation,
)
from uhlibs.sepuede.odata import getActivityIdsForStrikeName, getActivityIdsSet

log = logging.getLogger(__name__)

SYNC_DESC = """
  Sync walk events from StrikeDB to SePuede

  By default only prints changes that would be made to STDOUT, you have to use
  the --no-test-run flag to send updates to Se Puede

  For UPDATEs to Se Puede, where there is already data in Se Puede but the
  numbers don't match, --test-run output will look like this:

    UPDATE (173, '1881', Decimal('5.01')); run with --no-test-run to update SePuede

  Where the 173 corresponds to an ActivityStepDetailId, '1881' is the WorkerId,
  and the Decimal value is hours walked.

  For rows that that would be INSERTed, the data looks pretty much the same,
  but there is an ActivityStepId (aka action_id) before the detail_id:

    INSERT (136, 173, '1881', Decimal('5.01')); run with --no-test-run to update SePuede

  If you include --debug &/or --http-debug log messages will be written to STDERR
  so you can use bash redirection to create a debug log while not obscuring the output:

    sync-strike-walks --strike-id 28 --debug 2>/tmp/sync-debug.log
"""
sync_argparser = argparse.ArgumentParser(description=SYNC_DESC,
                                         formatter_class=argparse.RawDescriptionHelpFormatter)
sync_argparser.add_argument('--debug', action='store_true',
    help='increase log level to DEBUG')
sync_argparser.add_argument('--http-debug', action='store_true',
    help='print http requests to STDERR')
sync_argparser.add_argument('--test-run', action=argparse.BooleanOptionalAction, default=True,
    help='by default prints changes that would be made to STDOUT; use --no-test-run to send changes to sePuede')
sync_argparser.add_argument('--strike-id', type=int, required=True)

STRIKEDB_ACTIVITY_ID_SETS_QUERY = """
    SELECT DISTINCT ActivityId, ActivityActionId, ActivityActionDetailId
    FROM SePuedeActivityTracking
    WHERE ActivityId = ?
    ORDER BY ActivityId, ActivityActionId, ActivityActionDetailId;
"""

STRIKEDB_ACTIVITY_HISTORY_QUERY = """
    SELECT
        ActivityActionId AS action_id,
        ActivityActionDetailId AS detail_id,
        WorkerId AS worker_id,
        HoursWalked AS hours_walked
    FROM SePuedeActivityTracking
    WHERE ActivityId = ?
    ORDER BY 
        ActivityActionId ASC, ActivityActionDetailId ASC, WorkerId ASC,
        -- in case of multiple rows, select them in order created so only most recent is used
        CreatedOn ASC;
"""

STRIKEDB_STRIKE_NAME_BY_ID_QUERY = 'SELECT Title FROM StrikeInfo WHERE ID = ?;'

# don't bother to update SePuede if difference is within this threshold
UPDATE_DETAIL_TOLERANCE = Decimal(0.02)

def cmp_within_update_tolerance(a, b):
    # this *should* work for a,b which are Decimal,float,int,strings that look like numbers
    return abs(Decimal(a) - Decimal(b)) < UPDATE_DETAIL_TOLERANCE

class StrikeSyncError(RuntimeError):
    pass

def get_activity_ids_set(strike_cursor, activity_id):
    """returns list of 3-tuples: (activity_id, action_id, detail_id)"""
    strike_cursor.execute(STRIKEDB_ACTIVITY_ID_SETS_QUERY, activity_id)
    rows = strike_cursor.fetchall()
    ids = []
    for row in rows:
        ids.append((row.ActivityId, row.ActivityActionId, row.ActivityActionDetailId))
    return set(ids)

def get_activity_history(strike_cursor, activity_id):
    """returns list of dicts representing SePuedeActivityTracking rows"""
    activity_history = []
    result = strike_cursor.execute(STRIKEDB_ACTIVITY_HISTORY_QUERY, activity_id)
    col_names = [column[0] for column in strike_cursor.description]
    for row in result:
        activity_history.append(dict(zip(col_names, row)))
    return activity_history

def get_strike_name_by_id(strike_cursor, strike_id):
    result = strike_cursor.execute(STRIKEDB_STRIKE_NAME_BY_ID_QUERY, strike_id)
    strike_name = result.fetchval()
    return strike_name

def sync_strike_activity(strike_cursor, odata_svc, sepuede_api, activity_id, test_run=True):
    """sync_strike_activity is intended to be called by sync_strike_walks()"""
    # strike_ids_set looks like {(activity_id, action_id, detail_id), ...}
    strike_ids_set = get_activity_ids_set(strike_cursor, activity_id)
    log.debug(f"strike_ids_set for activity_id={activity_id}: {strike_ids_set}")
    # strikedb "action" is stored as sepuede "step": (activityId, activityStepId, activityStepDetailId)
    sepuede_ids_set = getActivityIdsSet(odata_svc, activity_id)
    log.debug(f"sepuede_ids_set for activity_id={activity_id}: {sepuede_ids_set}")
    # strike_only is set of ids from strike_ids_set not found in sepuede_ids_set
    # if there are ids in strike db *not* in se puede, how did they get logged?
    strike_only = strike_ids_set.difference(sepuede_ids_set)
    for act_id, step_id, det_id in strike_only:
        log.warning(f"Only in StrikeDB: Action={act_id} Step={step_id} Detail={det_id}")
    # if there is data in sepuede not in strike, may be newly set up/bad data no walks were ever logged for
    sepuede_only = sepuede_ids_set.difference(strike_ids_set)
    for act_id, step_id, det_id in sepuede_only:
        log.warning(f"Only in Se Puede: Action={act_id} Step={step_id} Detail={det_id}")
    shared_ids_set = strike_ids_set.intersection(sepuede_ids_set)
    log.info(f"{len(shared_ids_set)} common sets of (activity_id, step_id, detail_id): {shared_ids_set}")

    # iterate over walks in strikedb & verify data exists in se puede
    strikedb_history = get_activity_history(strike_cursor, activity_id)
    sepuede_history = {}
    # first member of shared_ids_set is activity_id; we already have it
    for (_, step_id, detail_id) in shared_ids_set:
        details = getStrikeWalkDetailsForActivity(sepuede_api, detail_id)
        sepuede_history.update(details)

    for row in strikedb_history:
        activity_ids = (activity_id, row["action_id"], row["detail_id"])
        if activity_ids not in shared_ids_set:
            log.info(f"skipping {activity_ids}; id set not in both strike db & sepuede")
            continue

        sepuede_key = ("Detail", row["detail_id"], row["worker_id"])
        try:
            sepuede_data = sepuede_history[sepuede_key]
        except KeyError:
            # Se Puede has no record of this worker's activity for this detail
            args = (row['action_id'], row['detail_id'], row['worker_id'], row['hours_walked'])
            if test_run:
                msg = " ".join([
                    "INSERT ACTION;",
                    f"StrikeDb (action, detail, worker, hours)={args}",
                    f"SePuede={sepuede_key} HAS NO DATA",
                ])
                print(msg)
            else:
                insertActivityParticipation(sepuede_api, *args)
            continue

        log.info(f"compare {row} vs. {sepuede_key} {sepuede_data}")
        sepuede_hours = Decimal(sepuede_data['responseString'])
        # exact comparison seems too picky; suspect precision difference in
        # table definintions in the dbs cause a lot of off-by-100th-errors
        #if row['hours_walked'] == sepuede_hours:
        if cmp_within_update_tolerance(row['hours_walked'], sepuede_hours):
            continue

        log.info(f"{row['hours_walked']} <> {sepuede_hours}")
        args = (row['detail_id'], row['worker_id'], row['hours_walked'])
        if test_run:
            msg = " ".join([
                f"UPDATE DETAIL; action_id={row['action_id']}",
                f"StrikeDb (detail, worker, hours)={args}",
                f"SePuede={sepuede_key} {sepuede_data}",
            ])
            print(msg)
        else:
            updateActivityDetailParticipation(sepuede_api, *args)

def sync_strike_walks(strike_cursor, odata_svc, sepuede_api, strike_id, test_run=True):
    """sync walk data from StrikeDB to Se Puede"""
    # need strike name to look up activity ids in se puede
    strike_name = get_strike_name_by_id(strike_cursor, strike_id)
    if not strike_name:
        raise StrikeSyncError(f"Cannot find a name for strike id {strike_id}")
    log.info(f"begin sync for strike id={strike_id} name={strike_name}")

    # query se puede activity ids
    daily_activity_id, weekly_activity_id = getActivityIdsForStrikeName(odata_svc, strike_name)
    if not all([daily_activity_id, weekly_activity_id]):
        err = " ".join([
            f"Could not find ids for StrikeId={strike_id} [{strike_name}]:",
            f"daily={daily_activity_id} weekly={weekly_activity_id}",
        ])
        raise StrikeSyncError(err)

    # sync strikedb data to sepuede
    for activity_id in (daily_activity_id, weekly_activity_id):
        sync_strike_activity(strike_cursor, odata_svc, sepuede_api,
                             activity_id, test_run=test_run)

