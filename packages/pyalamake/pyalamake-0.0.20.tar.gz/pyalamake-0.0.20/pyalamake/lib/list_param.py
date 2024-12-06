import os

from .svc import svc


# --------------------
## List oriented parameter
class ListParam:
    # --------------------
    ## constructor
    #
    # @param tag         the function name tag
    # @param parm_type   list of strings or paths
    # @param parent      the parent class
    # @param filter_fn   optional filter function callback; used to filter out various items; otherwise None
    # @param accum_fn    optional accumulator function callback; gathers the list of items into a parameter string
    def __init__(self, tag, parm_type, parent, filter_fn, accum_fn):
        ## holds the name of parameter; to generate function names
        self._tag = tag
        ## parameter type: either 'string' or 'path'
        self._parm_type = parm_type
        ## reference to the parent class
        self._parent = parent
        ## holds the parent class's name
        self._parent_name = self._parent.__class__.__name__
        ## filter callback function
        self._filter_fn = filter_fn
        ## accumulator callback function
        self._accum_fn = accum_fn

        if self._parm_type not in ['string', 'path']:
            svc.abort(f'ListParm {tag}: unknown type "{parm_type}"')

        ## holds the current list of parameter values
        self._values = []

        # define function (property) to return current values
        ## see property values; note will overwrite any existing function
        setattr(self._parent, self._tag, self.values)

        # define function to add values; note will overwrite any existing function
        fn = f'add_{self._tag}'
        ## see function update()
        setattr(self._parent, fn, self.update)

        # define function to remove a single value; note will overwrite any existing function
        fn = f'remove_{self._tag}'
        ## see function update()
        setattr(self._parent, fn, self.remove)

    # --------------------
    ## returns list of current values
    # @return list of current values
    @property
    def values(self):
        return self._values

    # --------------------
    ## remove the given value, if present in the list of values
    #
    # @param vals  the values to remove
    # @return None
    def remove(self, vals):
        if isinstance(vals, list):
            pass
        elif isinstance(vals, str):
            # convert to a list
            vals = [vals]
        else:
            svc.abort(f'{self._tag}: can only remove strings: {vals} is {type(vals)}')

        for val in vals:
            if not isinstance(val, str):
                svc.abort(f'{self._tag}: accepts only str or list of str, {val} is {type(val)}')

            if val in self._values:
                self._values.remove(val)
                if self._accum_fn:
                    self._accum_fn()

    # --------------------
    ## add additional values to the current list.
    #   * skips if the value is already present
    #   * skips if the value is empty "" or None
    #   * aborts if any of the values passed in is not a string
    #
    # @param vals  the values to add; accepts a string or a list of strings
    # @return None
    def update(self, vals):
        if isinstance(vals, list):
            pass
        elif isinstance(vals, str):
            # convert to a list
            vals = [vals]
        else:
            svc.abort(f'{self._tag}: can only add strings: {vals} is {type(vals)}')

        for val in vals:
            if not isinstance(val, str):
                svc.abort(f'{self._tag}: accepts only str or list of str, {val} is {type(val)}')

            # user can add an empty entry
            if not val:
                continue

            # if value matches filter, then don't add
            if self._filter_fn and self._filter_fn(val):
                continue

            if self._parm_type == 'path':
                updated_val = os.path.expanduser(val)
            else:  # parm_type == 'string'
                updated_val = val
            updated_val = os.path.normpath(updated_val)

            if updated_val in self._values:
                svc.log.line(f'{self._tag}: {val} is already added: {self._values}')
                continue

            self._values.append(updated_val)

        if self._accum_fn:
            self._accum_fn()
