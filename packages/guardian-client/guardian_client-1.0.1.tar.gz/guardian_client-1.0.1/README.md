# Protect AI Guardian Client

A CLI and SDK client for Protect AI's Guardian service. You can find more information about this service here: https://protectai.com/guardian

# Using CLI

The Guardian Scanner's CLI offers a convenient way of submitting a scan and receiving the scan report along with an exit code that can be used to block model deployment depending upon the discovered vulnerabilities.

## Installation

``` shell
pip install guardian-client
```

## Setup Environment Variables

These environment variables are required for setting up the authorization with the API. The admin of your account should be able to provide you with these. 

``` shell

# Guardian endpoint, can also be passed as a CLI option
export GUARDIAN_ENDPOINT=

# Client ID
export GUARDIAN_SCANNER_CLIENT_ID=
  
# Client Secret
export GUARDIAN_SCANNER_CLIENT_SECRET=
```

## Running Your Scans

That's it! Now you should be all set to start scanning your models.

``` shell

guardian-client scan <model_uri> \
       [--base-url <base-url>] \
       [--block-on-errors] \
       [--report-only] \
       [--log-level <log-level>] \
       [--poll-interval-secs <n_secs>] \
       [--silent] || echo $?
```

## Retrieving Your Scans

``` shell
guardian-client get-scan <scan_id> \
       [--base-url <base-url>] \
       [--block-on-errors] \
       [--report-only] \
       [--log-level <log-level>] \
       [--silent] || echo $?
```

### Arguments

- `--base-url` The API URL if not set as environment variable (required)

- `model_uri` The Path where the model is stored e.g. S3 bucket (required)

- `--block-on-errors` A boolean flag indicating the error in scanning should also lead to a block. These errors are only specific to model scanning.

- `--log-level` Can be set to any of the following: error, info, or debug

- `--silent` Disable all logging / reporting

- `--report-only` Print out the scan report and skip evaluating it for blocking.

- `--poll-interval-secs` The interval in seconds to wait before polling the server for scan status. Default is 5.

### Exit Codes
The CLI returns following exit codes that can be used by the downstream applications to block a deployment.

- **0** Successful scan without violating any of your organization's policies

- **1** Successful scan with issues violating your organization's policies

- **2** Scan failed for any reason

## Examples

### To get a block decision for a model in S3

``` shell
guardian-client scan s3://a-bucket/path/ || echo $?
```
### To only see the report from scanning the model.

```
guardian-client scan s3://a-bucket/path/ --report-only

```

### To retrieve a historical scan

```
guardian-client get-scan c4fb7d8c-fc8c-422e-814c-c4441982e726 --report-only
```

# Using the Python SDK

In addition to the CLI, you can also integrate the scanner within your python application. The installation and environment setup is same as CLI when using the SDK. 

Example for submitting a scan:

``` python
# Import the Guardian API client
from guardian_client import GuardianAPIClient

# Define the location of the Guardian Scanner's API and your model
base_url = "<ADD_YOUR_SERVICE_URL>"
model_uri = "<ADD_YOUR_MODEL_URL>"

# Initiate the client
guardian = GuardianAPIClient(base_url=base_url)

# Scan the model
response = guardian.scan(model_uri=model_uri)


# Retrieve the pass/fail decision from Guardian
assert response.get("http_status_code") == 200
assert response.get("scan_status_json") != None
assert response.get("scan_status_json").get("aggregate_eval_outcome") != "ERROR"
  
if response.get("scan_status_json").get("aggregate_eval_outcome") == "FAIL":
  print(f"Model {model_uri} was blocked because it failed your organization's security policies")
```

Example for retrieving a previous scan's results:

```python
# Import the Guardian API client
from guardian_client import GuardianAPIClient

# Define the location of the Guardian Scanner's API
base_url = "<ADD_YOUR_SERVICE_URL>"

# Initiate the client
guardian = GuardianAPIClient(base_url=base_url)

# Get a historical scan
retrieved = guardian.get_scan(scan_uuid="c4fb7d8c-fc8c-422e-814c-c4441982e726")

print(retrieved.get("scan_status_json"))
```

## Reference

### Class GuardianAPIClient

``` python
def __init__(
    self,
    base_url: str,
    scan_endpoint: str = "scans",
    api_version: str = "v1",
    log_level: str = "INFO",
) -> None:
    """
    Initializes the Guardian API client.

    Args:
        base_url (str): The base URL of the Guardian API.
        scan_endpoint (str, optional): The endpoint for scanning. Defaults to "scans".
        api_version (str, optional): The API version. Defaults to "v1".
        log_level (str, optional): The log level. Defaults to "INFO".

    Raises:
        ValueError: If the log level is not one of "DEBUG", "INFO", "ERROR", or "CRITICAL".

    """
```

#### Methods

#### GuardianAPIClient.scan
``` python
def scan(self, model_uri: str, poll_interval_secs: int = 5) -> Dict[str, Any]:
    """
    Submits a scan request for the given URI and polls for the scan status until it is completed.

    Args:
        uri (str): The URI to be scanned.
        poll_interval_secs (int, optional): The interval in seconds to poll for the scan status.
            If <= 0, the function returns immediately after submitting the scan. Defaults to 5.

    Returns:
        dict: A dictionary containing the HTTP status code and the scan status JSON.
                If an error occurs during the scan submission or polling, the dictionary
                will also contain the error details.
    """
```

#### GuardianAPIClient.get_scan
```python
def get_scan(self, scan_uuid: str) -> Dict[str, Any]:
    """
    Retrieves the scan results for a given past scan.

    Args:
        scan_uuid (str): The ID of the scan to retrieve.

    Returns:
        dict: A dictionary containing the HTTP status code and the scan status JSON.
                If an error occurred during the scan, the dictionary
                will contain the error details instead of the scan status.
    """
```
