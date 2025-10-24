"""
Orchestrator uAgent

Receives messages and routes them to the appropriate next agent in the pipeline.
"""

from uagents import Agent, Context

from schemas.messages import CrawlRequest, PDFReady, ParsedText, SummaryReady, EthicsReport


agent = Agent(
    name="Aethel", 
    seed="sk_dfdb772ee76f4a519f2d81870831911bb99530554f754e36a29aad452bf729df",
    port=8002,  # Use port 8002 for orchestrator
)


# In a real deployment, these could be loaded from env/config or registry
INTERPRETER_ADDR = "interpreter"
SUMMARIZER_ADDR = "summarizer"
ETHICS_ADDR = "ethical_analyst"
COMMUNICATOR_ADDR = "Twilio"  # Updated to use Twilio's name
REGISTRY_ADDR = "Agent Registry"  # Agent Registry for coordination


@agent.on_event("startup")
async def startup_handler(ctx: Context):
    ctx.logger.info("🔮 Aethel Orchestrator & Sentinel Started!")
    ctx.logger.info(f"📡 Agent Address: {agent.address}")
    ctx.logger.info("🎭 Role: Message routing and pipeline orchestration")
    ctx.logger.info("✅ Ready to route CrawlRequest, PDFReady, ParsedText, SummaryReady, EthicsReport")


@agent.on_interval(period=45.0)
async def sentinel_heartbeat(ctx: Context):
    ctx.logger.info("🛡️ Aethel Sentinel: Pipeline monitoring active")


@agent.on_message(model=CrawlRequest)
async def handle_crawl(ctx: Context, msg: CrawlRequest):
    ctx.logger.info(f"🔀 Routing CrawlRequest with {len(msg.urls)} URLs to librarian")
    await ctx.send("librarian", msg)


@agent.on_message(model=PDFReady)
async def route_pdf(ctx: Context, msg: PDFReady):
    ctx.logger.info(f"📄 Routing PDFReady for {msg.url} to {INTERPRETER_ADDR}")
    await ctx.send(INTERPRETER_ADDR, msg)


@agent.on_message(model=ParsedText)
async def route_parsed(ctx: Context, msg: ParsedText):
    ctx.logger.info(f"📝 Routing ParsedText for {msg.doc_id} to parallel analysis")
    await ctx.send(SUMMARIZER_ADDR, msg)
    await ctx.send(ETHICS_ADDR, msg)


@agent.on_message(model=SummaryReady)
async def route_summary(ctx: Context, msg: SummaryReady):
    ctx.logger.info(f"📊 Routing SummaryReady for {msg.doc_id} to {COMMUNICATOR_ADDR}")
    await ctx.send(COMMUNICATOR_ADDR, msg)
    await ctx.send(REGISTRY_ADDR, msg)  # Also coordinate via registry


@agent.on_message(model=EthicsReport)
async def route_ethics(ctx: Context, msg: EthicsReport):
    ctx.logger.info(f"⚖️ Routing EthicsReport for {msg.doc_id} to {COMMUNICATOR_ADDR}")
    await ctx.send(COMMUNICATOR_ADDR, msg)
    await ctx.send(REGISTRY_ADDR, msg)  # Also coordinate via registry


if __name__ == "__main__":
    agent.run()


