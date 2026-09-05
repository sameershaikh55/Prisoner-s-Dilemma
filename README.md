# Iterated Prisoner's Dilemma - Custom AI Agent

This repository contains a custom AI agent designed to compete in a round-robin tournament of the Iterated Prisoner's Dilemma.

## Project Overview
The Prisoner's Dilemma is a classic game theory problem. In this iterated version, agents play multiple rounds against each other. The goal isn't just to beat the opponent in a single round, but to achieve the **lowest possible overall score** across the entire tournament.

### Modified Scoring Rules (Lowest Score Wins!):
* **Both Cooperate (True, True):** 0 points each
* **Both Defect (False, False):** 2 points each
* **One Cooperates, One Defects:** Cooperator gets 5 points, Defector gets 1 point

## My Agent's Strategy: "Explore & Exploit"
This agent is built to handle the tournament's two distinct phases:

1. **The Learning Phase (Burn-in):** 
   The first 500 rounds are unscored. Instead of playing randomly, my agent uses this phase to "probe" the opponent. It plays a set pattern (3 Cooperations followed by 2 Defections) to observe exactly how the opponent reacts to both loyalty and betrayal.
   
2. **The Scoring Phase:** 
   In the final 25 scored rounds, the agent stops testing and analyzes the data collected. It calculates the opponent's probability of cooperating ($p$). Using expected utility math, the agent only cooperates if the opponent's probability of cooperation is strictly greater than **75%**. Otherwise, it defaults to defection to protect itself from receiving the 5-point penalty.

## Tech Stack & Setup
* **Language:** Python 3.11
* **Environment:** Jupyter Notebook / VS Code
* **Dependencies:** `numpy`

To test the agent, you can run the `prisonersDilemma.ipynb` notebook which contains the base `agent` class and the tournament simulation engine.