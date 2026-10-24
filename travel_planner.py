"""
travel_planner.py
My first CrewAI agent: the user types a city, and a Travel Planner agent
suggests exactly 3 places to visit there.

The API key is read from the environment (or a local .env file).
It is never hard-coded in this file.

By default only the final 3 places are printed. Set SHOW_LOGS=true in .env
to see the agent's full verbose log.
"""

import os
import sys

from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM

# Load variables from a local .env file (if present) into the environment.
load_dotenv()

SHOW_LOGS = os.getenv("SHOW_LOGS", "false").strip().lower() == "true"


def check_api_key() -> None:
    """Stop early with a clear message if the API key is missing."""
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY is not set.")
        print("Create a .env file (see .env.example) or set the variable in your terminal.")
        sys.exit(1)


def ask_for_city() -> str:
    """Ask the user for a city until they type something."""
    while True:
        city = input("Enter a city you want to visit: ").strip()
        if city:
            return city
        print("Please type a city name.")


def build_crew() -> Crew:
    """Create the agent, the task, and assemble them into a crew."""

    llm = LLM(
        model=os.getenv("MODEL", "gpt-4o-mini"),
        temperature=0.7,
    )

    # 1. The Agent: who it is, what it wants, and where it comes from.
    travel_planner = Agent(
        role="Travel Planner",
        goal=(
            "Recommend the three most worthwhile places for a first-time "
            "visitor to see in {city}, with a short reason for each."
        ),
        backstory=(
            "You are a seasoned travel planner who has spent fifteen years "
            "designing trips for curious travellers around the world. "
            "You know the difference between tourist traps and places that "
            "truly capture the character of a city, and you always explain "
            "your picks in plain, friendly language."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

    # 2. The Task: exactly what the agent must produce.
    suggest_places = Task(
        description=(
            "The traveller is planning a visit to {city}. "
            "Suggest exactly 3 well-known tourist places to visit in {city}. "
            "Choose a mix where possible (for example a landmark, a cultural "
            "or historical spot, and a nature or food experience). "
            "Only include real places that are actually in or near {city}. "
            "Do not suggest offices, IT parks, colleges, hotels or private businesses."
        ),
        expected_output=(
            "A numbered list of exactly 3 places in this format:\n"
            "1. <Place name> - <one sentence on what it is>. "
            "Why visit: <one sentence on why it is worth the trip>.\n"
            "2. ...\n"
            "3. ...\n"
            "No introduction or closing text, just the 3 numbered items."
        ),
        agent=travel_planner,
    )

    # 3. The Crew: puts the agent and the task together.
    return Crew(
        agents=[travel_planner],
        tasks=[suggest_places],
        process=Process.sequential,
        verbose=SHOW_LOGS,
    )


def main() -> None:
    check_api_key()
    city = ask_for_city()
    crew = build_crew()

    real_stdout = sys.stdout
    if not SHOW_LOGS:
        print("Planning your trip, please wait...\n")
        # Send CrewAI's console panels to nowhere. It stays redirected after
        # the run so the exit-time "Tracing Status" panel is hidden too.
        sys.stdout = open(os.devnull, "w", encoding="utf-8")

    try:
        # 4. Run it. The {city} placeholders above are filled in from inputs.
        result = crew.kickoff(inputs={"city": city})
    except Exception:
        sys.stdout = real_stdout  # make sure errors are visible
        raise

    print(f"Top 3 places to visit in {city}", file=real_stdout)
    print("=" * 50, file=real_stdout)
    print(result.raw, file=real_stdout)
    real_stdout.flush()


if __name__ == "__main__":
    main()