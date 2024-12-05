# Mobicontrol CLI

The Mobicontrol CLI is a wrapper around the Mobicontrol API, to make deployment of apps easier.

## Prerequisites

1. You should already have credentials for the Mobicontrol API. If you don't have it, reach out to Warehouse & Site Logistics
2. Python version > 3.11
3. Optional: jq is a JSON parser, that is useful to parse and filter the JSON responses.

## Installation

To install the latest version, run `pip install mobicontrol`.

## Usage

### Auth

First time you run the CLI, you need to login:

```bash
mc login --url <mobicontrol_base_url> --client_id <client_id> --client_secret <client_secret> --username <username> --password <password>
```

The base URL for the LEGO instance is: https://s115517.mobicontrolcloud.com

The session status is stored in ~/.mobicontrol/store.json

### Upload an app

To upload an app you will need the .apk file.

```
mc app upload --file <path_to_apk>.apk
```

Take note of the "ReferenceId" in the response JSON.

### Create a profile

To create a profile, run a the following command:

```bash
mc policy create --name "Manual Test" --kind ManagedGooglePlay --description "Manual test profile from MC API"
```

If a policy with the same name already exists, the payload for the existing profile is returned.

### Assign the app to the profile

Using the policy and app ReferenceId, assign the app to the policy:

```bash
mc policy app create --id <policy_reference_id>  --app <app_reference_id>
```

There is an additional flag `--config`, that can be used to pass a Managed App Config to the app. It must be a valid JSON string.

### Assign the profile to a device group

mc profile assign

Finally assign the new profile to a device group:

```bash
mc policy assignment create --id <policy_reference_id> --group <device_group_path>
```

Device groups are formatted like a path with backslashes. If you don't know where to deploy, reach out to Warehousing & Site Logistics.

NOTE: It is necessary to escape backslashes in your request. E.g. `\\LEGO\Development` must be enteres as `\\\\LEGO\\Development`.
