# iam_actions

`iam_actions` is a python module which contains a dictionary of AWS IAM information. Ideally, it is a complete catalog of all AWS services, actions, and resource types. The information is scraped from the AWS documentation pages.

Nightly, the scraping service runs, and publishes a new version with the date appended. 

The package is meant to be used as a consumable package, but it also contains the code to generate the definitions for packaging.

There are three "roots" that you can consume: actions, resource_types, and services. They all currently return as dict's. *However, in a future release, it will be returned as python data structures*

## Actions

Actions is a listing of all the actions for a given service. The structure is as follows:
```
{
    "service_name": {
        "action_name: {
            "access_level": access_level,
            "action": action_name,
            "condition_keys": [condition_key1, ...],
            "description": description
        }
    }
}
```

Therefore, you can find information about an action as follows

```
>>> iam_actions.actions['s3']['GetObject']
{'access_level': 'Read', 'action': 'GetObject', 'condition_keys': ['s3:AccessPointNetworkOrigin', 's3:DataAccessPointAccount', 's3:DataAccessPointArn', 's3:ExistingObjectTag/<key>', 's3:ResourceAccount', 's3:TlsVersion', 's3:authType', 's3:signatureAge', 's3:signatureversion', 's3:x-amz-content-sha256'], 'description': 'Grants permission to retrieve objects from Amazon S3', 'orphan': False, 'resources': ['object']}
```

## Services

Services list information about the service. The structure is as follows:

```
{
    "service_name": {
        "Actions": [action1, ...]
        "ServiceNames": [service_name1, ...]
        "ARNFormats": [arn_format1, ...]
        "ConditionKeys": [condition_key1, ...]
        "HasResource": bool
    }
}
```

## Resource Types

Resource Types list information about the resource types for the service. The structure is as follows:

```
{
    "service_name": {
        "resource_name": {
            "arn_pattern": arn_pattern,
            "condition_keys": [condition_key1, ...]
        }
    }
}
```

## Usage

```python
import iam_actions

print(item_actions.services)
print(item_actions.actions)
print(item_actions.resource_types)
```
