import pytest

from imerit_ango.models.enums import OrganizationRoles, ProjectRoles
from imerit_ango.models.invite import Invitation, RoleUpdate
from imerit_ango.sdk import SDK

API_KEY = "a2199a36-1f36-4650-bc73-5c7bf48b735c"
HOST = "https://testapi.ango.ai"
ORG = "65a54e51b9639d6570d3f27c"
PROJECT = "65b0d1dfa17e9516ff1c2035"
USER = "faruk@imerit.net"
TASK = "65b0dbb2a17e9516ff1c20ed"
@pytest.fixture
def sdk_instance():
    return SDK(api_key=API_KEY, host=HOST)

def test_list_projects_and_get_project(sdk_instance):
    response = sdk_instance.list_projects()
    assert isinstance(response, dict)
    assert 'projects' in response.get("data", {})

    project_id = response.get("data").get("projects")[0].get("_id")
    project_response = sdk_instance.get_project(project_id)
    assert 'name' in project_response.get("data").get("project")

def test_task_related_funcs(sdk_instance):
    response = sdk_instance.get_tasks(PROJECT)
    assert isinstance(response, dict)
    assert 'tasks' in response.get("data")

    task_id = response.get("data").get("tasks")[0].get("_id")
    sdk_instance.assign_task(PROJECT, [task_id], email=USER)

    task_response = sdk_instance.get_task(task_id)
    assert 'task' in task_response.get("data")
    assert task_response.get("data").get("task").get("assignee") == USER

    issue_response = sdk_instance.create_issue(task_id, "issue here", [30, 30])
    assert issue_response.get("data").get("issue").get("status") == "Open"

def test_get_assets(sdk_instance):
    response = sdk_instance.get_assets(PROJECT)
    assert isinstance(response, dict)
    assert 'assets' in response.get("data")

def test_create_attachment(sdk_instance):
    response = sdk_instance.create_attachment(PROJECT, [
      {
        "data": "https://asset.url/image-sample.jpg",
        "externalId": "image-sample.jpg",
        "attachments": [
          {
            "type": "IMAGE",
            "value": "https://sample-image.jpg"
          },
          {
            "type": "VIDEO",
            "value": "http://sample-video.mp4"
          },
          {
            "type": "TEXT",
            "value": "Some sample text"
          }
        ]
      }
    ])
    assert isinstance(response, dict)
    assert 'project' in response.get("data")


def test_get_organization_members(sdk_instance):
    response = sdk_instance.get_organization_members(ORG)
    assert isinstance(response, dict)
    assert 'users' in response.get("data")