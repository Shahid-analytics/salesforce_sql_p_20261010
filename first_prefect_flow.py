
from prefect import flow, task, get_run_logger
# attempts = 0


# # @task
# # # (retries=2, retry_delay_seconds=5)
# # def say_goodbye():
# #     # global attempts
# #     # attempts += 1

# #     # print(f"Attempt number: {attempts}")

# #     # if attempts == 1:
# #     #     raise ValueError("Simulated temporary failure")

# #     print("Goodbye from my second Prefect task!")
    


# # @task
# # def say_hello():
# #     print("Hello from my first Prefect task!")


# # @flow
# # def my_first_flow():
# #     say_hello()
# #     say_goodbye()


# # if __name__ == "__main__":
# #     my_first_flow()


# @task(retries=2, retry_delay_seconds=3)
# def get_number():
#     global attempts
#     attempts += 1

#     print(f"Task 1 attempt: {attempts}")

#     if attempts == 1:
#         raise ValueError("Simulated temporary failure")

#     print("Task 1: Producing a number")
#     return 10

# @task
# def multiply_number(number):
#     result = number * 2
#     print(f"Task 2: {number} x 2 = {result}")
#     return result


# @flow
# def my_first_flow(input_number: int = 10):
#     # value = get_number()
#     final_result = multiply_number(input_number)
#     print(f"Final result: {final_result}")


# if __name__ == "__main__":
#     my_first_flow.serve(name="manual-practice")



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
