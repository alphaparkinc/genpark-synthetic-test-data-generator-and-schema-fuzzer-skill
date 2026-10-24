"""Synthetic Test Data Generator and Schema Fuzzer.
100% Python Standard Library.
"""

import random
import uuid
import time
from typing import Dict, Any, List, Optional


class SyntheticDataFuzzer:
    """Generates realistic synthetic mock data and schema-driven boundary fuzzing vectors
    for testing data pipelines, APIs, and ML models without external dependencies."""

    FIRST_NAMES = ["James", "Emma", "Liam", "Olivia", "Noah", "Ava", "Lucas", "Sophia"]
    LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis"]
    DOMAINS = ["example.com", "genpark.ai", "enterprise.org", "techlab.io"]

    FUZZ_VECTORS = {
        "string": ["", " ", "A" * 1024, "'; DROP TABLE test; --", "<script>alert(1)</script>", "🔥🚀💻🧪", "\x00\r\n\t"],
        "integer": [0, -1, 2147483647, -2147483648, 9223372036854775807, -9223372036854775808],
        "number": [0.0, -0.0, float("inf"), float("-inf"), 1e308, -1e308, 0.00000000001],
        "boolean": [None, 0, 1, "true", "false"],
    }

    @classmethod
    def generate_record(
        cls,
        schema_properties: Dict[str, Any],
        seed: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Generates realistic structured mock record from schema definition."""
        rng = random.Random(seed)
        record = {}

        for field_name, spec in schema_properties.items():
            field_type = spec.get("type", "string").lower()
            field_format = spec.get("format", "").lower()

            if "enum" in spec:
                record[field_name] = rng.choice(spec["enum"])
            elif field_format == "uuid":
                record[field_name] = str(uuid.UUID(int=rng.getrandbits(128), version=4))
            elif field_format == "email":
                fn = rng.choice(cls.FIRST_NAMES).lower()
                ln = rng.choice(cls.LAST_NAMES).lower()
                dm = rng.choice(cls.DOMAINS)
                record[field_name] = f"{fn}.{ln}{rng.randint(10, 99)}@{dm}"
            elif field_format == "iso_date":
                offset = rng.randint(0, 365 * 86400)
                record[field_name] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() - offset))
            elif field_type == "integer":
                min_v = spec.get("minimum", 1)
                max_v = spec.get("maximum", 1000)
                record[field_name] = rng.randint(min_v, max_v)
            elif field_type == "number":
                min_v = spec.get("minimum", 1.0)
                max_v = spec.get("maximum", 1000.0)
                record[field_name] = round(rng.uniform(min_v, max_v), 2)
            elif field_type == "boolean":
                record[field_name] = rng.choice([True, False])
            else:
                # General string
                if "name" in field_name.lower():
                    record[field_name] = f"{rng.choice(cls.FIRST_NAMES)} {rng.choice(cls.LAST_NAMES)}"
                else:
                    record[field_name] = f"mock_{field_name}_{rng.randint(100, 999)}"

        return record

    @classmethod
    def fuzz_record(
        cls,
        schema_properties: Dict[str, Any],
        target_fuzz_field: Optional[str] = None,
        seed: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Generates a record with deliberate boundary edge-cases and anomalous vectors."""
        rng = random.Random(seed)
        base = cls.generate_record(schema_properties, seed=seed)

        # Pick a field to fuzz
        field_to_fuzz = target_fuzz_field or rng.choice(list(schema_properties.keys()))
        spec = schema_properties.get(field_to_fuzz, {})
        f_type = spec.get("type", "string").lower()

        vectors = cls.FUZZ_VECTORS.get(f_type, cls.FUZZ_VECTORS["string"])
        fuzzed_val = rng.choice(vectors)

        base[field_to_fuzz] = fuzzed_val
        base["_fuzzed_metadata"] = {
            "field": field_to_fuzz,
            "injected_vector": str(fuzzed_val),
            "expected_type": f_type,
        }
        return base
