"""
Agent Registry uAgent

Handles agent registration, discovery, and blockchain coordination for the Wagwan Swarm.
"""

import json
import os
from typing import Dict, List, Any
from uagents import Agent, Context

from schemas.messages import CrawlRequest, PDFReady, ParsedText, SummaryReady, EthicsReport

# Registry storage
REGISTRY_DIR = "data/registry"
AGENTS_FILE = os.path.join(REGISTRY_DIR, "agents.json")
BLOCKCHAIN_FILE = os.path.join(REGISTRY_DIR, "blockchain.json")
os.makedirs(REGISTRY_DIR, exist_ok=True)

agent = Agent(
    name="Agent Registry",
    seed="agent1q28ryexcvl2hv55gatd4dur07tlzcweqxmyk6dahrn4va0sdqt2lk2zfywa",
    port=8003,  # Use port 8003 for registry
)


@agent.on_event("startup")
async def startup_handler(ctx: Context):
    ctx.logger.info("🏛️ Agent Registry & Blockchain Coordinator Started!")
    ctx.logger.info(f"📡 Agent Address: {agent.address}")
    ctx.logger.info(f"🔗 Blockchain Coordination: Active")
    ctx.logger.info(f"📋 Registry Directory: {REGISTRY_DIR}")
    ctx.logger.info("✅ Ready for agent registration and discovery")
    
    # Initialize registry files
    await initialize_registry(ctx)


@agent.on_interval(period=60.0)
async def registry_heartbeat(ctx: Context):
    registered_count = await get_registered_agent_count()
    ctx.logger.info(f"📊 Registry Status: {registered_count} agents registered")


async def initialize_registry(ctx: Context):
    """Initialize empty registry files if they don't exist."""
    from datetime import datetime
    current_time = datetime.now().isoformat()
    
    if not os.path.exists(AGENTS_FILE):
        initial_agents = {
            "agents": [],
            "last_updated": current_time,
            "total_count": 0
        }
        with open(AGENTS_FILE, 'w') as f:
            json.dump(initial_agents, f, indent=2)
        ctx.logger.info("📝 Initialized agents registry")
    
    if not os.path.exists(BLOCKCHAIN_FILE):
        initial_blockchain = {
            "transactions": [],
            "blocks": [],
            "last_sync": current_time
        }
        with open(BLOCKCHAIN_FILE, 'w') as f:
            json.dump(initial_blockchain, f, indent=2)
        ctx.logger.info("⛓️ Initialized blockchain coordination")


async def get_registered_agent_count() -> int:
    """Get count of registered agents."""
    try:
        if os.path.exists(AGENTS_FILE):
            with open(AGENTS_FILE, 'r') as f:
                data = json.load(f)
                return len(data.get("agents", []))
    except Exception:
        pass
    return 0


@agent.on_message(model=CrawlRequest)
async def handle_registration_request(ctx: Context, msg: CrawlRequest):
    """Handle agent registration requests via CrawlRequest."""
    ctx.logger.info(f"🔍 Processing registration for {len(msg.urls)} potential agents")
    
    # Load current registry
    try:
        with open(AGENTS_FILE, 'r') as f:
            registry = json.load(f)
    except Exception:
        registry = {"agents": [], "total_count": 0}
    
    # Add new agents to registry
    for url in msg.urls:
        from datetime import datetime
        agent_info = {
            "url": url,
            "registered_at": datetime.now().isoformat(),
            "status": "active",
            "metadata": msg.metadata or {}
        }
        registry["agents"].append(agent_info)
        ctx.logger.info(f"📋 Registered agent: {url}")
    
    registry["total_count"] = len(registry["agents"])
    registry["last_updated"] = datetime.now().isoformat()
    
    # Save updated registry
    with open(AGENTS_FILE, 'w') as f:
        json.dump(registry, f, indent=2)
    
    ctx.logger.info(f"✅ Registry updated: {registry['total_count']} total agents")


@agent.on_message(model=SummaryReady)
async def handle_summary_coordination(ctx: Context, msg: SummaryReady):
    """Handle summary coordination for blockchain logging."""
    ctx.logger.info(f"📄 Coordinating summary for doc {msg.doc_id}")
    
    # Log to blockchain coordination
    try:
        with open(BLOCKCHAIN_FILE, 'r') as f:
            blockchain_data = json.load(f)
    except Exception:
        blockchain_data = {"transactions": [], "blocks": []}
    
    from datetime import datetime
    current_time = datetime.now().isoformat()
    
    transaction = {
        "type": "summary_ready",
        "doc_id": msg.doc_id,
        "timestamp": current_time,
        "agent": "summarizer",
        "data_hash": hash(str(msg.summary))
    }
    
    blockchain_data["transactions"].append(transaction)
    blockchain_data["last_sync"] = current_time
    
    with open(BLOCKCHAIN_FILE, 'w') as f:
        json.dump(blockchain_data, f, indent=2)
    
    ctx.logger.info(f"⛓️ Blockchain: Logged summary transaction for {msg.doc_id}")


@agent.on_message(model=EthicsReport)
async def handle_ethics_coordination(ctx: Context, msg: EthicsReport):
    """Handle ethics report coordination for blockchain logging."""
    ctx.logger.info(f"⚖️ Coordinating ethics report for doc {msg.doc_id}")
    
    # Log to blockchain coordination
    try:
        with open(BLOCKCHAIN_FILE, 'r') as f:
            blockchain_data = json.load(f)
    except Exception:
        blockchain_data = {"transactions": [], "blocks": []}
    
    from datetime import datetime
    current_time = datetime.now().isoformat()
    
    transaction = {
        "type": "ethics_report",
        "doc_id": msg.doc_id,
        "timestamp": current_time,
        "agent": "ethical_analyst",
        "risks_count": len(msg.risks),
        "recommendations_count": len(msg.recommendations),
        "data_hash": hash(str(msg.report))
    }
    
    blockchain_data["transactions"].append(transaction)
    blockchain_data["last_sync"] = current_time
    
    with open(BLOCKCHAIN_FILE, 'w') as f:
        json.dump(blockchain_data, f, indent=2)
    
    ctx.logger.info(f"⛓️ Blockchain: Logged ethics transaction for {msg.doc_id}")


if __name__ == "__main__":
    agent.run()