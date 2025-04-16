from collections import namedtuple
from enum import Enum
from itertools import zip_longest

Condition = Enum("Condition", ("CURE", "HEALTHY", "SICK", "DYING", "DEAD"))
Agent = namedtuple("Agent", ("name", "category"))

def improve(agent: Agent) -> Agent:
    """Improve the condition of an agent by one level.

    The improvement is done according to the following rules:
`   - CURE -> CURE
    - SICK -> HEALTHY
    - DYING -> SICK

    Parameters
    ----------
    Agent : Agent
        The agent to improve.

    Returns
    -------
    Agent
        The improved agent.
    """
    if agent.category == Condition.SICK:
        return agent._replace(category=Condition.HEALTHY)
    elif agent.category == Condition.DYING:
        return agent._replace(category=Condition.SICK)
    else:
        return agent

def worsen(agent: Agent) -> Agent:
    """Worsen the condition of an agent by one level.

    The worsening is done according to the following rules:
    - SICK -> DYING
    - DYING -> DEAD


    Parameters
    ----------
    agent : Agent
        The agent to worsen.

    Returns
    -------
    Agent
        The worsened agent.
    """
    if agent.category == Condition.SICK:
        return agent._replace(category=Condition.DYING)
    elif agent.category == Condition.DYING:
        return agent._replace(category=Condition.DEAD)
    else:
        return agent
    
def meeting_result(agent1: Agent, agent2: Agent):
    """Determine the outcome of a meeting between two agents.

    The outcome is determined by the following rules:
    - If one agent is CURE, the other agent improves one level (e.g from 'DYING' to 'SICK').
    - If one agent is DYING  or SICK,the other agent's condition worsens by one level (e.g 'SICK' becomes 'DYING').
    - If both agents are SICK, they both become DYING.
    - If both agents are CURE, their condition remains the same.
    - If an agent is HEALTHY or DEAD they will now show up for the meeting

    Parameters
    ----------
    a : Agent
        The first agent in the meeting.
    b : Agent
        The second agent in the meeting.

    Returns
    -------
    Agent objects of the two agents (name and category) after participating in the meeting
    """
    agent1_after = agent1
    agent2_after = agent2
    # If agent1 is a CURE, they improve the other agent's condition.
    if agent1.category == Condition.CURE:
        agent2_after = improve(agent2)
    # If agent1 is DYING or SICK, they worsen the other agent's condition.
    elif agent1.category in (Condition.DYING, Condition.SICK):
        agent2_after = worsen(agent2) 
    # Now for agent 2:
    if agent2.category == Condition.CURE:
        agent1_after = improve(agent1)
    elif agent2.category in (Condition.DYING, Condition.SICK):
        agent1_after = worsen(agent1)
    
    return agent1_after, agent2_after

def meetup(agent_listing: tuple) -> list:
    """Model the outcome of the meetings of pairs of agents.

    The pairs of agents are ((a[0], a[1]), (a[2], a[3]), ...). If there's an uneven
    number of agents, the last agent will remain the same.

    Notes
    -----
    The rules governing the meetings were described in the question. The outgoing
    listing may change its internal ordering relative to the incoming one.

    Parameters
    ----------
    agent_listing : tuple of Agent
        A listing (tuple in this case) in which each element is of the Agent
        type, containing a 'name' field and a 'category' field, with 'category' being
        of the type Condition.

    Returns
    -------
    updated_listing : list
        A list of Agents with their 'category' field changed according to the result
        of the meeting.
    """
    # 1. Filter HEALTHY and DEAD agents out
    # 2. Pair agents up
    # 3. Apply the meeting_result function to each pair and add the result to a new list.
    # 4. Add the filtered out agents to the new list.
    # 5. Return the new list.

    active_agents = [agent for agent in agent_listing if agent.category not in (Condition.HEALTHY, Condition.DEAD)]

    updated_listing = []

    it = iter(active_agents)
    for agent1, agent2 in zip_longest(it, it):
        # Handle uneven number of agents:
        if agent2:
            agent1, agent2 = meeting_result(agent1, agent2)
            updated_listing.extend([agent1, agent2])
        else:
            updated_listing.append(agent1)
    
    # Add the filtered out agents to the new list.
    updated_listing.extend(agent for agent in agent_listing if agent.category in (Condition.HEALTHY, Condition.DEAD))
    return updated_listing


if __name__ == "__main__":
    data1 = (
        Agent("Agent1", Condition.CURE),
        Agent("Agent2", Condition.CURE),
        Agent("Agent3", Condition.SICK),
        Agent("Agent4", Condition.SICK),
        Agent("Agent5", Condition.DYING),
        Agent("Agent6", Condition.DYING),
    )
    data2 = (
        Agent("Zelda0", Condition.CURE),
        Agent("Zelda1", Condition.CURE),
        Agent("Zelda2", Condition.SICK),
        Agent("Zelda3", Condition.SICK),
        Agent("Zelda4", Condition.DYING),
        Agent("Zelda5", Condition.DYING),
        Agent("Zelda6", Condition.SICK),
    )

    results = meetup(data1)
    print("Results for data1:")
    for agent in results:
        print(f"{agent.name}: {agent.category}")

    results = meetup(data2)
    print("\nResults for data2:")
    for agent in results:
        print(f"{agent.name}: {agent.category}")