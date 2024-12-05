# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class StreamingBuffer(Component):
    """A StreamingBuffer component.
The StreamingBuffer makes it possible to buffer data from a ResponseStream. It's a wrapper around the SSE.js library.
https://github.com/mpetazzoni/sse.js

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- done (boolean; optional):
    A boolean indicating if the stream has ended.

- options (dict; optional):
    Options passed to the SSE constructor.
    https://github.com/mpetazzoni/sse.js?tab=readme-ov-file#options-reference.

    `options` is a dict with keys:

    - debug (boolean; optional)

    - headers (dict; optional)

    - method (string; optional)

    - payload (dict; optional)

    - start (boolean; optional)

    - withCredentials (boolean; optional)

- url (string; optional):
    URL of the endpoint.

- value (string; optional):
    The data value (streamed, buffered)."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_extensions'
    _type = 'StreamingBuffer'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, options=Component.UNDEFINED, url=Component.UNDEFINED, value=Component.UNDEFINED, done=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'done', 'options', 'url', 'value']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'done', 'options', 'url', 'value']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(StreamingBuffer, self).__init__(**args)
