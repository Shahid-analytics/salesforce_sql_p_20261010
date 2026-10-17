
import os
import subprocess
import sys
import traceback
import msal
import requests
from pathlib import Path

from prefect import flow, task, get_run_logger
from prefect.runtime import flow_run

from email_notifications import send_failure_email


PROJECT_DIR = Path(__file__).resolve().parent

def run_command(command):
    logger = get_run_logger()

    logger.info("Starting command: %s", " ".join(command))

    with subprocess.Popen(
        command,
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    ) as process:

        for line in process.stdout:
            logger.info(line.rstrip())

        return_code = process.wait()

    if return_code != 0:
        raise RuntimeError(
            f"Command failed with exit code {return_code}: "
            f"{' '.join(command)}"
        )

    logger.info("Command completed successfully.")


@task
def run_dlt():
    run_command([
    sys.executable,
    "salesforce_pipeline.py",
    ])

@task
def run_dbt_staging():
    run_command([
    "dbt",
    "run",
    "--select",
    "staging",
    ])



@task
def run_dbt_marts():
    run_command([
    "dbt",
    "run",
    "--select",
    "marts",
    ])




@task
def run_dbt_tests():
    run_command([
    "dbt",
    "test",
    ])



@task
def run_powerbi_refresh():
    logger = get_run_logger()

    # Read credentials from .env
    tenant_id = os.getenv("POWERBI_TENANT_ID")
    client_id = os.getenv("POWERBI_CLIENT_ID")
    client_secret = os.getenv("POWERBI_CLIENT_SECRET")

    if not all([tenant_id, client_id, client_secret]):
        raise ValueError(
            "Missing Power BI credentials. Check the .env file."
        )

    # Power BI workspace and semantic model IDs
    workspace_id = "65f68826-e1c2-477e-9abc-2abefee0c5dd"
    dataset_id = "291aff46-560d-4350-9ad3-8928264a7846"

    logger.info("Authenticating with Microsoft Entra...")

    app = msal.ConfidentialClientApplication(
        client_id=client_id,
        authority=f"https://login.microsoftonline.com/{tenant_id}",
        client_credential=client_secret,
    )

    token_result = app.acquire_token_for_client(
        scopes=[
            "https://analysis.windows.net/powerbi/api/.default"
        ]
    )

    if "access_token" not in token_result:
        raise RuntimeError(
            "Power BI authentication failed: "
            + token_result.get(
                "error_description", "Unknown authentication error"
            )
        )

    logger.info("Authentication successful.")

    # Request the semantic model refresh
    url = (
        "https://api.powerbi.com/v1.0/myorg/groups/"
        f"{workspace_id}/datasets/{dataset_id}/refreshes"
    )

    response = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {token_result['access_token']}",
            "Content-Type": "application/json",
        },
        json={"notifyOption": "NoNotification"},
        timeout=30,
    )

    if response.status_code != 202:
        raise RuntimeError(
            f"Power BI refresh request failed: "
            f"HTTP {response.status_code} - {response.text}"
        )

    logger.info(
        "Power BI accepted the semantic model refresh request."
    )


@flow(name="salesforce-pipeline-flow")
def salesforce_pipeline_flow():
    logger = get_run_logger()

    try:
        run_dlt()
        run_dbt_staging()
        run_dbt_tests()
        run_dbt_marts()
        run_powerbi_refresh()

    except Exception as exc:
        logger.exception("Salesforce pipeline failed.")

        try:
            ui_url = os.getenv(
                "PREFECT_UI_URL",
                "http://127.0.0.1:4200",
            )
            run_id = flow_run.id

            subject = "[Prefect ALERT] Salesforce pipeline failed"

            body = f"""
The Salesforce pipeline has failed.

Flow: salesforce-pipeline-flow
Run ID: {run_id}
Error: {type(exc).__name__}: {exc}

Open Prefect and inspect this flow run:
{ui_url}/runs/flow-run/{run_id}

The detailed task logs are available in the Prefect UI.
"""

            send_failure_email(subject, body)
            logger.info("Failure notification email sent.")

        except Exception:
            logger.exception(
                "Could not send failure notification email."
            )

        raise

if __name__ == "__main__":
    salesforce_pipeline_flow()
    
