import logging
from datetime import timedelta
import requests
from homeassistant.const import CONF_HOST, STATE_ON, STATE_OFF
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.util import Throttle
from .const import DOMAIN, CONF_POLLING_INTERVAL

_LOGGER = logging.getLogger(__name__)

DEFAULT_POLLING_INTERVAL = timedelta(seconds=60)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the camera_ir_light sensor platform."""
    host = config.get(CONF_HOST)
    polling_interval = config.get(CONF_POLLING_INTERVAL, DEFAULT_POLLING_INTERVAL)

    coordinator = IRLightSensorDataCoordinator(hass, host, polling_interval)
    add_entities([IRLightSensor(coordinator, host)], True)


class IRLightSensorDataCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the camera IR light sensor."""

    def __init__(self, hass, host, interval):
        """Initialize."""
        self.host = host
        self.file_url = f"http://{self.host}/log/syslog.txt"

        super().__init__(hass, _LOGGER, name="IR Light Sensor", update_interval=interval)

    @Throttle(DEFAULT_POLLING_INTERVAL)
    def update(self):
        """Fetch data from IR light sensor."""
        try:
            response = requests.get(self.file_url, timeout=10)
            text = response.text

            color_flag = "display switch(blackwhite -> color)." in text
            blackwhite_flag = "display switch(color -> blackwhite)." in text

            if blackwhite_flag:
                self.data = STATE_ON
            elif color_flag:
                self.data = STATE_OFF
            else:
                self.data = STATE_ON
        except Exception as e:
            _LOGGER.error(f"Error updating sensor state: {e}")
            self.data = STATE_OFF


class IRLightSensor(Entity):
    """Representation of a camera_ir_light sensor."""

    def __init__(self, coordinator, host):
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._host = host
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return "IR Light Sensor"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data

    @property
    def should_poll(self):
        """Return the polling state."""
        return False

    async def async_update(self):
        """Update the sensor."""
        await self.hass.async_add_executor_job(self.coordinator.update)