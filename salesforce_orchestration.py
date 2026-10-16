
import subprocess
import sys
from pathlib import Path

from prefect import flow, task


PROJECT_DIR = Path(__file__).resolve().parent


@task
def run_dlt():
    result = subprocess.run(
        [sys.executable, "salesforce_pipeline.py"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        check=True,
    )

    print(result.stdout)

@task
def run_dbt_staging():
    result = subprocess.run(
        ["dbt", "run", "--select", "staging"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        check=True,
    )

    print(result.stdout)


@task
def run_dbt_marts():
    result = subprocess.run(
        ["dbt", "run", "--select", "marts"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        check=True,
    )

    print(result.stdout)




@task
def run_dbt_tests():
    result = subprocess.run(
        ["dbt", "test"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )

    print(result.stdout, flush=True)

    if result.returncode != 0:
        raise RuntimeError(
            f"dbt tests failed with exit code {result.returncode}."
        )




@flow
def salesforce_pipeline_flow():
    run_dlt()
    run_dbt_staging()
    run_dbt_marts()
    run_dbt_tests()

if __name__ == "__main__":
    salesforce_pipeline_flow()
    
