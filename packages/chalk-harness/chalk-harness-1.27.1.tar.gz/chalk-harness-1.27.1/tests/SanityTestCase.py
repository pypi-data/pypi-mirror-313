from chalkharness.chalkharness import ChalkCLIHarness


h = ChalkCLIHarness(dry=True)


def test_apply():
    assert ["chalk", "apply", "--json", "--await", "--force"] == h.apply_await(True)


def test_version():
    assert ["chalk", "version", "--json"] == h.version()
    assert ["chalk", "version", "--json", "--tag-only"] == h.version_tag_only()


def test_whoami():
    assert ["chalk", "whoami", "--json"] == h.whoami()


def test_token():
    assert ["chalk", "token", "--json"] == h.token()


def test_environments():
    assert ["chalk", "environment", "--json"] == h.environments()
    assert ["chalk", "environment", "dev", "--json"] == h.set_environment("dev")


def test_project():
    assert ["chalk", "project", "--json"] == h.project()


def test_config():
    assert ["chalk", "config", "--json"] == h.config()


def test_dashboard():
    assert ["chalk", "dashboard", "--json"] == h.dashboard()


def test_init():
    assert ["chalk", "init", "--json", "--template=fraud"] == h.init(template="fraud")
