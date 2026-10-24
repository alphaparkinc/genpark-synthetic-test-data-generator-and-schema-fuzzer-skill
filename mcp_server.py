"""MCP server for Synthetic Test Data Generator and Schema Fuzzer."""
import sys
import json
from client import SyntheticDataFuzzer


def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "generate_mock_record",
                    "description": "Generates realistic mock data records matching JSON schema properties",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "schema_properties": {"type": "object"},
                            "seed": {"type": "integer"},
                        },
                        "required": ["schema_properties"],
                    },
                },
                {
                    "name": "fuzz_record",
                    "description": "Generates boundary fuzzing edge-case records to test validation robustness",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "schema_properties": {"type": "object"},
                            "target_fuzz_field": {"type": "string"},
                            "seed": {"type": "integer"},
                        },
                        "required": ["schema_properties"],
                    },
                },
            ]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "generate_mock_record":
            res = SyntheticDataFuzzer.generate_record(
                schema_properties=args.get("schema_properties", {}),
                seed=args.get("seed"),
            )
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
        elif tool_name == "fuzz_record":
            res = SyntheticDataFuzzer.fuzz_record(
                schema_properties=args.get("schema_properties", {}),
                target_fuzz_field=args.get("target_fuzz_field"),
                seed=args.get("seed"),
            )
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
    return {"error": "Method not found"}


if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_request(json.loads(line))))
            sys.stdout.flush()
