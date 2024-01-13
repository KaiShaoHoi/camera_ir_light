from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
import voluptuous as vol
from homeassistant.components import translation
from .const import DOMAIN

# 定义配置常量
CONF_HOST = "host"
CONF_POLLING_INTERVAL = "polling_interval"

# 定义配置模式
CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: {
            vol.Optional(CONF_HOST): cv.string,
            vol.Optional(CONF_POLLING_INTERVAL, default=60): cv.positive_int,
        }
    },
    extra=vol.ALLOW_EXTRA,
)

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the camera_ir_light component."""
    hass.data[DOMAIN] = {}
    
    if DOMAIN in config:
        # 配置验证
        config[DOMAIN] = CONFIG_SCHEMA(config[DOMAIN])
    
    if translation.LOCALE_DOMAIN not in hass.data:
        hass.data[translation.LOCALE_DOMAIN] = "zh_CN"
    return True
