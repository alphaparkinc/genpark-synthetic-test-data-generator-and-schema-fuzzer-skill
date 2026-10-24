"""Example usage for Synthetic Test Data Generator and Schema Fuzzer."""
from client import SyntheticDataFuzzer


def main():
    user_schema = {
        "user_id": {"type": "string", "format": "uuid"},
        "full_name": {"type": "string"},
        "email": {"type": "string", "format": "email"},
        "age": {"type": "integer", "minimum": 18, "maximum": 80},
        "account_balance": {"type": "number", "minimum": 0.0, "maximum": 10000.0},
        "subscription_tier": {"type": "string", "enum": ["STARTER", "PRO", "ENTERPRISE"]},
        "is_active": {"type": "boolean"},
        "created_at": {"type": "string", "format": "iso_date"},
    }

    print("=== 1. Generating Clean Realistic Synthetic Records ===")
    for i in range(2):
        rec = SyntheticDataFuzzer.generate_record(user_schema, seed=42 + i)
        print(f"\nRecord #{i+1}:")
        for k, v in rec.items():
            print(f"  {k}: {v}")

    print("\n=== 2. Generating Boundary Fuzzing Vectors ===")
    fuzzed_email = SyntheticDataFuzzer.fuzz_record(user_schema, target_fuzz_field="email", seed=99)
    print("Fuzzed Email Record:")
    print(f"  email value: {repr(fuzzed_email['email'])}")
    print(f"  metadata: {fuzzed_email['_fuzzed_metadata']}")

    fuzzed_age = SyntheticDataFuzzer.fuzz_record(user_schema, target_fuzz_field="age", seed=101)
    print("\nFuzzed Age Record:")
    print(f"  age value: {fuzzed_age['age']}")
    print(f"  metadata: {fuzzed_age['_fuzzed_metadata']}")


if __name__ == "__main__":
    main()
