import glob
import json
import os
from collections import OrderedDict

from .storage import Storage
from .. import services


# -------------------
## Holds base functions for use with file storage
class StorageFileBase(Storage):
    # -------------------
    ## constructor
    def __init__(self):
        ## holds the path to the protocol json file
        self._protocol_path = None
        ## holds the path to the trace matrix json file
        self._trace_path = None
        ## holds the path to the summary json file
        self._summary_path = None

    # -------------------
    ## (overridden) initialize
    #
    # @return None
    def init(self):
        # coverage: overridden methods not called
        pass  # pragma: no cover

    # -------------------
    ## (overridden) initialize
    #
    # @return None
    def term(self):
        # coverage: overridden methods not called
        pass  # pragma: no cover

    # -------------------
    ## save protocol information to local file
    #
    # @param protocols    the info to save
    # @return None
    def save_protocol(self, protocols):
        if services.cfg.report_mode or services.cfg.test_script is None:
            return

        self._protocol_path = os.path.join(services.cfg.outdir, f'{services.cfg.test_script}_protocol.json')
        with open(self._protocol_path, 'w', encoding='utf=8') as fp:
            json.dump(protocols, fp, ensure_ascii=True, indent=2)

    # -------------------
    ## get protocol information from local file
    #
    # @return the protocol info
    def get_protocols(self):
        protocols = {}
        for f in glob.glob(os.path.join(services.cfg.outdir, '*_protocol.json')):
            with open(f, 'r', encoding='utf=8') as fp:
                services.logger.ok(f'loading protocol file: {f}')
                curr_protos = json.load(fp)

                for proto_id, protocol in curr_protos.items():
                    if proto_id in protocols:
                        curr_loc = protocol['location']
                        prev_loc = protocols[proto_id]['location']
                        services.logger.err(f'{proto_id} protocol id is already in use:')
                        services.logger.err(f'   location: {curr_loc}')
                        services.logger.err(f'   previous: {prev_loc}')
                    else:
                        protocols[proto_id] = protocol
        return OrderedDict(sorted(protocols.items()))

    # -------------------
    ## save trace matrix information to local file
    #
    # @param trace    the info to save
    # @return None
    def save_trace(self, trace):
        if services.cfg.report_mode or services.cfg.test_script is None:
            return

        self._trace_path = os.path.join(services.cfg.outdir, f'{services.cfg.test_script}_trace.json')
        with open(self._trace_path, 'w', encoding='utf=8') as fp:
            json.dump(trace, fp, ensure_ascii=True, indent=2)

    # -------------------
    ## save trace matrix information get from the local file
    #
    # @return the trace matrix info
    def get_trace(self):
        jlist = {}
        for f in glob.glob(os.path.join(services.cfg.outdir, '*_trace.json')):
            with open(f, 'r', encoding='utf=8') as fp:
                items = json.load(fp)

                # TODO callback into trace object
                for key in items.keys():
                    if key not in jlist:
                        jlist[key] = []

                    for item in items[key]:
                        jlist[key].append(item)
        return jlist

    # -------------------
    ## save summary information to local file
    #
    # @param summary    the info to save
    # @return None
    def save_summary(self, summary):
        if services.cfg.report_mode or services.cfg.test_script is None:
            return

        self._summary_path = os.path.join(services.cfg.outdir, f'{services.cfg.test_script}_summary.json')
        with open(self._summary_path, 'w', encoding='utf=8') as fp:
            json.dump(summary, fp, ensure_ascii=True, indent=2)

    # -------------------
    ## get summary information from the local file
    #
    # @return the summary information retrieved
    def get_summary(self):
        jlist = {
            'reqids': {},
            'protoids': {},
        }
        for f in glob.glob(os.path.join(services.cfg.outdir, '*_summary.json')):
            with open(f, 'r', encoding='utf=8') as fp:
                items = json.load(fp)

                # TODO callback into summary object
                reqids = items['reqids']
                for key in reqids.keys():
                    if key in jlist['reqids']:
                        jlist['reqids'][key]['count'] += 1
                        if reqids[key]['result'] == 'FAIL':
                            jlist['reqids'][key]['result'] = 'FAIL'
                    else:
                        jlist['reqids'][key] = reqids[key]

                protoids = items['protoids']
                for key in protoids.keys():
                    if key in jlist['protoids']:
                        services.logger.err(f'{key} protocol id is already in use, skipping')
                    else:
                        jlist['protoids'][key] = protoids[key]

        return jlist
