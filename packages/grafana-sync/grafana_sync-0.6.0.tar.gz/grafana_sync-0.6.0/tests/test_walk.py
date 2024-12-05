from typing import TYPE_CHECKING

import pytest

from grafana_sync.api.models import (
    DashboardData,
    GetFoldersResponse,
    SearchDashboardsResponse,
)

from .utils import docker_grafana_client

if TYPE_CHECKING:
    from grafana_sync.api.client import GrafanaClient

pytestmark = pytest.mark.docker


@pytest.fixture(scope="session")
def grafana(docker_ip, docker_services):
    return docker_grafana_client(docker_ip, docker_services)


def _to_dicts(items: GetFoldersResponse | SearchDashboardsResponse):
    """Remove id fields from folder items and convert to dict for comparison."""
    return [
        {
            k: v
            for k, v in item.model_dump().items()
            if k in ["uid", "title", "folderUid", "parentUid"] and v is not None
        }
        for item in items.root
    ]


def test_walk_single_folder(grafana: "GrafanaClient"):
    grafana.create_folder(title="dummy", uid="dummy", parent_uid=None)

    try:
        lst = list(grafana.walk("general", True, True))
        lst = [
            (folder_uid, _to_dicts(folders), _to_dicts(dashboards))
            for folder_uid, folders, dashboards in lst
        ]
        assert lst == [
            ("general", [{"uid": "dummy", "title": "dummy"}], []),
            ("dummy", [], []),
        ]
    finally:
        grafana.delete_folder("dummy")


def test_walk_recursive_folders(grafana: "GrafanaClient"):
    grafana.create_folder(title="l1", uid="l1", parent_uid=None)
    grafana.create_folder(title="l2", uid="l2", parent_uid="l1")

    try:
        lst = list(grafana.walk("general", True, True))
        lst = [
            (folder_uid, _to_dicts(folders), _to_dicts(dashboards))
            for folder_uid, folders, dashboards in lst
        ]
        assert lst == [
            ("general", [{"uid": "l1", "title": "l1"}], []),
            ("l1", [{"uid": "l2", "title": "l2", "parentUid": "l1"}], []),
            ("l2", [], []),
        ]
    finally:
        grafana.delete_folder("l1")


def test_walk_recursive_with_dashboards(grafana: "GrafanaClient"):
    """Test walking folders recursively with dashboards at different levels."""
    # Create test structure:
    # l1/
    #   dashboard1
    #   l2/
    #     dashboard2

    # Create folders
    grafana.create_folder(title="l1", uid="l1", parent_uid=None)
    grafana.create_folder(title="l2", uid="l2", parent_uid="l1")

    # Create dashboards
    dashboard1 = DashboardData(uid="dash1", title="Dashboard 1")
    dashboard2 = DashboardData(uid="dash2", title="Dashboard 2")

    grafana.update_dashboard(dashboard1, "l1")
    grafana.update_dashboard(dashboard2, "l2")

    try:
        lst = list(grafana.walk("general", True, True))
        lst = [
            (folder_uid, _to_dicts(folders), _to_dicts(dashboards))
            for folder_uid, folders, dashboards in lst
        ]
        assert lst == [
            ("general", [{"uid": "l1", "title": "l1"}], []),
            (
                "l1",
                [{"uid": "l2", "title": "l2", "parentUid": "l1"}],
                [
                    {
                        "uid": "dash1",
                        "title": "Dashboard 1",
                        "folderUid": "l1",
                    }
                ],
            ),
            (
                "l2",
                [],
                [
                    {
                        "uid": "dash2",
                        "title": "Dashboard 2",
                        "folderUid": "l2",
                    }
                ],
            ),
        ]
    finally:
        # Clean up
        grafana.delete_dashboard("dash1")
        grafana.delete_dashboard("dash2")
        grafana.delete_folder("l1")  # This will cascade delete l2


def test_list_command(grafana: "GrafanaClient"):
    """Test that list command runs without errors."""
    from click.testing import CliRunner

    from grafana_sync.cli import cli

    grafana.create_folder(title="test", uid="test", parent_uid=None)

    try:
        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "--url",
                grafana.url,
                "--username",
                "admin",
                "--password",
                "admin",
                "list",
                "--recursive",
                "--include-dashboards",
            ],
        )
        assert result.exit_code == 0
    finally:
        grafana.delete_folder("test")
