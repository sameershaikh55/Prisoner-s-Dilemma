#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np


# ### Base class for agents.
#
# All agents should inherit from this class and implement the **call** method.
#

# In[ ]:


class agent:
    # def Python mein kisi bhi function ko define karne (banane) ka keyword hai
    # __init__ "initialize" ka short form hai. Iske aage aur peeche double underscores (__) hote hain, jo Python ko batate hain ki yeh ek special (magic) method hai
    def __init__(self, name):
        self.name = name

    def name(self):
        return self.name

    # __call__ ka faida yeh hai ke aap apne object ko seedha function ki tarah chala sakte hain. Yani agent() likhne par automatic yeh __call__ wala block chal jayega. Tournament ka engine isi tarah har agent se uska agla move mangta hai
    def __call__(self, agent_history, opponent_history, burn_in=False):
        # NumPy being used
        return np.random.rand() < 0.5


# ### Example agents
#

# In[ ]:


class agentRandom(agent): # Yahan bracket mein (agent) likhne ka matlab hai ke agentRandom ek child class hai aur agent iski parent class hai. Child class parent ke saare functions ko khud-ba-khud inherit kar leti hai
    def __init__(self, name):
        super().__init__(name) # super() ka matlab hota hai "Parent Class". Yahan yeh code keh raha hai ke "Parent class ka __init__ method chalao aur usko yeh name de do". Is wajah se humein is class mein dobara self.name = name nahi likhna pada; parent class khud hi naam set kar degi

    def __call__(self, agent_history, opponent_history, burn_in=False):
        # Random strategy: cooperate with a probability of 0.5
        return np.random.rand() < 0.5


# In[ ]:


class agentCooperate(agent):
    def __init__(self, name):
        super().__init__(name)

    def __call__(self, agent_history, opponent_history, burn_in=False):
        return True  # Always cooperate


# In[ ]:


class agentDefect(agent):
    def __init__(self, name):
        super().__init__(name)

    def __call__(self, agent_history, opponent_history, burn_in=False):
        # Always defect
            return False


# In[ ]:


# Definition: Yeh agent game ko do hisson mein taqseem karta hai: training phase mein fixed pattern
# ke zariye opponent ko poke/test karta hai, aur scored phase mein poori history ki average probability
# nikal kar agar cooperation 75% se zyada ho toh cooperate karta hai, warna safe defect karta hai.
class agentThreshold75(agent):
    def __init__(self, name):
        super().__init__(name)

    def __call__(self, agent_history, opponent_history, burn_in=False):
        current_round = len(agent_history)

        # 1. Edge Case: Pehla round
        if current_round == 0:
            return False  # Default safe play

        # 2. Learning Phase (Pehle 500 rounds unscored hain)
        # Yahan hum jaan-boojh kar ek pattern khelenge taake opponent ka reaction check karein.
        if current_round < 500:
            # Exploration pattern: Har 5 rounds mein 3 dafa Cooperate (True), 2 dafa Defect (False)
            if (current_round % 5) < 3:
                # current_round = 0 -> 0 % 5 = 0 (less then 3) -> Cooperate
                # current_round = 1 -> 1 % 5 = 1 (less then 3) -> Cooperate
                # current_round = 2 -> 2 % 5 = 2 (less then 3) -> Cooperate
                return True
            else:
                # current_round = 3 -> 3 % 5 = 3 (not less than 3) -> Defect
                # current_round = 4 -> 4 % 5 = 4 (not less than 3) -> Defect
                return False

        # 3. Scored Phase (Akhri 25 rounds jahan points count honge)
        else:
            # Inference Engine: Pichle 500 rounds ka data use kar ke probability nikalna
            # cooperations variable opponent_history mein maujood tamaam 'True' (cooperation) moves ko count karna (True = 1, False = 0)
            # Jab hum sum(...) karte hain, toh yeh opponent ke saare True (cooperations) ko ginn leta hai.
            # Agar opponent ne 500 me se 400 dafa cooperate kiya, toh cooperations = 400
            cooperations = sum(opponent_history)

            # Yeh opponent ki Cooperation Probability (p) nikalta hai (Total cooperations / Total rounds).
            # Example: 400/500 = 0.80 (yani 80% aitbaar ka score)
            p_cooperate = cooperations / current_round

            # Decision Action: 75% Threshold Rule
            # Yeh uper waley p_cooperate ko dekh kr check karta hai ke kya samne wale ka cooperate karne ka track record 75% se zyada hai ya nahi
            if p_cooperate > 0.75:
                # Agar opponent ka rate 75% se zyada hai, toh agent samajhta hai ke samne wala dostana (friendly) hai, isliye khud bhi cooperate karta hai taaki dono ko 0 points milein
                return True # Cooperate
            else:
                # Agar rate 75% ya us se kam hai (jaise Random bot ~50% ya Defect bot ~0%), toh agent samajh jata hai ke samne wale par bharosa nahi kiya ja sakta. Wo khud False (Defect) khel kar 5 points ke bhari nuqsaan se bach jata hai
                return False # Defect


# In[ ]:


# Tit-for-Tat (Jaise ko Taisa) ek aisi strategy hai jo hamesha dosti (Cooperate) se shuru hoti hai.
# Uske baad wale har round mein, yeh agent sirf aur sirf opponent ki pichli move ki naqal (copy) karta hai.
# - Agar opponent ne pichle round mein dhoka diya, toh Tit-for-Tat is round mein badla lega (Defect).
# - Agar opponent ne pichle round mein mafi mang li (Cooperate), toh Tit-for-Tat bhi is round mein dosti kar lega (Cooperate).
class agentTitForTat(agent):
    def __init__(self, name):
        super().__init__(name)

    def __call__(self, agent_history, opponent_history, burn_in=False):

        # 1. Edge Case: Pehla round (Hamesha Cooperate / Dosti)
        if len(opponent_history) == 0:
            return True

        # 2. Memory Logic: Opponent ka bilkul aakhri move return kar do
        # Python mein array ke aakhri item ko target karne ke liye [-1] use hota hai
        last_move_of_opponent = opponent_history[-1]

        return last_move_of_opponent


# In[ ]:


# Ek bar Defect mila to hamesha Defect karne wali strategy
class agentGrimTrigger(agent):
    def __init__(self, name):
        super().__init__(name)
        # Yeh ek memory variable hai jo yaad rakhega ke kya opponent ne kabhi dhoka diya hai
        self.betrayed = False

    def __call__(self, agent_history, opponent_history, burn_in=False):

        # 1. Edge Case: Pehla round (Hamesha Cooperate)
        if len(opponent_history) == 0:
            self.betrayed = False  # Naye match par memory reset karna zaroori hai
            return True

        # 2. Memory Check: Kya pichle round mein opponent ne Defect kiya?
        # Agar pichla move False tha (dhoka), toh betrayed ko hamesha ke liye True kar do
        if opponent_history[-1] == False:
            self.betrayed = True

        # 3. Decision Action: The Grim Logic
        # Agar ek dafa bhi dhoka mila hai, toh hamesha Defect karo
        if self.betrayed:
            return False
        # Agar dhoka nahi mila, toh dosti nibhao
        else:
            return True


# In[ ]:


# threshold75 - Version: 1.2 - mera dene k liye
class agentSmartOPM(agent):
    def __init__(self, name):
        super().__init__(name)

    def __call__(self, agent_history, opponent_history, burn_in=False):
        if len(opponent_history) == 0:
            return True

        if opponent_history[-1] == False:
            return False

        return sum(opponent_history) / len(opponent_history) > 0.75


# In[ ]:


class agentSneaky(agent):
    def __init__(self, name="Sneaky_Exploiter"):
        super().__init__(name)

    def __call__(self, agent_history, opponent_history, burn_in=False):
        # Agar yeh 500 rounds wala learning phase hai, toh farishta ban jao (Cooperate)
        if burn_in == True:
            return True
        # Jaise hi points count hona shuru hon, gaddari karo (Defect)
        else:
            return False


# In[ ]:


class agentJester(agent):
    def __init__(self, name="Jester_76"):
        super().__init__(name)

    def __call__(self, agent_history, opponent_history, burn_in=False):
        current_round = len(opponent_history)
        # Har chothe round (round 3, 7, 11, etc) par dhoka do
        if current_round % 4 == 3:
            return False
        else:
            return True


# In[ ]:


class agentUltimateOPM(agent):
    def __init__(self, name="UltimateOPM"):
        super().__init__(name)

    def __call__(self, agent_history, opponent_history, burn_in=False):
        # 1. Pehla round hamesha dosti ka
        if len(opponent_history) == 0:
            return True

        # 2. FAST & FRUGAL DEFENSE (Short-term memory)
        # Agar pichle round mein dushman ne dhoka diya hai, toh calculation chhoro aur foran badla lo!
        # Yeh rule Sneaky aur Jester dono ko tabah kar dega, kyunke inhein lagatar lootne ka mauqa nahi milega.
        if opponent_history[-1] == False:
            return False

        # 3. LONG-TERM CLASSIFIER (Sirf doston aur randoms ke liye)
        cooperations = sum(opponent_history)
        total_rounds = len(opponent_history)

        # Agar opponent ne history mein HAMESHA cooperate kiya hai (TFT, Grim, Coop, ya burn-in wala Sneaky)
        if cooperations == total_rounds:
            return True

        # Agar opponent mixed (Random) khel raha hai
        else:
            p_cooperate = cooperations / total_rounds
            if p_cooperate > 0.75:
                return True
            else:
                return False


# ### Iterated prisoner's dilemma
#
# - Agent input: own history, opponent history
# - Agent return: True (cooperate) or False (defect)
#
# Scoring:
#
# - Both cooperate: 0 point each
# - Both defect: 2 points each
# - One cooperates, one defects: Cooperator: 5, Defector: 1
#   Lowest score wins
#

# In[ ]:


def prisoners_dilemma(agent_1, agent_2, rounds=10, burn_in=0):
    # Scoring system:
    # Both cooperate: Both get 0 point
    bothCooperate = 0
    # One cooperates, one defects: Cooperator gets 5 points, Defector gets 1 points
    oneCooperateOneDefect_Cooperate = 5
    oneCooperateOneDefect_Defect = 1
    # Both defect: Both get 2 point
    bothDefect = 2


    agent_1_history = [] # ki list mein unki pichli saari chaalein (moves) record hongi.
    agent_2_history = []
    agent_1_score = 0
    agent_1_score2 = 0   # squared score for stdv calculation / unke points ka square (murabba) jama karega, jo aakhir mein maths (Standard Deviation) ke kaam aayega
    agent_2_score = 0
    agent_2_score2 = 0   # squared score for stdv calculation / unke points ka square (murabba) jama karega, jo aakhir mein maths (Standard Deviation) ke kaam aayega

    # Burn-in phase: play a few rounds without scoring to establish history
    for _ in range(burn_in):
        agent_1_move = agent_1(agent_1_history, agent_2_history, True)
        agent_2_move = agent_2(agent_2_history, agent_1_history, True)

        agent_1_history.append(agent_1_move)
        agent_2_history.append(agent_2_move)


    # Actual game rounds
    for _ in range(rounds):
        agent_1_move = agent_1(agent_1_history, agent_2_history, False)
        agent_2_move = agent_2(agent_2_history, agent_1_history, False)

        if agent_1_move and agent_2_move:   # both cooperate
            agent_1_score += bothCooperate
            agent_2_score += bothCooperate
            agent_1_score2 += bothCooperate**2
            agent_2_score2 += bothCooperate**2
        elif agent_1_move and not agent_2_move:  # agent 1 cooperates, agent 2 defects
            agent_1_score += oneCooperateOneDefect_Cooperate
            agent_1_score2 += oneCooperateOneDefect_Cooperate**2
            agent_2_score += oneCooperateOneDefect_Defect
            agent_2_score2 += oneCooperateOneDefect_Defect**2
        elif not agent_1_move and agent_2_move:  # agent 1 defects, agent 2 cooperates
            agent_1_score += oneCooperateOneDefect_Defect
            agent_1_score2 += oneCooperateOneDefect_Defect**2
            agent_2_score += oneCooperateOneDefect_Cooperate
            agent_2_score2 += oneCooperateOneDefect_Cooperate**2
        else:  # both defect
            agent_1_score += bothDefect
            agent_2_score += bothDefect
            agent_1_score2 += bothDefect**2
            agent_2_score2 += bothDefect**2

        agent_1_history.append(agent_1_move)
        agent_2_history.append(agent_2_move)

    agent_1_stdv = np.sqrt((agent_1_score2 - agent_1_score**2/rounds)/(rounds-1))
    agent_2_stdv = np.sqrt((agent_2_score2 - agent_2_score**2/rounds)/(rounds-1))

    return agent_1_score/rounds, agent_2_score/rounds, agent_1_stdv, agent_2_stdv


# In[ ]:


def round_robin_tournament(agents, rounds=10, burn_in=0):

        scores = np.zeros(len(agents))   # sum of scores
        stdvs = np.zeros(len(agents))    # sum of standard deviations

        # Randomize playing order of agents
        playing_order = np.arange(len(agents))
        playing_order = np.random.permutation(playing_order)

        # Round-robin tournament with burn-in period where each agent plays against every other agent for a specified number of rounds, but the first few rounds are not counted towards the final score
        for i in range(len(agents)):
            for j in range(i + 1, len(agents)):
                    a1 = agents[playing_order[i]]
                    a2 = agents[playing_order[j]]
                    agent_1_score, agent_2_score, agent_1_stdv, agent_2_stdv = prisoners_dilemma(a1, a2, rounds=rounds, burn_in=burn_in)
                    scores[playing_order[i]] += agent_1_score
                    stdvs[playing_order[i]] += agent_1_stdv
                    scores[playing_order[j]] += agent_2_score
                    stdvs[playing_order[j]] += agent_2_stdv

        # Python mein Arrays ko "Lists" kaha jata hai aur inke methods JS se thore mukhtalif hain
        # Length: JS mein aap opponent_history.length likhte hain. Python mein aap function use karte hain: len(opponent_history)
        scores /= (len(agents) - 1)       # average score per match
        stdv = stdvs / (len(agents) - 1)  # average standard deviation per match
        return scores, stdv


# ### Standard round-robin turnament
#
# - All agents play each-other once
# - Each game consits of 25 iterations of prisoner's dilemma
# - All iterations are scored
#

# In[ ]:


agents = [agentRandom('Random'),
          agentCooperate('Cooperate'),
          agentDefect('Defect'),
          agentThreshold75('Threshold75'),
          agentTitForTat('TitForTat'),
          agentGrimTrigger('GrimTrigger'),
          agentSmartOPM('SmartOPM'),
          agentSneaky('Sneaky'),
          agentJester('Jester'),
          agentUltimateOPM('UltimateOPM')
        ]

scores, stdv = round_robin_tournament(agents, rounds=25, burn_in=0)

# Print the final scores of each agent after the tournament
# enumerate() tracks both the item index (i) and the score value in each iteration
for i, score in enumerate(scores):
    print(f"Agent {agents[i].name} final score:\t\t {score:.1f}, (stdv: {stdv[i]:.1f})")


# ### Round-robin turnament with burn-in phase
#
# - All agents play each-other once
# - Each game starts with 500 unscored iterations of prisoner's dilemma, followed by 25 scored iterations
#

# In[ ]:


agents = [agentRandom('Random'),
          agentCooperate('Cooperate'),
          agentDefect('Defect'),
          agentThreshold75('Threshold75'),
          agentTitForTat('TitForTat'),
          agentGrimTrigger('GrimTrigger'),
          agentSmartOPM('SmartOPM'),
          agentSneaky('Sneaky'),
          agentJester('Jester'),
          agentUltimateOPM('UltimateOPM')
        ]

scores, stdv = round_robin_tournament(agents, rounds=25, burn_in=500)

# Print the final scores of each agent after the tournament
for i, score in enumerate(scores):
    print(f"Agent {agents[i].name} final score:\t\t {score:.1f}, (stdv: {stdv[i]:.1f})")


# In[ ]:


def compare_agents(agents, trials=50, rounds=25, burn_in=500, seed=2026):
    """Compare every agent over repeated, reproducible round-robin tournaments.

    Lower scores are better for the payoff rules used in this notebook.
    """
    if len(agents) < 2:
        raise ValueError("At least two agents are required.")
    if trials < 2:
        raise ValueError("Use at least two trials to estimate variability.")
    if rounds < 2:
        raise ValueError("Use at least two scored rounds for standard deviation.")
    if burn_in < 0:
        raise ValueError("burn_in cannot be negative.")

    names = [agent.name for agent in agents]
    if len(names) != len(set(names)):
        raise ValueError("Agent names must be unique so results remain unambiguous.")

    score_runs = np.zeros((trials, len(agents)))
    stdv_runs = np.zeros((trials, len(agents)))

    for trial in range(trials):
        np.random.seed(seed + trial)
        score_runs[trial], stdv_runs[trial] = round_robin_tournament(
            agents, rounds=rounds, burn_in=burn_in
        )

    mean_scores = score_runs.mean(axis=0)
    trial_std = score_runs.std(axis=0, ddof=1)
    standard_error = trial_std / np.sqrt(trials)
    confidence_low = mean_scores - 1.96 * standard_error
    confidence_high = mean_scores + 1.96 * standard_error
    mean_round_stdv = stdv_runs.mean(axis=0)
    ranking = np.argsort(mean_scores)

    print(f"Evaluation: {len(agents)} agents, {trials} trials, "
          f"{rounds} scored rounds, {burn_in} burn-in rounds")
    print("Lower mean score is better. 95% CI describes uncertainty across trials.\n")
    print(f"{'Rank':<6}{'Agent':<18}{'Mean':>10}{'Trial SD':>12}"
          f"{'95% CI':>22}{'Mean round SD':>17}")
    print("-" * 85)
    for rank, index in enumerate(ranking, start=1):
        print(f"{rank:<6}{names[index]:<18}{mean_scores[index]:>10.3f}"
              f"{trial_std[index]:>12.3f}"
              f"{confidence_low[index]:>9.3f} to {confidence_high[index]:<9.3f}"
              f"{mean_round_stdv[index]:>17.3f}")

    return {
        "names": names,
        "score_runs": score_runs,
        "stdv_runs": stdv_runs,
        "mean_scores": mean_scores,
        "trial_std": trial_std,
        "confidence_low": confidence_low,
        "confidence_high": confidence_high,
        "mean_round_stdv": mean_round_stdv,
        "ranking": ranking,
    }


def matchup_report(agents, rounds=25, burn_in=500, seed=2026):
    """Show one reproducible scored result for every unique agent pair."""
    if len(agents) < 2:
        raise ValueError("At least two agents are required.")

    print(f"{'Match':<4}{'Agent 1':<18}{'Agent 2':<18}"
          f"{'Score 1':>10}{'Score 2':>10}")
    print("-" * 60)
    match_number = 0
    for first in range(len(agents)):
        for second in range(first + 1, len(agents)):
            np.random.seed(seed + match_number)
            score_1, score_2, stdv_1, stdv_2 = prisoners_dilemma(
                agents[first], agents[second], rounds=rounds, burn_in=burn_in
            )
            print(f"{match_number + 1:<4}{agents[first].name:<18}"
                  f"{agents[second].name:<18}{score_1:>10.3f}{score_2:>10.3f}")
            match_number += 1


comparison = compare_agents(agents, trials=50, rounds=25, burn_in=500, seed=2026)
print("\nOne reproducible matchup snapshot:")
matchup_report(agents, rounds=25, burn_in=500, seed=2026)


# ## Reusable agent comparison standard
#
# This section is the reliable evaluation layer for every current and future agent.
#
# ### How to add another agent
#
# 1. Define the new class with the same `__call__(agent_history, opponent_history, burn_in=False)` interface.
# 2. Add one uniquely named instance to the existing `agents` list.
# 3. Run the comparison cell below the list. Do not change the evaluator.
#
# ### What the evaluation measures
#
# - **Mean:** average tournament score over repeated trials. Lower is better for this payoff system.
# - **Trial SD:** how much the agent's tournament score changes between trials. Lower means more stable.
# - **95% CI:** uncertainty around the estimated mean. Narrower intervals mean a more precise estimate.
# - **Mean round SD:** average within-match variation in round scores.
# - **Matchup snapshot:** one deterministic, inspectable example for every unique pair. It is useful for diagnosis, but the repeated-trial ranking is the primary comparison.
#
# ### Reproducibility and fairness
#
# Each trial uses a known seed, every agent faces every other agent once per tournament, and all agents use the same number of scored rounds and burn-in rounds. The evaluator ranks by mean score, not by one lucky or unlucky random run.
#
# For a final report, record the agent list, `trials`, `rounds`, `burn_in`, and `seed` together with the printed ranking. If a new strategy uses randomness, increase `trials` before drawing conclusions.
