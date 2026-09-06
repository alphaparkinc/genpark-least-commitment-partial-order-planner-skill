"""
Example usage of Least Commitment Partial Order Planner Skill.
"""

from client import PartialOrderPlanner


def main():
    print("=== Least Commitment Partial Order Planner (POCL) Demonstration ===")
    pocl = PartialOrderPlanner()

    # Define steps for getting dressed: Left Shoe, Right Shoe, Left Sock, Right Sock
    # Causal links:
    #   Left Sock --has_left_sock--> Left Shoe
    #   Right Sock --has_right_sock--> Right Shoe
    # (Left and right branches can execute in parallel or any interleaved order!)
    pocl.add_causal_link("PutOnLeftSock", "LeftSockOn", "PutOnLeftShoe")
    pocl.add_causal_link("PutOnRightSock", "RightSockOn", "PutOnRightShoe")

    print(f"Total Steps: {len(pocl.steps)}")
    print(f"Causal Links: {pocl.causal_links}")
    print(f"Partial Orderings: {pocl.orderings}")

    # Solve linear linearization
    linear_plan = pocl.topological_sort()
    print("\nValid Linearized Execution Sequence:")
    for idx, step in enumerate(linear_plan, 1):
        print(f"  Step {idx}: {step}")


if __name__ == "__main__":
    main()
