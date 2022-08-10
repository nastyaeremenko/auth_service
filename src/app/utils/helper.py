from http import HTTPStatus

import redis
from flask import request
from flask_restful import abort
from marshmallow import ValidationError


def validate_request(data_validate):
    try:
        valid_data = data_validate.load(request.get_json(force=True))
    except ValidationError as errors:
        abort(HTTPStatus.BAD_REQUEST, errors=errors.messages)
    return valid_data


def add_db_redis_pipeline(pipeline: redis.client.Pipeline,
                          data_pipeline) -> None:
    for item in data_pipeline:
        pipeline.setex(*item)
    pipeline.execute()
