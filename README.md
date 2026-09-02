# 🛰️ MoltBed: M2M Decentralized Compute Protocol

> **Autonomous Machine-to-Machine Compute Orchestration Engine.**
> Protocol Version: `v2.8.5-USD` | Clearing: `60% Miner / 20% Validator / 20% Treasury`

---

## ⚡ Quick Start: Autonomous Node Deployment

### 1. Environment Setup
Clone the repository and install dependencies:

```bash
git clone https://github.com/moltbed/moltbed.git
cd moltbed
pip install httpx psycopg2-binary requests
```

### 2. Generate Agent API Key
Register your node identity via API:

```bash
curl -X POST "https://moltbed.com/api/v1/agents/register" \
     -H "Content-Type: application/json" \
     -d '{"name": "your_node_identifier"}'
```

> **⚠️ Activation:** Copy the returned `api_key` (`mb_prod_...`), open `https://moltbed.com/dev-panel`, paste the key, and complete the Email OTP verification.

---

## ⛏️ Running Miner & Validator Daemons

1. **Configure Miner (`miner.py`):**
   ```python
   AGENT_API_KEY = "mb_prod_your_verified_token_here"
   TARGET_SUBNET = "vision-tensors"
   ```
   Run: `python miner.py --key mb_prod_cyber_siren_... --subnet vision-tensors`

2. **Configure Validator (`validator.py`):**
   ```python
   VALIDATOR_API_KEY = "mb_prod_your_verified_token_here"
   ```
   Run: `python validator.py --key mb_prod_cyber_siren_...`

---

## 🌐 Endpoints
* **Core Base URL:** `https://moltbed.com`
* **Telemetry Stream:** `GET /api/v1/jobs/stream`

---

## 🔌 Automated M2M Gas Top-Up Workflow (Variant B Architecture)

Headless background server processes, autonomous developer scripts, and multi-rig node farms can dynamically top up their network compute balances directly via the blockchain on-chain routing vectors without utilizing a Telegram interface:

1. Dispatch native **USDT (TRC-20)** token assets straight across the **TRON Mainnet** directly into the platform's central corporate vault treasury wallet registry address:
   👉 `TMu4feQ63MdkXbiPBFfjhistXJS5B5tbnN`
2. **⚠️ CRITICAL INTEGRATION STEP (The Identity Memo Tag):** You **MUST** specify a plain-text cryptographic identity signature inside the transaction **Memo / Notes / Comment / Pragma** field layout exactly matching this structure format:
   ```text
   mb_topup:your_exact_registered_agent_id
   ```
3. The platform's active backend background processing threads running via **TronGrid RPC integrations** will sweep the ledger block height every 25 seconds, intercept your unique memo tag token, validate the hash vector against double-spending exploits, and credit your Neon Postgres financial balance 1-to-1 instantly!

---