import hashlib
import os
import re
from logging import getLogger
from pathlib import Path

import pexpect
import requests

from .defaults import Defaults

log = getLogger(__name__)

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += "HIGH:!DH:!aNULL"  # type: ignore
try:
    requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += (  # type: ignore
        "HIGH:!DH:!aNULL"
    )
except AttributeError:
    # no pyopenssl support used / needed / available
    pass


# todo make ts_type an enum
# todo use Path instead of system
class TsConfig:
    def __init__(
        self,
        ts: str,
        backup_directory: Path,
        username: str | None = None,
        password: str | None = None,
        ts_type: str = "",
    ):
        self.ts = ts
        self.path: Path = backup_directory
        self.desc = f"Terminal server {ts} type {ts_type}"

        log.info(f"backing up {self.desc}")

        self.success = False
        if ts_type.lower() == "moxa":
            self.success = self.get_moxa_config(
                username or "admin", password or "tslinux"
            )
        elif ts_type.lower() == "acs":
            self.success = self.get_acs_config(
                username or "root", password or "tslinux", "/mnt/flash/config.tgz"
            )
        elif ts_type.lower() == "acsold":
            self.success = self.get_acs_config(
                username or "root", password or "tslinux", "/proc/flash/script"
            )
        else:
            log.error(f"unknown type for {self.desc}")

    @staticmethod
    def make_moxa_login(page: str, username: str, password: str):
        match = re.search("(?:fake_challenge|FakeChallenge) value=([^>]*)>", page)
        if match is None:
            raise ValueError("This web page that doesn't look like a moxa login screen")
        fake_challenge = match.groups()[0]

        # do what the function SetPass() javascript does on the login screen
        md = hashlib.md5(fake_challenge.encode("utf8")).hexdigest()
        p = ""
        for c in password:
            p += f"{ord(c):x}"
        md5_pass = ""
        for i in range(len(p)):
            m = int(p[i], 16)
            n = int(md[i], 16)
            md5_pass += "%x" % (m ^ n)

        login_data = {
            "Username": username,
            "MD5Password": md5_pass,
            "Password": "",
            "FakeChallenge": fake_challenge,
        }
        return login_data

    def get_moxa_config(self, username, password):
        url = f"http://{self.ts}"
        # use requests session to get authentication cookie
        session = requests.session()
        response = session.post(url)
        response.raise_for_status()

        login = self.make_moxa_login(response.text, username, password)
        # send the md5 hash and username - populates session cookie 'ChallID'
        session.post(url, data=login, verify=False)

        response = session.get(f"{url}/ConfExp.htm", verify=False)
        m = re.search(r"csrf_token value=([^>]*)>", response.text)
        data = {"csrf_token": m[1]} if m else {}

        response = session.post(f"{url}/Config.txt", data=data, verify=False)

        cfg_path = self.path / (self.ts + "_config.dec")
        with cfg_path.open("wb") as f:
            f.write(response.content)
        return True

    def get_acs_config(self, username, password, remote_path):
        tar = self.path / (self.ts + "_config.tar.gz")
        child = pexpect.spawn(f"scp {username}@{self.ts}:{remote_path} {str(tar)}")
        i = child.expect(
            ["Are you sure you want to continue connecting (yes/no)?", "Password:"],
            timeout=120,
        )
        if i == 0:
            child.sendline("yes")
            child.expect("Password:", timeout=120)
        child.sendline(password)
        i = child.expect([pexpect.EOF, "scp: [^ ]* No such file or directory"])
        try:
            os.chmod(str(tar), 0o664)
        except Exception:
            msg = "Warning: Permissions for ACS Terminal server backup file could not be changed."
            log.critical(msg)
            pass
        if i == 1:
            log.error(f"Remote path {remote_path} doesn't exist on this ACS")
            return False
        else:
            return True


def backup_terminal_server(server: str, ts_type: str, defaults: Defaults):
    desc = f"terminal server {server} type {ts_type}"

    # If backup fails retry specified number of times before giving up
    for attempt_num in range(defaults.retries):
        # noinspection PyBroadException
        try:
            t = TsConfig(server, defaults.ts_folder, None, None, ts_type)
            if t.success:
                log.critical(f"SUCCESS backed up {desc}")
            else:
                log.critical(f"ERROR failed to back up {desc}")
        except Exception:
            msg = f"ERROR: {desc} backup failed on attempt {attempt_num + 1} of {defaults.retries}"
            log.debug(msg, exc_info=True)
            log.error(msg)
            continue
        break
    else:
        msg = f"ERROR: {desc} all {defaults.retries} attempts failed"
        log.critical(msg)
