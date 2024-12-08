from gh_hooks_utils.payloads import InstallationEvent

from .data.installation.payloads import install_event_all_repos


def test_installation_event_should_accept_all_repositories_selection():
    event = InstallationEvent(**install_event_all_repos)

    assert event is not None
    assert len(event.repositories) > 0
