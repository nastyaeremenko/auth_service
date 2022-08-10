from uuid import uuid1

from flask import request
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.trace.export import BatchSpanProcessor, \
    ConsoleSpanExporter
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource


def configure_tracer(app, host='localhost', port=8631) -> None:
    trace.set_tracer_provider(
        TracerProvider(resource=Resource.create({SERVICE_NAME: "auth_app"})))
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                agent_host_name=host,
                agent_port=port,
            )
        )
    )
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(ConsoleSpanExporter()))

    FlaskInstrumentor().instrument_app(app)

    @app.before_request
    def before_request():
        request_id = request.headers.get('X-Request-Id')
        if not request_id:
            request_id = uuid1().hex
        current_span = trace.get_current_span()
        current_span.set_attribute("http.request_id", request_id)
