"""
MCP Server for Least Commitment Partial Order Planner Skill.
"""

import json
import sys
from client import PartialOrderPlanner

POCL = PartialOrderPlanner()


def handle_request(req: dict) -> dict:
    method = req.get("method")
    params = req.get("params", {})

    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "add_causal_link",
                    "description": "Establish causal link S_i --p--> S_j and enforce ordering",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "producer": {"type": "string"},
                            "condition": {"type": "string"},
                            "consumer": {"type": "string"}
                        },
                        "required": ["producer", "condition", "consumer"]
                    }
                },
                {
                    "name": "linearize_plan",
                    "description": "Generate valid linear execution order from partial plan",
                    "inputSchema": {
                        "type": "object"
                    }
                }
            ]
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "add_causal_link":
            POCL.add_causal_link(args["producer"], args["condition"], args["consumer"])
            return {"content": [{"type": "text", "text": json.dumps({"status": "causal_link_added"})}]}

        elif tool_name == "linearize_plan":
            res = POCL.topological_sort()
            return {"content": [{"type": "text", "text": json.dumps({"linear_sequence": res})}]}

        return {"error": f"Unknown tool: {tool_name}"}

    return {"error": f"Unknown method: {method}"}


def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            resp["id"] = req.get("id")
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"error": str(e)}) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
