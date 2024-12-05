from mobicontrol.client import MobicontrolClient
from typing import Optional
import re


def get_policies(
    client: MobicontrolClient,
    name_contains: Optional[str] = None,
    families: Optional[str] = None,
    statuses: Optional[str] = None,
    is_scheduled: Optional[bool] = None,
    order: Optional[str] = None,
    skip: Optional[int] = None,
    take: Optional[int] = None,
) -> list:
    response = client.get(
        "/appManagement/policies",
        params={
            "nameContains": name_contains,
            "families": families,
            "statuses": statuses,
            "isScheduled": is_scheduled,
            "order": order,
            "skip": skip,
            "take": take,
            "source": "",
        },
    )

    if response.status_code != 200:
        raise Exception(
            f"Could not fetch policies. Error code: {response.status_code}. {response.text}"
        )

    return response.json()


def get_policy(
    client: MobicontrolClient,
    policy_id: str,
):
    response = client.get(f"/appManagement/android/policies/{policy_id}")

    if response.status_code != 200:
        raise Exception(
            f"Could not delete policy. Error code: {response.status_code}. {response.text}"
        )

    return response.json()


def create_policy(
    client: MobicontrolClient,
    name: str,
    kind: str,
    description: str = "",
) -> dict:
    response = client.post(
        "/appManagement/android/policies",
        json={
            "Name": name,
            "Description": description,
            "RuleKind": kind,
        },
    )

    if response.status_code != 200:
        raise Exception(
            f"Could not create policy. Error code: {response.status_code}. {response.text}"
        )

    return response.json()


def delete_policy(client: MobicontrolClient, policy_id: str):
    response = client.delete(f"/appManagement/android/policies/{policy_id}")

    if response.status_code != 204:
        raise Exception(
            f"Could not delete policy. Error code: {response.status_code}. {response.text}"
        )


def get_apps(client: MobicontrolClient, policy_id: str) -> list:
    response = client.get(
        f"/appManagement/android/policies/{policy_id}/apps/enterprise"
    )

    if response.status_code != 200:
        raise Exception(
            f"Could not fetch apps. Error code: {response.status_code}. {response.text}"
        )

    return response.json()


def set_apps(client: MobicontrolClient, policy_id: str, apps: list):
    response = client.put(
        f"/appManagement/android/policies/{policy_id}/apps/enterprise",
        json=apps,
    )

    if response.status_code != 204:
        data = response.json()

        if "ErrorCode" in data:
            raise Exception(f"Upload failed with message: {data['Message']}")

        raise Exception(
            f"Upload failed with status code {response.status_code}. {response.text}."
        )


def add_app(
    client: MobicontrolClient, policy_id: str, app_id: str, config: Optional[str] = ""
):
    apps = get_apps(client, policy_id)

    payload = []

    for app in apps:
        app_payload = {
            "ReferenceId": app["ReferenceId"],
            "IsMandatory": app["IsMandatory"],
            "AppPriority": app["AppPriority"],
            "AppConfiguration": app["AppConfiguration"],
        }

        if app["ReferenceId"] == app_id:
            app_payload["AppConfiguration"] = config

        payload.append(app_payload)

    if app_id not in [app["ReferenceId"] for app in apps]:
        payload.append(
            {
                "ReferenceId": app_id,
                "IsMandatory": True,
                "AppPriority": 1,
                "AppConfiguration": config,
            }
        )

    set_apps(client, policy_id, payload)


def remove_app(client: MobicontrolClient, policy_id: str, app_id: str):
    apps = get_apps(client, policy_id)

    payload = []
    for app in apps:
        if app["ReferenceId"] != app_id:
            payload.append(
                {
                    "ReferenceId": app["ReferenceId"],
                    "IsMandatory": app["IsMandatory"],
                    "AppPriority": app["AppPriority"],
                    "AppConfiguration": app["AppConfiguration"],
                }
            )

    set_apps(client, policy_id, payload)


def get_assignments(client: MobicontrolClient, policy_id: str) -> dict:
    response = client.get(f"/appManagement/policies/{policy_id}/assignment")

    if response.status_code != 200:
        raise Exception(f"Error code: {response.status_code}. {response.text}")

    data = response.json()

    if data is None:
        return {"TargetDeviceGroups": []}

    return data


def set_assignments(
    client: MobicontrolClient, policy_id: str, device_groups: list[str]
):

    groups_payload = [
        {
            "DeviceGroupPath": group,
            "Excluded": False,
        }
        for group in device_groups
    ]

    payload = {
        "TargetDeviceGroups": groups_payload,
    }

    response = client.put(
        f"/appManagement/policies/{policy_id}/assignment",
        json=payload,
    )

    if response.status_code != 200:
        raise Exception(f"Error code: {response.status_code}. {response.text}")

    return response.json()


def assign_device_group(client, policy_id: str, device_group: str):
    assignments = get_assignments(client, policy_id)

    group_ids = [
        assignment["DeviceGroupPath"]
        for assignment in assignments["TargetDeviceGroups"]
    ]

    if device_group in group_ids:
        return

    group_ids.append(device_group)

    set_assignments(client, policy_id, group_ids)


def unassign_device_group(client: MobicontrolClient, policy_id: str, device_group: str):
    assignments = get_assignments(client, policy_id)

    group_ids = [
        assignment["DeviceGroupPath"]
        for assignment in assignments["TargetDeviceGroups"]
    ]

    if device_group not in group_ids:
        return

    group_ids.remove(device_group)

    set_assignments(client, policy_id, group_ids)
