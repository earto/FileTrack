import voluptuous as vol
import os
from homeassistant import config_entries
import homeassistant.helpers.config_validation as cv
from .const import DOMAIN, CONF_FOLDER_PATHS, CONF_FILTER, CONF_SORT, CONF_RECURSIVE, DEFAULT_FILTER, DEFAULT_SORT, DEFAULT_RECURSIVE, SORT_OPTIONS

class FileTrackConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for FileTrack."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Stap die de gebruiker ziet bij het toevoegen."""
        errors = {}

        if user_input is not None:
            folder = user_input[CONF_FOLDER_PATHS]
            if not os.path.isdir(folder):
                try:
                    os.makedirs(folder, exist_ok=True)
                except Exception:
                    errors["base"] = "invalid_path"
            if not errors:
                return self.async_create_entry(
                    title=user_input["name"], 
                    data=user_input
                )

        # Het formulier definitie
        data_schema = vol.Schema({
            vol.Required("name"): str,
            vol.Required(CONF_FOLDER_PATHS): str,
            vol.Optional(CONF_FILTER, default=DEFAULT_FILTER): str,
            vol.Optional(CONF_SORT, default=DEFAULT_SORT): vol.In(SORT_OPTIONS),
            vol.Optional(CONF_RECURSIVE, default=DEFAULT_RECURSIVE): bool,
        })

        return self.async_show_form(
            step_id="user", 
            data_schema=data_schema, 
            errors=errors
        )
