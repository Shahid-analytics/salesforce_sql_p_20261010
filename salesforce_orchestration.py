
import os
import subprocess
import sys
import traceback
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


@flow(name="salesforce-pipeline-flow")
def salesforce_pipeline_flow():
    logger = get_run_logger()

    try:
        run_dlt()
        run_dbt_staging()
        run_dbt_tests()
        run_dbt_marts()

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
    
