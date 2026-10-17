
from prefect import flow, task, get_run_logger


@task(retries=2, retry_delay_seconds=5)
def controlled_failure():
    logger = get_run_logger()

    # Fail deliberately on every attempt
    logger.info("Running controlled retry test.")
    raise ValueError("Intentional test failure to verify Prefect retries.")


@flow(name="Controlled Retry Test")
def retry_test_flow():
    controlled_failure()


if __name__ == "__main__":
    retry_test_flow()
