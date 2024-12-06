import configparser
import subprocess
from os import environ, path
from pathlib import Path
from typing import Optional

from loguru import logger
from pydantic import BaseModel

from bpkio_api.defaults import DEFAULT_FQDN

DEFAULT_INI_FILE = path.join(path.expanduser("~"), ".bpkio/tenants")


class TenantProfile(BaseModel):
    label: str
    id: int
    fqdn: Optional[str] = DEFAULT_FQDN
    api_key: str
    credential_source: str = "file"


class TenantProfileProvider:
    config = configparser.ConfigParser()

    def __init__(self, filename: Optional[str] = None) -> None:
        f = Path(filename or DEFAULT_INI_FILE)
        if not f.exists():
            f.parent.mkdir(exist_ok=True, parents=True)
            f.touch()

        self._filename = f
        self._read_ini_file()

    @property
    def inifile(self):
        return self._filename

    def get_tenant_profile(self, tenant_label: str):
        tenant_info = self._get_tenant_section(tenant_label)

        tp = TenantProfile(
            label=tenant_label,
            api_key=tenant_info.get("api_key"),
            id=tenant_info.getint("id"),
            fqdn=tenant_info.get("fqdn", DEFAULT_FQDN),
        )
        if "_cred_source" in tenant_info:
            tp.credential_source = tenant_info["_cred_source"]
        return tp

    def list_tenants(self):
        tenants = []
        for section in self.config.sections():
            tenants.append(
                TenantProfile(
                    label=section,
                    id=self.config[section].getint("id"),
                    fqdn=self.config[section].get("fqdn", DEFAULT_FQDN),
                    api_key=self.config[section].get("api_key"),
                )
            )

        return tenants

    def has_tenant_label(self, tenant: str):
        return tenant in self.config

    def has_default_tenant(self):
        return self.has_tenant_label("default")

    # --- Core methods to read and write the `tenants` file ---

    def get_tenant_label_from_working_directory(self):
        try:
            with open(".tenant") as f:
                return f.read().strip()
        except Exception:
            return None

    def store_tenant_label_in_working_directory(self, tenant: str):
        with open(".tenant", "w") as f:
            f.write(tenant)

    def _get_tenant_section(self, tenant: str | None):
        tenant_section = None
        if tenant:
            if tenant in self.config:
                # tenant is the key in a section of the config file
                tenant_section = self.config[tenant]

            elif tenant.isdigit():
                # by tenant ID, in the first section that contains it
                for section in self.config.sections():
                    if (
                        "id" in self.config[section]
                        and self.config[section]["id"] == tenant
                    ):
                        tenant_section = self.config[section]

            if not tenant_section:
                raise NoTenantSectionError(
                    f"There is no tenant `{tenant}` in the file at {self._filename}"
                )

        if not tenant_section and "default" in self.config:
            # default section
            tenant_section = self.config["default"]

        if not tenant_section:
            raise NoTenantSectionError()

        # Treat external credential providers
        if tenant_section.get("api_key").strip('"').startswith("op://"):
            tenant_section['api_key'] = self._resolve_1password_credential(tenant_section.get("api_key"))
            tenant_section['_cred_source'] = "1Password"
            logger.debug(f"Resolved OP credential for tenant `{tenant}`")

        return tenant_section

    def _read_ini_file(self):
        # TODO - warning if the file does not exist
        self.config.read(DEFAULT_INI_FILE)

    def _from_config_file_section(self, tenant: str, key: str) -> str:
        return self.config[tenant][key]

    def _from_env(self, var) -> Optional[str]:
        return environ.get(var)

    def add_tenant(self, key: str, entries: dict):
        self.config[key] = entries
        with open(self._filename, "w") as ini:
            self.config.write(ini)

    def replace_tenant_api_key(self, key: str, api_key: str):
        self.config[key]["api_key"] = api_key
        with open(self._filename, "w") as ini:
            self.config.write(ini)

    def remove_tenant(self, key: str):
        self.config.remove_section(key)
        with open(self._filename, "w") as ini:
            self.config.write(ini)

    @staticmethod
    def resolve_platform(platform):
        if platform == "prod":
            return "api.broadpeak.io"
        if platform == "staging":
            return "apidev.ridgeline.fr"
        return platform

    @staticmethod
    def _resolve_1password_credential(op_path: str):
        # run the op cli to get the credential
        # removing quotes from the credential
        op_path = op_path.strip('"')
        op_credential = subprocess.run(["op", "read", op_path], capture_output=True, text=True)
        credential = op_credential.stdout.strip()

        if not credential:
            raise Exception(f"No credential found in 1Password. If you have multiple accounts, you may need to switch with `op signin` first")

        return credential
    


class InvalidTenantError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class NoTenantSectionError(Exception):
    def __init__(self, message: str = "No valid tenant section could be found in the tenant config file") -> None:
        super().__init__(message)
