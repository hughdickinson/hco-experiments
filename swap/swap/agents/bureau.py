################################################################
# Keeps track of all user and subject agents
# - Initial class to test SWAP

from swap.agents.agent import Agent


class Bureau(object):
    """ Bureau to keep track of agents

    Parameter:
    ----------
        agent_type: str
            Informative string to indicate agent types in that specific bureau
    """

    def __init__(self, agent_type):
        # type of agents, just a string? (e.g. users, subjects, machines,...)
        # maybe not required because we could look at the agents' subclass

        # What if we pass the type of the agents here... as in Bureau(Subject)
        # or Bureau(User) etc. ?
        self.agent_type = agent_type
        # dictionary to store all agents, key is agent-ID
        self._agents = dict()

    @property
    def agents(self):
        return self._agents.copy()

    def addAgent(self, agent):
        """
            Add agent to bureau

            Parameter:
            ----------
                agent: agent object
        """
        # Verify agent is of proper type
        if not isinstance(agent, self.agent_type):
            raise TypeError(
                'Agent type %s is not of type %s' %
                (type(agent), self.agent_type))

        # Add agent to collection
        if agent.id not in self._agents:
            self._agents[agent.id] = agent
        else:
            raise KeyError("Agent-ID already in bureau, remove first")

    def add(self, agent):
        self.addAgent(agent)

    def getAgent(self, agent_id):
        """ Get agent from bureau

        Parameter:
        ----------
            agent_id: id of agent

        Returns:
        -------
            agent
        """
        if agent_id in self._agents:
            return self._agents[agent_id]
        else:
            raise KeyError("Error: Agent_id not in Bureau")

    def get(self, agent_id):
        return self.getAgent(agent_id)

    def removeAgent(self, agent_id):
        """ Remove agent from bureau

        Parameter:
        ----------
            agent_id: id of agent
        """
        del self._agents[agent_id]

    def has(self, agent_id):
        """ Check if agent is in bureau

        Parameter:
        ----------
            agent_id: id of agent

        Returns:
        --------
            boolean
        """
        return agent_id in self._agents

    # ----------------------------------------------------------------

    def getAgentIds(self):
        return set(self.agents.keys())

    def stats(self):
        """
            Calculates the mean, standard deviation, and median
            of scores in this bureau
        """
        return self.agent_type.stats(self)

    def export(self):
        data = dict()
        for name, agent in self.agents.items():
            data[name] = agent.export()
        return data

    def iter_ids(self, ids):
        return AgentIterator(self, ids)

    def __iter__(self):
        return iter(self.agents.values())

    def __contains__(self, item):
        if isinstance(item, Agent):
            id_ = item.id
        else:
            id_ = item

        return self.has(id_)

    def __str__(self):
        return '\n'.join([str(item) for item in self._agents.values()])


class AgentIterator:
    """
        Custom iterator to iterate through agents in a bureau
        according to a list of ids
    """

    def __init__(self, bureau, ids):
        self.bureau = bureau
        self.ids = ids
        self.index = 0

    def next(self):
        index = self.index
        if index >= len(self):
            raise StopIteration
        else:
            agent = self.bureau.get(self.ids[index])
            self.index += 1
            return agent

    def __iter__(self):
        return self

    def __len__(self):
        return len(self.ids)

    def __next__(self):
        return self.next()
