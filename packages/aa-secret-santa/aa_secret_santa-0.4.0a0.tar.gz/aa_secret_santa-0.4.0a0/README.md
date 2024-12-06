# AA Secret Santa

A Secret Santa Manager for [Alliance Auth](https://gitlab.com/allianceauth/allianceauth)

## Features

- Accepts Applications to be secret santas
- Handles randomly pairing up users
- Notifies users of their santee
- handles if gifts have been delivered
- [Secure Groups Integration](https://github.com/Solar-Helix-Independent-Transport/allianceauth-secure-groups)

## Installation

### Step 1 - Install app

```shell
pip install aa-secret-santa
```

### Step 2 - Configure Auth settings

Configure your Auth settings (`local.py`) as follows:

- Add `'secretsanta'` to `INSTALLED_APPS`

### Step 4 - Maintain Alliance Auth

- Run migrations `python manage.py migrate`
- Gather your staticfiles `python manage.py collectstatic`
- Restart your project `supervisorctl restart myauth:`

### Step 5 - Configuration

In the Admin interface, visit `secretsanta` or `<AUTH-URL>/admin/secretsanta` # Coming Soon

## Permissions

| Perm | Admin Site  | Perm | Description |
| --- | --- | --- | --- |
| basic_access | nill | Can access Secret Santa | Can access the Secret Santa Module and Apply to Years |
| manager | nill | Can manage Secret Santa | Can Manage and See all Santa<>Santee Pairs |

## Settings

| Name | Description | Default |
| --- | --- | --- |
| `SECRETSANTA_GENERATE_PAIRS_PRIORITY`| the generate_pairs task, to run super uber omega immediately so we can identify issues | 1 |
| `SECRETSANTA_NOTIFY_PRIORITY`| Priority for discord messages for secret santa | 5 |

## Contributing

Make sure you have signed the [License Agreement](https://developers.eveonline.com/resource/license-agreement) by logging in at <https://developers.eveonline.com> before submitting any pull requests. All bug fixes or features must not include extra superfluous formatting changes.
