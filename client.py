"""
Least Commitment Partial Order Planner Skill Client
Pure Python Standard Library implementation of Partial-Order Causal Link (POCL) Planning (McAllester & Rosenblitt UCPOP style).
Maintains open preconditions, causal links S_i --p--> S_j, and resolves causal threats
via ordering constraints (promotion and demotion) without premature step ordering.
"""

from typing import List, Dict, Any, Tuple, Optional, Set


class PartialOrderPlanner:
    """
    POCL planner: avoids committing to step order unless forced by a causal threat.
    Plan = (Steps, Orderings, CausalLinks)
    """

    def __init__(self):
        self.steps: Set[str] = set()
        self.orderings: Set[Tuple[str, str]] = set()  # (A, B) means A must occur before B
        self.causal_links: List[Tuple[str, str, str]] = []  # (S_i, p, S_j) means S_i produces p for S_j

    def add_step(self, step_name: str):
        """Add action step to partial plan."""
        self.steps.add(step_name)

    def add_ordering(self, before: str, after: str):
        """Constrain 'before' to occur prior to 'after'."""
        self.steps.add(before)
        self.steps.add(after)
        self.orderings.add((before, after))

    def add_causal_link(self, producer: str, condition: str, consumer: str):
        """Record causal dependency: producer establishes condition for consumer."""
        self.steps.add(producer)
        self.steps.add(consumer)
        self.orderings.add((producer, consumer))
        self.causal_links.append((producer, condition, consumer))

    def resolve_threat(self, threat_step: str, producer: str, condition: str, consumer: str, resolution: str = "promotion") -> bool:
        """
        Resolve threat where threat_step deletes condition protected by causal link.
        - Promotion: threat_step occurs AFTER consumer -> (consumer < threat_step)
        - Demotion:  threat_step occurs BEFORE producer -> (threat_step < producer)
        """
        if resolution == "promotion":
            self.add_ordering(consumer, threat_step)
            return True
        elif resolution == "demotion":
            self.add_ordering(threat_step, producer)
            return True
        return False

    def topological_sort(self) -> Optional[List[str]]:
        """
        Produce valid linear sequence consistent with all partial orderings.
        Returns None if cycle detected (ordering conflict).
        """
        nodes = list(self.steps)
        in_degree = {n: 0 for n in nodes}
        adj = {n: set() for n in nodes}

        for u, v in self.orderings:
            if v not in adj[u]:
                adj[u].add(v)
                in_degree[v] += 1

        queue = [n for n in nodes if in_degree[n] == 0]
        result = []

        while queue:
            curr = queue.pop(0)
            result.append(curr)
            for neighbor in adj[curr]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(result) == len(nodes):
            return result
        return None  # Cycle detected
