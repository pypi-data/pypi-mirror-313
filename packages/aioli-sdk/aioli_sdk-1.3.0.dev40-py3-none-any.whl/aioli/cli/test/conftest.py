# © Copyright 2024 Hewlett Packard Enterprise Development LP
import subprocess
import time

import pexpect
import pytest


@pytest.fixture(scope="session")
def setup_login(request: pytest.FixtureRequest) -> None:
    print("\nDoing setup")
    shell_cmd = "aioli user login admin"
    child = pexpect.spawn("/bin/bash", ["-c", shell_cmd])
    fout = open("/tmp/login-log.txt", "wb")
    child.logfile = fout
    child.expect("Password for user 'admin':")
    child.sendline("")
    time.sleep(1)
    if child.isalive():
        child.close()

    def fin() -> None:
        print("\nDoing teardown")
        subprocess.check_output(["aioli", "user", "logout"], shell=False)
        time.sleep(1)

    request.addfinalizer(fin)
