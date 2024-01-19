import logging
from datetime import timedelta
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.const import STATE_ON, STATE_OFF
from homeassistant.helpers.entity import Entity
from .const import DOMAIN, CONF_HOST, CONF_POLLING_INTERVAL

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(seconds=60)  # 默认轮询间隔，可以根据需要调整

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the camera_ir_light sensor platform."""
    host = config.get(CONF_HOST)
    polling_interval = config.get(CONF_POLLING_INTERVAL, SCAN_INTERVAL.total_seconds())

    async_add_entities([IRLightSensor(hass, host, polling_interval)], True)

class IRLightSensor(Entity):
    """Representation of a camera_ir_light sensor."""

    def __init__(self, hass, host, polling_interval):
        """Initialize the sensor."""
        self.hass = hass
        self._host = host
        self._polling_interval = polling_interval
        self._state = None  # 初始状态为未知
        self._file_url = f"http://{self._host}/log/syslog.txt"

    @property
    def name(self):
        """Return the name of the sensor."""
        return "IR Light Sensor"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def should_poll(self):
        """Return the polling state."""
        return True

    @property
    def scan_interval(self):
        """Return the polling interval for the sensor."""
        return timedelta(seconds=self._polling_interval)

    async def async_update(self):
        """Fetch new state data for the sensor."""
        try:
            color_flag = False
            blackwhite_flag = False

            session = async_get_clientsession(self.hass)
            async with session.get(self._file_url, timeout=10) as response:
                text = await response.text()
                for line in text.splitlines():
                    if "display switch(blackwhite -> color)." in line:
                        color_flag = True
                    elif "display switch(color -> blackwhite)." in line:
                        blackwhite_flag = True
                        break

            if blackwhite_flag:
                self._state = STATE_ON
            elif color_flag:
                self._state = STATE_OFF
            else:
                self._state = STATE_ON

        except asyncio.TimeoutError:
            _LOGGER.warning(f"Timeout error occurred while updating sensor state for {self.name}")
            self._state = STATE_OFF
        except Exception as e:
            _LOGGER.error(f"Error updating sensor state for {self.name}: {e}")
            self._state = STATE_OFF