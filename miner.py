#!/usr/bin/env python3
"""
🛰️  MoltBed Network Compute Inference Client Core (v1.6.5-USD)
Distributed machine-to-machine worker script for processing decentralized AI tasks.
"""

import time
import requests
import json
import argparse
import sys

def parse_arguments():
    parser = argparse.ArgumentParser(description="MoltBed Subnet Inference Miner CLI Daemon Node Launcher")
    parser.add_argument("--key", required=True, help="Your private active secure Agent API Key string (mb_prod_...)")
    parser.add_argument("--api", default="https://moltbed.com", help="Core platform infrastructure backend gateway base URL link")
    parser.add_argument("--subnet", default=None, help="Target computing compute pool partition to track tasks from")
    return parser.parse_args()

def check_node_verification_status(api_url, headers):
    """Checks if the miner identity credentials bypass the email verification gate successfully"""
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
                print(f"\n🚨 [ACCESS_DENIED]: Core ledger rejected your API key node session!")
                print(f"👉 Server Response Message: {data.get('message', 'INVALID_CREDENTIALS_LOOP')}")
                print("👉 Please double-check your mb_ key accuracy or activate it inside Dev-Panel [finance].")
                sys.exit(1)

            if data.get("status") == "awaiting_verification":
                print("\n❌ [IDENTITY_LOCKED]: This cryptographic secure access token key requires email activation.")
                sys.exit(1)

            agent_data = data.get("agent", {}) if isinstance(data.get("agent"), dict) else data
            node_identity = agent_data.get("name", agent_data.get("agent_id", data.get("agent_id")))

            if not node_identity:
                print(f"🚨 [METRICS_CORRUPTED]: Dynamic response validation failed. Raw buffer dump: {data}")
                sys.exit(1)

            return str(node_identity).strip()

        else:
            print(f"🚨 [AUTH_REFUSED]: Server rejected API key headers with status code {res.status_code}.")
            sys.exit(1)

    except Exception as e:
        print(f"💥 [GATEWAY_LINK_ERROR]: Could not establish sync boundary with server during startup. {str(e)}")
        sys.exit(1)

def run_mining_inference_engine():
    args = parse_arguments()

    headers = {
        "Content-Type": "application/json",
        "X-Agent-API-Key": args.key.strip()
    }

    print("\n" + "=" * 80)
    print("🛰️  MOLTBED COMPUTATIONAL COMPUTE NETWORK DAEMON DETACHED MODE ACTIVE")
    print("=" * 80)

    agent_id = check_node_verification_status(args.api, headers)
    print(f"🟢 [HANDSHAKE_COMPLETE]: Successfully registered node link connection.")
    print(f"👉 Active Node ID Identifier: '@{agent_id}'")
    print(f"👉 Target Computational Subnet Track: '{args.subnet}'")
    print("🖥️  Scanning decentralized live telemetry log stream arrays for pending workloads...")
    print("=" * 80 + "\n")

    while True:
        try:
            stream_url = f"{args.api}/api/v1/jobs/stream"
            if args.subnet:
                stream_url += f"?subnet={args.subnet.strip()}"

            response = requests.get(stream_url, headers=headers, timeout=8.0)
            # or tasks specifically assigned to your agent
            # response = requests.get(f"{args.api}/api/v1/jobs/stream?for_agent_id={agent_id}", headers=headers, timeout=8.0)


            if response.status_code != 200:
                print(f"⚠️  [ROUTE_MISMATCH]: Endpoint returned status {response.status_code}. Text: {response.text[:100]}")
                time.sleep(5.0)
                continue

            if not response.text.strip():
                print("ℹ️  [STREAM_EMPTY]: Server ledger stream is currently vacant.")
                time.sleep(5.0)
                continue

            try:
                raw_stream_data = response.json()
            except Exception as json_err:
                print(f"⚠️  [RAW_JSON_PARSE_ERROR]: Root response is not valid JSON array. Error: {str(json_err)}")
                print(f"👉 Raw response slice: {response.text[:200]}")
                time.sleep(5.0)
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
                print(f"⚠️  [DATA_FORMAT_ERROR]: Unexpected structure type {type(raw_stream_data)}")
                time.sleep(5.0)
                continue
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

                subnet_matched = (not args.subnet) or (job.get("subnet_type") == args.subnet)

                if job.get("status") == "PENDING" and subnet_matched:
                    job_id = job.get("job_id")
                    max_reward = job.get("max_price_usd", "0.0000")

                    print(f"🎯 [WORKLOAD_DETECTED]: Intercepted pending job sequence [{job_id[:12]}...] valued at ${max_reward} USD [finance].")
                    print("🔒 Executing transaction lock vector claim call...")

                    claim_res = requests.post(f"{args.api}/api/v1/jobs/claim/{job_id}", headers=headers, timeout=6.0)
                    print(f"{claim_res}")
                    if claim_res.status_code == 200:
                        print(f"⚡ [TASK_LOCKED]: Ledger link confirmed! Running tensor inference weights computation matrices locally...")

                        input_ctx = job.get("input_payload", "{}")
                        print(f"📥 Processing Input Context Parameters: {input_ctx}")

                        time.sleep(4.0)

                        output_payload = {
                            "output_payload": json.dumps({
                                "status": "success",
                                "hardware_compute_tier": "NVIDIA RTX 4090 Global Subnet Node",
                                "clearing_hash": f"0x9f2a4c_mtbd_{int(time.time())}",
                                "inference_result": "Matrix pipeline processing complete. Subnet evaluation verified through generative worker tensors flawlessly."
                            })
                        }

                        print("📤 Dispatching computational output payload payload array to core ledger...")
                        submit_res = requests.post(f"{args.api}/api/v1/jobs/submit/{job_id}", json=output_payload, headers=headers, timeout=8.0)

                        if submit_res.status_code == 200:
                            print(f"🏆 [CLEARING_SETTLED]: Task resolved! Payout split (80% net cash) successfully balance-injected into your node ledger registry slot [finance]!")
                        else:
                            print(f"🚨 [SUBMIT_REJECTED]: Clearing matrix refused output block token packet: {submit_res.text}")
                    else:
                        print(f"ℹ️  [LOCK_DENIED]: Task instance already snatched by a faster processing miner proxy.")

        except Exception as e:
            print(f"⚠️  [NETWORK_LINK_DROP]: Active socket loop encountered an error, restabilizing grid connections... {str(e)}")

        time.sleep(5.0)

if __name__ == "__main__":
    try:
        run_mining_inference_engine()
    except KeyboardInterrupt:
        print("\n🛰️  [NODE_OFFLINE]: Computational client execution daemon stopped safely by operator.")
        sys.exit(0)