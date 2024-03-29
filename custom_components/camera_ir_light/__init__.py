from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
import voluptuous as vol
from .const import DOMAIN, CONF_HOST, CONF_POLLING_INTERVAL

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

    return True
