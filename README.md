# genpark-synthetic-test-data-generator-and-schema-fuzzer-skill

Deterministic mock data synthesizer, JSON schema boundary fuzzer, and edge-case generator.

100% Python Standard Library implementation with zero external dependencies.

## Key Capabilities

- **Schema-Driven Realistic Mock Synthesis**: Generates plausible synthetic records covering UUIDs, emails, names, ISO-8601 timestamps, bounded numbers, and enums.
- **Reproducible Seeded Generation**: Guarantees identical dataset outputs across CI test suites via deterministic pseudorandom seeds.
- **Boundary & Exploit Vector Fuzzing**: Injects edge cases (empty strings, integer overflows, NaN/Infinity, SQL injection strings, Unicode emojis, null bytes) to stress-test validation routines.
- **Lightweight Zero-Dependency Operation**: Built entirely on standard Python without heavyweight binary packages.

## Architecture

```
[Target JSON Schema Specification + Seed Configuration]
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│                 SyntheticDataFuzzer                    │
│  - Type & Format Synthesizer (UUID, Email, ISO Dates)  │
│  - Bounded Numeric Range & Enum Generator              │
│  - Multi-Type Boundary Fuzzing Vector Injector         │
│  - Synthetic Metadata & Fuzz Tracker                   │
└────────────────────────────────────────────────────────┘
          │                                  │
    (Clean Mode)                       (Fuzz Mode)
          ▼                                  ▼
[Realistic Synthetic Record]        [Boundary Edge-Case Record]
```

## MCP Server Integration

Run standard MCP stdio server:
```bash
python mcp_server.py
```

Exposed Tools:
- `generate_mock_record`: Generates realistic mock data records matching JSON schema properties.
- `fuzz_record`: Generates boundary fuzzing edge-case records to test validation robustness.

## Quickstart (Python API)

```python
from client import SyntheticDataFuzzer

schema = {"user_id": {"type": "string", "format": "uuid"}, "email": {"type": "string", "format": "email"}}
record = SyntheticDataFuzzer.generate_record(schema)
print("Generated Record:", record)
```

---

## GenPark Ecosystem

- **Official Website**: [https://www.genpark.ai](https://www.genpark.ai)
- **LinkedIn Page**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)
