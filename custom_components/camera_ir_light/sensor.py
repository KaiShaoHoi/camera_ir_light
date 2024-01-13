import requests
import time
from homeassistant.const import STATE_ON, STATE_OFF
from homeassistant.helpers.entity import Entity

# 导入你的红外摄像头库或相关的库
from .const import DOMAIN

CONF_HOST = "host"
CONF_POLLING_INTERVAL = "polling_interval"

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the camera_ir_light sensor platform."""
    host = config.get(CONF_HOST)
    polling_interval = config.get(CONF_POLLING_INTERVAL, 60)

    add_entities([IRLightSensor(host, polling_interval)], True)


class IRLightSensor(Entity):
    """Representation of a camera_ir_light sensor."""

    def __init__(self, host, polling_interval):
        """Initialize the sensor."""
        self._host = host
        self._polling_interval = polling_interval
        self._state = None  # 初始状态为未知
        self._file_url = f"http://{self._host}/log/syslog.txt"
        self._session = requests.Session()

    @property
    def name(self):
        """Return the name of the sensor."""
        return "IR Light Sensor"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update(self):
        """Update the sensor."""
        try:
            color_flag = False
            blackwhite_flag = False
            
            with self._session.get(self._file_url, stream=True) as response:
                for line in response.iter_lines(decode_unicode=True):
                    if line and "display switch(blackwhite -> color)." in line:
                        color_flag = True
                    elif line and "display switch(color -> blackwhite)." in line:
                        blackwhite_flag = True
                        break  # 一旦匹配到 "display switch(color -> blackwhite)." 就停止遍历

            # 根据标志位设置 self._state
            if blackwhite_flag:
                self._state = STATE_ON
            elif color_flag:
                self._state = STATE_OFF
            else:
                self._state = STATE_ON

        except requests.RequestException as e:
            self._state = STATE_OFF
            # 在实际使用中，可以记录日志或者通过其他途径报告错误
            print(f"Error updating sensor state: {e}")
        finally:
            time.sleep(self._polling_interval)
