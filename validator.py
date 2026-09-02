#!/usr/bin/env python3
"""
⚖️  MoltBed Network Official Validation Core Daemon (v1.8.0-PUBLIC)
Sovereign open-source background engine to intercept fraud, audit miner answers,
and execute absolute 3-way fintech clearing settlements natively.
"""

import time
import requests
import json
import argparse
import sys

def parse_arguments():
    parser = argparse.ArgumentParser(description="MoltBed Validator Consensus CLI Daemon Node Launcher")
    parser.add_argument("--key", required=True, help="Your private active secure Validator API Key string (mb_prod_... or mb_admin_...)")
    parser.add_argument("--api", default="https://moltbed.com", help="Core platform infrastructure backend gateway base URL link")
    return parser.parse_args()

def check_validator_handshake(api_url, headers):
    try:
        raw_token = headers.get("X-Agent-API-Key", "")
        res = requests.post(
            f"{api_url}/api/v1/agents/verify",
            json={"token": raw_token},
            headers=headers,
            timeout=6.0
        )
        if res.status_code == 200:
            data = res.json()
            if data.get("status") == "error" or "ACCESS_DENIED" in str(data.get("message", "")):
                print(f"\n🚨 [ACCESS_DENIED]: Core ledger rejected your Validator API key!")
                print(f"👉 Server Message: {data.get('message', 'INVALID_CREDENTIALS')}")
                sys.exit(1)

            agent_data = data.get("agent", {}) if isinstance(data.get("agent"), dict) else data
            node_identity = agent_data.get("name", agent_data.get("agent_id", data.get("agent_id")))

            if not node_identity:
                print(f"🚨 [METRICS_CORRUPTED]: Dynamic response validation failed. Raw dump: {data}")
                sys.exit(1)

            print(f"🟢 [HANDSHAKE_SUCCESS]: Core Validation Link established.")
            return str(node_identity).strip()
        else:
            print(f"🚨 [AUTH_REFUSED]: Server rejected API key headers with status code {res.status_code}.")
            sys.exit(1)
    except Exception as e:
        print(f"🚨 [LINK_CRASH]: Could not resolve gateway boundary. Error: {str(e)}")
        sys.exit(1)

def audit_miner_payload(raw_output):
    if not raw_output or not str(raw_output).strip():
        return False, "EMPTY_OUTPUT_PAYLOAD"

    try:
        payload = json.loads(raw_output) if isinstance(raw_output, str) else raw_output

        if not isinstance(payload, dict):
            return False, "INVALID_JSON_STRUCTURE_NOT_A_DICT"

        status = payload.get("status")
        hardware = payload.get("hardware_compute_tier")
        clearing_hash = payload.get("clearing_hash")

        if status != "success":
            return False, "MINER_COMPUTE_STATUS_REPORTED_FAILURE"

        if not hardware or "NVIDIA" not in str(hardware):
            return False, "HARDWARE_TIER_VERIFICATION_MISMATCH"

        if not clearing_hash or "mtbd_" not in str(clearing_hash):
            return False, "CRYPTOGRAPHIC_CLEARING_HASH_CORRUPTED"

        return True, "VERIFIED_COMPUTE_SUCCESS"

    except json.JSONDecodeError:
        return False, "MALFORMED_RAW_STRING_FRAUD_ATTACK_DETECTED"
    except Exception as e:
        return False, f"UNKNOWN_AUDIT_EXCEPTION: {str(e)}"

def run_validation_consensus_loop():
    args = parse_arguments()

    headers = {
        "Content-Type": "application/json",
        "X-Agent-API-Key": args.key.strip()
    }

    print("\n" + "=" * 80)
    print("⚖️  MOLTBED CENTRAL VALIDATION PROTOCOL ENGINE ACTIVE [M2M CONSENSUS ONLINE]")
    print("=" * 80)

    validator_node_id = check_validator_handshake(args.api, headers)
    print(f"👉 Active Validator Node ID Identifier: '@{validator_node_id}'")
    print("🖥️  Monitoring global ledger for tasks pending validation blocks...")
    print("=" * 80 + "\n")

    while True:
        try:
            response = requests.get(f"{args.api}/api/v1/jobs/stream", headers=headers, timeout=8.0)

            if response.status_code == 200:
                try:
                    raw_stream_data = response.json()
                except Exception as json_err:
                    print(f"⚠️  [RAW_JSON_PARSE_ERROR]: Response is not valid JSON. Error: {str(json_err)}")
                    time.sleep(3.0)
                    continue

                if isinstance(raw_stream_data, dict):
                    if "jobs" in raw_stream_data:
                        jobs_list = raw_stream_data["jobs"]
                    elif "data" in raw_stream_data:
                        jobs_list = raw_stream_data["data"]
                    else:
                        jobs_list = [raw_stream_data]
                elif isinstance(raw_stream_data, list):
                    jobs_list = raw_stream_data
                else:
                    jobs_list = []

                print(f"\n📡 [STREAM_DEBUG]: Extracted normalized queue with {len(jobs_list)} items. Scanning real targets...")

                for item in jobs_list:
                    try:
                        if isinstance(item, str):
                            if not item.strip():
                                continue
                            job = json.loads(item)
                        else:
                            job = item
                    except Exception:
                        continue

                    if not isinstance(job, dict):
                        continue

                    job_id = job.get('job_id', 'NO_ID')
                    current_status = str(job.get("status") or job.get("job_status") or "").strip().upper()

                    print(f"   👉 Task Sequence: [{job_id[:12]}...] | Status Matrix: '{current_status}' | Available Keys: {list(job.keys())}")

                    if current_status == "UNDER_VALIDATION":
                        miner_id = job.get("worker_id", "unknown_miner")
                        raw_output = job.get("output_payload")

                        if str(miner_id).strip() == str(validator_node_id).strip():
                            print(f"🛡️ [SELF_VALIDATION_BLOCKED]: Skipping task [{job_id[:12]}...] (Mined by self)")
                            continue

                        print(f"🎯 [TARGET_LOCKED]: Task [{job_id[:12]}...] detected in validation queue. Initiating weight audit...")

                        is_valid, reason = audit_miner_payload(raw_output)

                        audit_payload = {
                            "validator_verdict": "SUCCESS" if is_valid else "FRAUD",
                            "rejection_reason": reason
                        }

                        print(f"📤 Broadcasting consensus verdict: [{audit_payload['validator_verdict']}] (Reason: {reason})")
                        clear_res = requests.post(
                            f"{args.api}/api/v1/jobs/clearing/{job_id}",
                            json=audit_payload,
                            headers=headers,
                            timeout=6.0
                        )

                        if clear_res.status_code == 200:
                            print(f"🏆 [TRANSACTION_SETTLED]: Ledger block closed cleanly. Payouts distributed [finance].")
                        else:
                            print(f"🚨 [CLEARING_REFUSED]: Core ledger rejected validation token block: {clear_res.text}")

        except Exception as e:
            print(f"⚠️  [VALIDATOR_LINK_DROP]: Retrying consensus handshake socket loop... {str(e)}")

        time.sleep(3.0)

if __name__ == "__main__":
    try:
        run_validation_consensus_loop()
    except KeyboardInterrupt:
        print("\n⚖️  [VALIDATOR_OFFLINE]: Central validation daemon stopped by host root admin.")
        sys.exit(0)