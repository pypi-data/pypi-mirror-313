# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Terminator(Component):
    """A Terminator component.
An interface to server sent events in Dash

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- url (string; required):
    A DOMString representing the URL of the source.

- withCredentials (boolean; optional):
    A boolean value indicating whether the EventSource object was
    instantiated with cross-origin (CORS) credentials set (True), or
    not (False, the default)."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_extensions'
    _type = 'Terminator'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, withCredentials=Component.UNDEFINED, url=Component.REQUIRED, **kwargs):
        self._prop_names = ['id', 'url', 'withCredentials']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'url', 'withCredentials']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['url']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(Terminator, self).__init__(**args)
