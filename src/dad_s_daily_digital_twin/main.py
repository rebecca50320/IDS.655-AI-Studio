#!/usr/bin/env python
import sys
from dad_s_daily_digital_twin.crew import DadSDailyDigitalTwinCrew
from generate_email import run_crew_and_extract_email

# This main file is intended to be a way for your to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'dad_name': 'sample_value',
        'your_name': 'sample_value',
        'dad_email': 'sample_value'
    }
    DadSDailyDigitalTwinCrew().crew().kickoff(inputs=inputs)
    run_crew_and_extract_email()


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'dad_name': 'sample_value',
        'your_name': 'sample_value',
        'dad_email': 'sample_value'
    }
    try:
        DadSDailyDigitalTwinCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        DadSDailyDigitalTwinCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'dad_name': 'sample_value',
        'your_name': 'sample_value',
        'dad_email': 'sample_value'
    }
    try:
        DadSDailyDigitalTwinCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: main.py <command> [<args>]")
        sys.exit(1)

    command = sys.argv[1]
    if command == "run":
        run()
    elif command == "train":
        train()
    elif command == "replay":
        replay()
    elif command == "test":
        test()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
