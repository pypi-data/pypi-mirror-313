from . import services


# -------------------
## holds trace matrix data
class TraceMatrix:
    # -------------------
    ## constructor
    def __init__(self):
        ## holds the trace matrix info
        self._matrix = {}
        ## holds the current test script name
        self._current_test_script = None
        ## indicates if there is any information to be saved to the output file
        self._dirty = False

    # -------------------
    ## ensure that the current data is cleared out when the test script changes
    #
    # @return None
    def check_test_script(self):
        if self._current_test_script != services.cfg.test_script:
            if self._current_test_script is not None:
                self.save()

            self._current_test_script = services.cfg.test_script
            self._matrix = {}
            self._dirty = True

    # -------------------
    ## terminate
    #
    # @return None
    def term(self):
        self.save()

    # -------------------
    ## add protocol info to one or more reqids
    #
    # @param req_ids      one or more reqids to add
    # @param proto_id     the protocol id
    # @param proto_info   additional protocol information
    # @return None
    def add_proto(self, req_ids, proto_id, proto_info):
        self.check_test_script()

        for req_id in req_ids:
            if req_id in self._matrix:
                self._add_to(req_id, proto_id, proto_info)
            else:
                self._add(req_id, proto_id, proto_info)
        self.save()

    # -------------------
    ## add protocol info to a new req_id
    #
    # @param req_id       the reqid
    # @param proto_id     the protocol id
    # @param proto_info   additional protocol information
    # @return None
    def _add(self, req_id, proto_id, proto_info):
        self._matrix[req_id] = [
            {
                'proto_id': proto_id,
                'proto_info': proto_info,  # TODO what info?
            }
        ]
        self._dirty = True

    # -------------------
    ## add protocol info to an existing req_id
    #
    # @param req_id       the reqid
    # @param proto_id     the protocol id
    # @param proto_info   additional protocol information
    # @return None
    def _add_to(self, req_id, proto_id, proto_info):
        self._matrix[req_id].append(
            {
                'proto_id': proto_id,
                'proto_info': proto_info,  # TODO what info?
            }
        )
        self._dirty = True

    # -------------------
    ## save trace matrix data to storage
    #
    # @return None
    def save(self):
        services.storage.save_trace(self._matrix)
        self._dirty = False

    # === IUV only

    # -------------------
    ## (IUV only) get current dirty flag
    #
    # @return dirty flag
    def iuv_get_dirty(self):
        return self._dirty

    # -------------------
    ## (IUV only) get current trace object
    #
    # @return trace object
    def iuv_get_trace(self):
        return self._matrix
