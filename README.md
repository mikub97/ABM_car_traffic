# ABM_CPMII

Tutorial on mesa <https://towardsdatascience.com/introduction-to-mesa-agent-based-modeling-in-python-bcb0596e1c9a>

<https://www.youtube.com/watch?v=u-XeFNeImyk> \<-- tutorial on MESA (Boltzmann game) and the code from the tutorial --\> <https://github.com/wlifferth/modeling-inequality-with-mesa> <https://github.com/wlifferth/spatially-iterated-prisoners-dilemma>

### Pomysły :

    Small World Model: This model is based on the idea that social networks often exhibit both high clustering (meaning that individuals tend to be connected to others who are also connected to each other) and short path lengths (meaning that it is possible to reach any individual in the network from any other individual with relatively few steps). The model is implemented by starting with a regular lattice of individuals, and then randomly rewiring some of the connections to create shortcuts. This model can be used to study the emergence of social communities and the spread of information through a network.

    Preferential Attachment Model: This model is based on the idea that new connections in a social network are more likely to be formed with individuals who are already highly connected. The model is implemented by starting with a small number of individuals and then adding new individuals one at a time, with each new individual forming connections with existing individuals in proportion to their degree (i.e., the number of connections they already have). This model can be used to study the growth and structure of social networks.

    Network Formation Game Model: This model is based on the idea that individuals in a social network may strategically form connections in order to maximize their own utility. The model is implemented as a game, where each individual chooses which other individuals to form connections with based on a payoff function that takes into account factors such as the benefits of being connected and the costs of maintaining connections. This model can be used to study the formation of social networks in settings where individuals have competing incentives.

    Epidemic Spreading Model on Social Networks: This model is based on the idea that diseases can spread through social networks. The model is implemented by representing individuals as nodes in a network and modeling the transmission of the disease through the edges connecting them. The model can be used to study the impact of different network structures and interventions (such as quarantine or vaccination) on the spread of disease.

    Social Influence Model: This model is based on the idea that individuals in a social network may be influenced by the behavior and opinions of others. The model is implemented by representing individuals as nodes in a network and modeling the spread of influence through the edges connecting them. The model can be used to study the dynamics of opinion formation and the emergence of social norms in a network.

### Possible rules that we could implement in Social influence model

      Influence Threshold: Each agent has an influence threshold, which represents the minimum number of neighbors they need to agree with before changing their own behavior or opinion. For example, an agent might require at least 50% of their neighbors to hold a particular opinion before they adopt that opinion themselves.

      Social Learning: Agents can learn from their neighbors by observing their behavior and opinions. For example, an agent might adopt the same opinion as their most influential neighbor, or they might calculate a weighted average of the opinions of all their neighbors.

      Confirmation Bias: Agents can be biased towards opinions that are consistent with their existing beliefs or values. For example, an agent might be more likely to adopt an opinion that is consistent with their political or religious beliefs, even if it contradicts the opinions of the majority of their neighbors.

      Network Dynamics: Agents can form and break connections with their neighbors over time. For example, an agent might be more likely to form connections with neighbors who hold similar opinions or values, or they might break connections with neighbors who hold opposing opinions or engage in behaviors that they find objectionable.

      Feedback Loops: Agents can influence the opinions and behaviors of their neighbors, which can in turn influence their own behavior and opinions. For example, an agent might adopt a new behavior or opinion after observing it in a few of their neighbors, which could then cause more of their neighbors to adopt the same behavior or opinion in a feedback loop.

### Z myślą o pisaniu raportu zrobię tu notatki:

Agent-based modeling (z wikipedii na easy, wstępne rozeznanie):

-   computational model for simulating the actions and interactions of autonomous agents (both individual or collective entities such as organizations or groups) in order to understand the behavior of a system and what governs its outcomes

<!-- -->

-   explanatory insight \> solving specific engineering problems

<!-- -->

-   individual agents are boundedly (bounded by what they know and their own interests) rational - acting in own interests, they might be able to learn

-   We live in a very complex world where we face complex phenomena such as the formation of social norms and emergence of new disruptive technologies. To better understand such phenomena, social scientists often use a reductionism approach where they reduce complex systems to lower-level variables and model the relationships among them through a scheme of equations such as partial differential equations (PDE). This approach that is called equation-based modeling (EBM) has some basic weaknesses in modeling real complex systems. *EBMs emphasize nonrealistic assumptions, such as unbounded rationality and perfect information, while adaptability, evolvability, and network effects go unaddressed* (LOOK INTO - could be a nice idea to take something that has been modeled with these partial differential equations and propose an ABM model for it? perhaps?)

Social network analysis: SOCIOGRAMS

-   social structures commonly visualized through social network analysis: social media networks, meme spread, information circulation, friendship and acquaintance networks, peer learner networks, business networks, knowledge networks, difficult working relationships, collaboration, kinship, sexual contacts, disease transmission

-   
