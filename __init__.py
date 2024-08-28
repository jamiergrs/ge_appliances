import logging
import aiohttp
from gehomesdk import GeWebsocketClient
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

DOMAIN = "ge_appliances"
_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict):
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    async with aiohttp.ClientSession() as session:
        geh = GeWebsocketClient(username=entry.data["username"], password=entry.data["password"], region=entry.data["region"])
        try:
            await geh.async_get_credentials_and_run(session)
        except Exception as e:
            _LOGGER.error(f"Error setting up GE Appliances integration: {e}")
            return False

        for appliance in geh.appliances:
            hass.states.async_set(f"{DOMAIN}.{appliance.name}", appliance.attributes)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    return True
