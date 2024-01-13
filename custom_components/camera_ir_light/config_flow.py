from homeassistant import config_entries
from homeassistant.core import callback
import voluptuous as vol

from .const import DOMAIN
from .translations import DOMAIN_TEXTS

CONF_HOST = "host"
CONF_POLLING_INTERVAL = "polling_interval"

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            host = user_input.get(CONF_HOST)
            polling_interval = user_input.get(CONF_POLLING_INTERVAL)

            # 在这里可以添加一些验证逻辑，例如检查host是否有效

            return self.async_create_entry(
                title=DOMAIN_TEXTS["config"]["step"]["user"]["title"],
                data={
                    CONF_HOST: host,
                    CONF_POLLING_INTERVAL: polling_interval,
                },
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_HOST): str,
                vol.Required(CONF_POLLING_INTERVAL, default=60): int,
            }),
            errors=errors,
        )
