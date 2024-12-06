from mixpanel import Mixpanel, Consumer
from seeq import sdk, spy
import hashlib
from ._helper import rate_limit

MIXPANEL_EVENT_VERSION = "1"
CONFIG_UPDATE_INTERVAL_SECONDS = 15*60  # 15 minutes

class EventConstants:
    DLEM_VERSION = "DLEM Version"
    EVENT_VERSION = "Event Version"
    EVENT_NAME = "Event Name"
    EVENT_NAME_LAUNCH = "DLEM Launch"
    EVENT_NAME_VERIFY = "DLEM Verify Project"
    EVENT_NAME_PACKAGE_INSTALL = "DLEM Install Package"
    HOSTNAME = "Hostname"
    SEEQ_VERSION = "Seeq Version"
    USER_ID = "User ID"
    IS_USER_ADMIN = "Is User Admin"
    NUMBER_OF_PROJECTS = "Number of Projects"
    NUMBER_OF_SCHEDULED_NOTEBOOKS = "Number of Projects with Scheduled Notebooks"
    NUMBER_OF_ACTIVE_SCHEDULED_NOTEBOOKS = "Number of Projects with Active Scheduled Notebooks"
    NUMBER_OF_FUNCTIONS = "Number of Functions"
    NUMBER_OF_ADDONS = "Number of Add-On"
    NUMBER_OF_PACKAGED_ADDONS = "Number of Packaged Add-On"
    NUMBER_OF_COMPLETED_PROJECTS = "Number of 3.11 Verified Projects"
    INSTALLED_PACKAGE_NAME = "Installed Package Name"
    NUMBER_OF_COMPLETED_FUNCTIONS = "Number of 3.11 Verified Functions"
    NUMBER_OF_COMPLETED_ADDONS = "Number of 3.11 Verified Add-On"
    NUMBER_OF_COMPLETED_SCHEDULED_NOTEBOOKS = "Number of 3.11 Verified Projects with Scheduled Notebooks"
    NUMBER_OF_COMPLETED_ACTIVE_SCHEDULED_NOTEBOOKS = "Number of 3.11 Verified Projects with Active Scheduled Notebooks"


class MixpanelTracker(Mixpanel):
    _is_telemetry_enabled: bool
    _is_telemetry_anonymized: bool

    def __init__(self, token, consumer=None):
        self._is_telemetry_enabled = False
        self._is_telemetry_anonymized = True
        super().__init__(token, consumer=consumer)

    @rate_limit(interval_seconds=CONFIG_UPDATE_INTERVAL_SECONDS)
    def _update_configuration_options(self):
        try:
            system_api = sdk.SystemApi(spy.client)
            configs = {c.path: c.value for c in system_api.get_server_status().configuration_options}
            self._is_telemetry_enabled = configs.get('Features/Telemetry/Enabled', False)
            self._is_telemetry_anonymized = configs.get('Features/Telemetry/Anonymized', True)
        except Exception as e:
            print('Failed to update telemetry configuration options.')

    def _anonymize(self, value) -> str:
        if value is None or value == '':
            return ''
        to_hash = f'string:{len(value)}:{value}'.encode()
        return hashlib.sha1(to_hash).hexdigest()

    def track(self, distinct_id, event_name, properties=None, anonymous_props=None):
        self._update_configuration_options()

        if not self._is_telemetry_enabled:
            return
        
        # This doesnt work for properties as nested dict
        if self._is_telemetry_anonymized and anonymous_props:
            for prop in anonymous_props:
                if prop in properties:
                    properties[prop] = self._anonymize(properties[prop])
        if self._is_telemetry_anonymized:
            distinct_id = self._anonymize(distinct_id)

        super().track(distinct_id, event_name=event_name, properties=properties)

