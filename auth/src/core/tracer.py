from core.config import config
from flask import Flask
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter


def configure_tracer() -> None:
    trace.set_tracer_provider(TracerProvider(resource=Resource.create({"service.name": "Auth"})))
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                agent_host_name=config.JAEGER_HOST,
                agent_port=config.JAEGER_PORT,
            )
        )
    )
    # Чтобы видеть трейсы в консоли
    if config.DEBUG:
        trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))


def init_tracer(app: Flask) -> None:
    configure_tracer()
    FlaskInstrumentor().instrument_app(app)
