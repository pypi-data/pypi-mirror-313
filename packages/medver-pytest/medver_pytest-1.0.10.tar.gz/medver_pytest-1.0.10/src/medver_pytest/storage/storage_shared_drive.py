import glob
import os
import shutil

from .storage_file_base import StorageFileBase
from .. import services


# -------------------
## Holds storage information and how/where to save it
class StorageSharedDrive(StorageFileBase):
    # -------------------
    ## constructor
    def __init__(self):
        ## holds the path to the protocol json file
        super().__init__()

    # -------------------
    ## initialize
    #
    # @return None
    def init(self):
        # check storage_shared_path is defined
        if services.cfg.storage_shared_dir is None:
            services.abort('storage_shared_dir is None')

        # check if the dir exists
        if not os.path.isdir(services.cfg.storage_shared_dir):
            services.abort(f'storage_shared_dir does not exist: {services.cfg.storage_shared_dir}')

        services.logger.ok(f'found shared directory: {services.cfg.storage_shared_dir}')

    # -------------------
    ## terminate
    #
    # @return None
    def term(self):
        if services.cfg.report_mode:
            return

        services.logger.ok(f'publishing to shared: {services.cfg.storage_shared_dir}')
        self._save_to_shared_folder('*_trace.json')
        self._save_to_shared_folder('*_summary.json')
        self._save_to_shared_folder('*_protocol.json')

    # -------------------
    ## copy generated files to the shared directory
    #
    # @param pattern  the pattern of files to match usually json files
    # @return None
    def _save_to_shared_folder(self, pattern):
        for f in glob.glob(os.path.join(services.cfg.outdir, pattern)):
            shutil.copy2(f, services.cfg.storage_shared_dir)
