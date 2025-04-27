import time
from crewai import Crew, Process  # type: ignore
from agents import researcher, writer, proof_reader
from crew_tasks import research_task, write_task, proof_read_task
import litellm # type: ignore
from litellm.exceptions import RateLimitError # type: ignore

# Function to handle retry logic with backoff
def retry_with_backoff(func, max_retries=5, backoff_factor=2):
    attempt = 0
    while attempt < max_retries:
        try:
            return func()  # Try executing the function
        except RateLimitError as e:
            attempt += 1
            wait_time = backoff_factor ** attempt  # Exponential backoff
            print(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)  # Wait before retrying
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            break  # Exit on other errors
    print("Max retries reached, operation failed.")
    return None  # Return None or handle as needed

# Initialize Crew
crew = Crew(
    agents=[researcher, writer, proof_reader],
    tasks=[research_task, write_task, proof_read_task],
    process=Process.sequential
)

# Task execution function
def execute_task():
    topic = "Artificial Intelligence in Finance"
    result = crew.kickoff(inputs={"topic": topic})
    return result

# Retry with backoff
result = retry_with_backoff(execute_task)

if result:
    print("Task completed successfully!")
else:
    print("Task failed after retries.")
