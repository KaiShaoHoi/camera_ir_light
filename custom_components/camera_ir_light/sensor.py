import asyncio
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.const import STATE_ON, STATE_OFF
from homeassistant.helpers.entity import Entity
from .const import DOMAIN, CONF_HOST, CONF_POLLING_INTERVAL

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the camera_ir_light sensor platform."""
    host = config.get(CONF_HOST)
    polling_interval = config.get(CONF_POLLING_INTERVAL, 60)

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

    async def async_update(self):
        """Update the sensor."""
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
                        break  # 一旦匹配到 "display switch(color -> blackwhite)." 就停止遍历

            # 根据标志位设置 self._state
            if blackwhite_flag:
                self._state = STATE_ON
            elif color_flag:
                self._state = STATE_OFF
            else:
                self._state = STATE_ON

        except Exception as e:
            self._state = STATE_OFF
            # 在实际使用中，可以记录日志或者通过其他途径报告错误
            _LOGGER.error(f"Error updating sensor state: {e}")

        # 等待指定的轮询间隔时间
        await asyncio.sleep(self._polling_interval)