"""
Helper functions for working with python-odata

The naming gets a little weird; it appears that with OData, as a client who
wants to query data from a service, I must instantiate an ODataService() object
representing the remote API, and make requests through that.

`odataclient.get_odata_service(url, session)` instantiates such a client-side
representation of the server-side service.

Furthermore, each server-side endpoint requires a unique client-side
ODataService representation.

See https://tuomur-python-odata.readthedocs.io/en/latest/
"""
import logging
import requests

import odata
from odata.entity import EntityBase
from odata.exceptions import ODataConnectionError

log = logging.getLogger(__name__)

# Subclassing EntityBase to avoid urllib.urljoin()
# urljoin() is stripping /odata part of cls.__odata_service__.url
# compare to upstream version of __odata_url__ here:
# https://github.com/kennethd-uh/python-odata/blob/45a2a670cbfec46d3025dab9ff8ded1d22335534/odata/entity.py#L101
class UhEntityBase(EntityBase):

    @classmethod
    def __odata_url__(cls):
        # used by Query
        if cls.__odata_collection__:
            return "/".join([cls.__odata_service__.url, cls.__odata_collection__])
        else:
            raise ODataConnectionError(f"Cannot query {cls.__name__} objects as they don't have "
                                       f"the collection defined. Are you sure you're querying the correct object ?")

def get_odata_session(api_key):
    sess = requests.Session()
    sess.headers.update({ "ApiKey": api_key })
    return sess

def get_odata_service(url, session, reflect_entities=True, base=UhEntityBase):
    """returns instance of odata.ODataService

    session should be a requests.Session() instance.  Prepare the session
    object in advance with .auth() config or custom headers, such as "ApiKey"
    (the header required by SePuede)

    https://github.com/kennethd-uh/python-odata/blob/master/odata/service.py
    """
    odata_svc = odata.ODataService(url, base=base, reflect_entities=reflect_entities, session=session)
    log.debug("returning service {odata_svc} {id(odata_svc)} for url {url}")
    return odata_svc

def list_entities(odata_svc):
    return sorted(odata_svc.entities.keys())

def entity_schema(odata_svc, entity_name):
    return odata_svc.entities[entity_name].__odata_schema__

def entity_properties(odata_svc, entity_name):
    schema = entity_schema(odata_svc, entity_name)
    pks = [ (p["name"], p["type"]) for p in schema["properties"] if p["is_primary_key"] ]
    properties = [ (p["name"], p["type"]) for p in schema["properties"] if not p["is_primary_key"] ]
    relations = [ (p["name"], p["type"]) for p in schema["navigation_properties"] ]
    return sorted(pks) + sorted(properties + relations)

def dump_schema(odata_svc):
    schema = {}
    entities = list_entities(odata_svc)
    for entity_name in entities:
        schema[entity_name] = entity_properties(odata_svc, entity_name)
    return schema

