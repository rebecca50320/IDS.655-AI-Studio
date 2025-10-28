#!/usr/bin/env python
import sys
import os
from social_media_emotional_bias_detector.crew import SocialMediaEmotionalBiasDetectorCrew

# This main file is intended to be a way for your to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information
current_file_path = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_file_path, '..', '..'))
scraper_root = os.path.join(project_root, 'Reddit_Scrapper')

for path in (project_root, scraper_root):
    if path not in sys.path:
        sys.path.insert(0, path)

from Reddit_Scrapper.run_test import scrape_first_post
_, post_context = scrape_first_post()




def run():
    """
    Run the crew.
    """
    inputs = {
        'social_media_content': post_context
    }
    SocialMediaEmotionalBiasDetectorCrew().crew().kickoff(inputs=inputs)
    

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'social_media_content': post_context
    }
    try:
        SocialMediaEmotionalBiasDetectorCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        SocialMediaEmotionalBiasDetectorCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'social_media_content': post_context
    }
    try:
        SocialMediaEmotionalBiasDetectorCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

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
