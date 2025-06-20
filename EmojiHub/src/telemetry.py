from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor

from prometheus_fastapi_instrumentator import Instrumentator

from fastapi import FastAPI

def setup_telemetry(app: FastAPI):
    # Configure OpenTelemetry tracing
    resource = Resource(attributes={"service.name": "fastapi-app"})
    trace.set_tracer_provider(TracerProvider(resource=resource))

    otlp_exporter = OTLPSpanExporter(endpoint="http://tempo:4318/v1/traces")
    trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_exporter))

    # Instrument logging to include trace context
    LoggingInstrumentor().instrument()

    # Instrument FastAPI for tracing
    FastAPIInstrumentor.instrument_app(app)

    # Instrument FastAPI for Prometheus metrics
    Instrumentator().instrument(app).expose(app)