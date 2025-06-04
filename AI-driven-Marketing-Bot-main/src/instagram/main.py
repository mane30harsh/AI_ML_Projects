#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
import os
from instagram.crew import InstagramCrew
from litellm import completion
import yaml

config_path = r"C:\Users\nimis\Desktop\project2\instagram\src\instagram\config\config.yaml"

try:
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
        print("Config loaded successfully:", config)
except FileNotFoundError:
    print(f"Config file not found at {config_path}")

model_name = config.get("model", "gpt-4")  # Default to gpt-4 if not found

os.environ["OPENAI_API_KEY"] = "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"
os.environ["LITELLM_PROVIDER"] = "openai"

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

from datetime import datetime
import os

def run(topic, description):
    """
    Run the crew and save the generated content to multiple markdown files.
    """
    inputs = {
        'topic': topic,
        'current_year': str(datetime.now().year),
        'current_date': datetime.now().strftime("%Y-%m-%d"),
        'instagram_description': description,
        'topic_of_the_week': topic,
    }

    try:
        # Generate market research, content strategy, and visual content
        market_research_content = InstagramCrew().crew().kickoff(inputs={**inputs, "content_type": "market_research"})
        final_content_strategy = InstagramCrew().crew().kickoff(inputs={**inputs, "content_type": "final_content_strategy"})
        visual_content = InstagramCrew().crew().kickoff(inputs={**inputs, "content_type": "visual_content"})

        # Save the results to different markdown files
        market_research_path = f"market-research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        final_content_strategy_path = f"final-content-strategy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        visual_content_path = f"visual-content_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

        with open(market_research_path, "w") as file:
            file.write(market_research_content)
        with open(final_content_strategy_path, "w") as file:
            file.write(final_content_strategy)
        with open(visual_content_path, "w") as file:
            file.write(visual_content)

        # Return file paths
        return [market_research_path, final_content_strategy_path, visual_content_path]

    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")



def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year),
        "current_date": datetime.now().strftime("%Y-%m-%d"),
        "instagram_description": "Create engaging Instagram content about AI language models that educates and entertains the audience while highlighting the latest developments in the field.",
        "topic_of_the_week": "AI LLMs and their impact on content creation"
    }
    try:
        InstagramCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        InstagramCrew().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year),
        "current_date": datetime.now().strftime("%Y-%m-%d"),
        "instagram_description": "Create engaging Instagram content about AI language models that educates and entertains the audience while highlighting the latest developments in the field.",
        "topic_of_the_week": "AI LLMs and their impact on content creation"
    }
    try:
        InstagramCrew().crew().test(
            n_iterations=int(sys.argv[1]), 
            openai_model_name="gpt-4",
            inputs=inputs
        )
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
