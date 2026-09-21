# Iterated Prisoner's Dilemma - Custom AI Agent

This repository contains a custom AI agent designed to compete in a round-robin tournament of the Iterated Prisoner's Dilemma.

## Project Overview
The Prisoner's Dilemma is a classic game theory problem. In this iterated version, agents play multiple rounds against each other. The goal isn't just to beat the opponent in a single round, but to achieve the **lowest possible overall score** across the entire tournament.

### Modified Scoring Rules (Lowest Score Wins!):
* **Both Cooperate (True, True):** 0 points each
* **Both Defect (False, False):** 2 points each
* **One Cooperates, One Defects:** Cooperator gets 5 points, Defector gets 1 point

## My Agent's Strategy: Random
The agent now uses a purely random strategy, disregarding the tournament's phases or any historical data.

* For every round, whether it's during the learning (burn-in) phase or the scoring phase, it makes its decision by generating a random number.
* It chooses to cooperate with a 50% probability and defect with a 50% probability.
* It does not track or react to the opponent's previous moves.

## Tech Stack & Setup
* **Language:** Python 3.11
* **Environment:** Jupyter Notebook / VS Code
* **Dependencies:** `numpy`

To test the agent, you can run the `prisonersDilemma.ipynb` notebook which contains the base `agent` class and the tournament simulation engine.