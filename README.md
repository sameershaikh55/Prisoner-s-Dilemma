# Iterated Prisoner's Dilemma - Custom AI Agent

This repository contains a custom AI agent designed to compete in a round-robin tournament of the Iterated Prisoner's Dilemma.

## Project Overview
The Prisoner's Dilemma is a classic game theory problem. In this iterated version, agents play multiple rounds against each other. The goal isn't just to beat the opponent in a single round, but to achieve the **lowest possible overall score** across the entire tournament.

### Modified Scoring Rules (Lowest Score Wins!):
* **Both Cooperate (True, True):** 0 points each
* **Both Defect (False, False):** 2 points each
* **One Cooperates, One Defects:** Cooperator gets 5 points, Defector gets 1 point

## My Agent's Strategy: "Ultimate OPM"
My agent (`agentUltimateOPM`) uses a hybrid strategy that combines short-term defense with long-term classification:

1. **First Round:** Always starts by cooperating.
2. **Fast & Frugal Defense (Short-term memory):** If the opponent defected in the very last round, the agent immediately defects. This prevents continuous exploitation by sneaky or unpredictable opponents.
3. **Long-Term Classifier:** If the opponent cooperated in the last round, the agent looks at the opponent's entire history:
   * If the opponent has *always* cooperated, the agent cooperates.
   * If the opponent's history is mixed, the agent calculates their historical probability of cooperating ($p$). The agent will only cooperate if this probability is strictly greater than **75%**. Otherwise, it defects to protect itself.

## Tech Stack & Setup
* **Language:** Python 3.11
* **Environment:** Jupyter Notebook / VS Code
* **Dependencies:** `numpy`

To test the agent, you can run the `prisonersDilemma.ipynb` notebook which contains the base `agent` class and the tournament simulation engine.