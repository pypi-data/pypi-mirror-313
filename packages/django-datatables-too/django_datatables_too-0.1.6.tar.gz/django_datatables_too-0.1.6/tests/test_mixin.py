from http import HTTPStatus

import pytest
from django.contrib.auth.models import Permission
from django.urls import reverse

from .factories import UserFactory

pytestmark = pytest.mark.django_db


def flatten_dict(data, prefix=""):
    result = {}
    for key, value in data.items():
        new_key = f"{prefix}[{key}]" if prefix else key
        if isinstance(value, dict):
            result.update(flatten_dict(value, new_key))
        else:
            result[new_key] = value
    return result


def test_ajax_pagination_view(client):
    # Create test data
    user1 = UserFactory(username="User A")
    user2 = UserFactory(username="User B")

    # Create a user with the necessary permissions
    user = UserFactory()
    view_permission = Permission.objects.get(
        content_type__app_label="auth", codename="view_user"
    )
    user.user_permissions.add(view_permission)
    client.force_login(user)

    # Simulate a GET request to the CompanyAjaxPagination view
    url = reverse("ajax-pagination")
    data = {
        "draw": "1",
        "columns": {
            "0": {
                "data": "username",
                "name": "username",
                "searchable": "true",
                "orderable": "true",
                "search": {"value": "", "regex": "false"},
            },
            "1": {
                "data": "first_name",
                "name": "first_name",
                "searchable": "true",
                "orderable": "true",
                "search": {"value": "", "regex": "false"},
            },
            "2": {
                "data": "last_name",
                "name": "last_name",
                "searchable": "true",
                "orderable": "true",
                "search": {"value": "", "regex": "false"},
            },
        },
        "order": {"0": {"column": "0", "dir": "asc"}},
        "start": "0",
        "length": "25",
        "search": {"value": "User", "regex": "false"},
        "_": "1733504855924",
    }
    response = client.get(url, flatten_dict(data))
    assert response.status_code == HTTPStatus.OK

    # Verify the response data
    response_data = response.json()
    assert response_data["recordsTotal"] == 3  # noqa: PLR2004
    assert response_data["recordsFiltered"] == 2  # noqa: PLR2004
    # print(response_data)
    assert len(response_data["data"]) == 2  # noqa: PLR2004

    # Verify the content of the response data
    user_names = [user["username"] for user in response_data["data"]]
    assert user1.username in user_names
    assert user2.username in user_names
