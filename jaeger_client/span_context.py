# Copyright (c) 2016 Uber Technologies, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from __future__ import absolute_import

import opentracing


class SpanContext(opentracing.SpanContext):
    __slots__ = ['trace_id', 'span_id', 'parent_id', 'flags',
                 '_baggage', '_debug_id']

    """Implements opentracing.SpanContext"""
    def __init__(self, trace_id, span_id, parent_id, flags, baggage=None):
        self.trace_id = trace_id
        self.span_id = span_id
        self.parent_id = parent_id or None
        self.flags = flags
        self._baggage = baggage or opentracing.SpanContext.EMPTY_BAGGAGE
        self._debug_id = None

    @property
    def baggage(self):
        return self._baggage or opentracing.SpanContext.EMPTY_BAGGAGE

    def with_baggage_item(self, key, value):
        baggage = dict(self._baggage)
        baggage[key] = value
        return SpanContext(
            trace_id=self.trace_id,
            span_id=self.span_id,
            parent_id=self.parent_id,
            flags=self.flags,
            baggage=baggage,
        )

    @property
    def is_debug_id_container_only(self):
        return not self.trace_id and self._debug_id is not None

    @property
    def debug_id(self):
        return self._debug_id

    @staticmethod
    def with_debug_id(debug_id):
        ctx = SpanContext(
            trace_id=None, span_id=None, parent_id=None, flags=None
        )
        ctx._debug_id = debug_id
        return ctx
