from typing import Union, Optional

from fastapi import FastAPI
import uvicorn

from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter, SimpleSpanProcessor,
)

app = FastAPI()


provider = TracerProvider()
processor = SimpleSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)

# Sets the global default tracer provider
trace.set_tracer_provider(provider)

tracer = trace.get_tracer("fastapi-otel-demo")


@app.get("/")
async def read_root():
    with tracer.start_as_current_span("root") as span:
        span.set_attribute("msg", "noa was here")
        return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

FastAPIInstrumentor.instrument_app(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)