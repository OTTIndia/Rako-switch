"""Platform for Rako switch integration."""
import logging

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity

from .bridge import RakoBridge  # Assuming this handles the connection to Rako devices
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up Rako switch platform."""
    rako_domain_entry_data = hass.data[DOMAIN][entry.data[CONF_MAC]]
    rako_bridge: RakoBridge = rako_domain_entry_data["rako_bridge_client"]

    switches = []
    for switch_data in rako_bridge.get_switches():  # Assuming this method returns a list of switch info
        switches.append(RakoSwitch(switch_data, rako_bridge))

    async_add_entities(switches, update_before_add=True)

class RakoSwitch(SwitchEntity):
    """Representation of a Rako switch."""

    def __init__(self, switch_data, bridge: RakoBridge):
        """Initialize the switch."""
        self._bridge = bridge
        self._name = switch_data["name"]
        self._state = switch_data["state"]
        self._id = switch_data["id"]

    @property
    def name(self):
        """Return the name of the switch."""
        return self._name

    @property
    def is_on(self):
        """Return true if the switch is on."""
        return self._state

    async def async_turn_on(self, **kwargs):
        """Turn the switch on."""
        await self._bridge.turn_on_switch(self._id)  # Assuming this method turns on the switch
        self._state = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Turn the switch off."""
        await self._bridge.turn_off_switch(self._id)  # Assuming this method turns off the switch
        self._state = False
        self.async_write_ha_state()
