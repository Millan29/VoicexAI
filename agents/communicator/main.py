"""
Communicator uAgent

Interfaces with human ethics partner by logging summaries and ethics reports.
In a real deployment, this would back a dashboard/API.
"""

import json
import os
from uagents import Agent, Context
from uagents.setup import fund_agent_if_low

from schemas.messages import SummaryReady, EthicsReport

DATA_DIR = "data"
SUMMARY_FILE = os.path.join(DATA_DIR, "summaries.jsonl")
ETHICS_FILE = os.path.join(DATA_DIR, "ethics.jsonl")
os.makedirs(DATA_DIR, exist_ok=True)


agent = Agent(
    name="Twilio",
    seed="agent1qfcx8z8a5muprru7gvq0mkg9rn7x07my02z4z87u4ctfk02jc0ygwppw9fk",
    port=8001,  # Use port 8001 to avoid conflict
)

@agent.on_event("startup")
async def startup_handler(ctx: Context):
    ctx.logger.info(f"🚀 Twilio Communications Agent Started!")
    ctx.logger.info(f"📡 Agent Address: {agent.address}")
    ctx.logger.info(f"📝 Data Directory: {DATA_DIR}")
    ctx.logger.info(f"✅ Ready to receive SummaryReady and EthicsReport messages")

@agent.on_interval(period=30.0)
async def heartbeat(ctx: Context):
    # Check file sizes to show activity
    summary_count = 0
    ethics_count = 0
    
    if os.path.exists(SUMMARY_FILE):
        with open(SUMMARY_FILE, 'r') as f:
            summary_count = sum(1 for _ in f)
    
    if os.path.exists(ETHICS_FILE):
        with open(ETHICS_FILE, 'r') as f:
            ethics_count = sum(1 for _ in f)
    
    ctx.logger.info(f"💓 Heartbeat: {summary_count} summaries, {ethics_count} ethics reports processed")


@agent.on_message(model=SummaryReady)
async def handle_summary(ctx: Context, msg: SummaryReady):
    ctx.logger.info(f"Summary for {msg.doc_id}: {msg.key_points[:3]}")
    with open(SUMMARY_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(msg.dict()) + "\n")


@agent.on_message(model=EthicsReport)
async def handle_ethics(ctx: Context, msg: EthicsReport):
    summary = json.dumps(msg.report.get('summary', {}))
    ctx.logger.info(f"Ethics report for {msg.doc_id}: {summary}")
    with open(ETHICS_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps({
            "doc_id": msg.doc_id,
            "report": msg.report,
            "risks": msg.risks,
            "recommendations": msg.recommendations,
            "metadata": msg.metadata
        }) + "\n")


