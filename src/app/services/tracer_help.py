from functools import wraps

from flask import request
from opentelemetry import trace


def tracer_help(fn):
    @wraps(fn)
    def decorator(*args, **kwargs):
        tracer = trace.get_tracer(__name__)
        request_id = request.headers.get('X-Request-Id')
        with tracer.start_as_current_span(fn.__name__) as span:
            span.set_attribute('http.request_id', request_id)
            return fn(*args, **kwargs)
    return decorator
