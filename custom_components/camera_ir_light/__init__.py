from homeassistant.core import HomeAssistant
from .const import DOMAIN

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the camera_ir_light component."""
    hass.data[DOMAIN] = {}
    
    if translation.LOCALE_DOMAIN not in hass.data:
        hass.data[translation.LOCALE_DOMAIN] = "zh_CN"
    return True
