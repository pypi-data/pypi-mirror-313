from typing import *
from itertools import chain
from contextlib import contextmanager
from rest_framework import serializers
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import ErrorDetail
from pydantic import ValidationError


class CSRFExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


class handle_pydantic_validation:
    def __init__(self, path: Sequence[str] = ['non_field_errors']):
        self.exception = None
        self.path = path

    def __enter__(self):
        return self

    def reraise(self):
        e = self.exception

        if self.exception is None:
            return

        data = {}

        for x in e.errors():
            current = data
            last = x['loc'][-1]

            for field in chain(self.path, x['loc'][:-1]):
                if field not in current:
                    current[field] = {}

                current = current[field]

            if last not in current:
                current[last] = []

            current[last].append(ErrorDetail(x['msg'], code=x['type']))

        raise serializers.ValidationError(data)

    def __exit__(self, e_cls, e, traceback):
        if not isinstance(e, ValidationError):
            return False

        self.exception = e

        return True
