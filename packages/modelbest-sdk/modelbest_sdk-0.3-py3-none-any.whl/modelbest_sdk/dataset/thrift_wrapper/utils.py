import logging
import os
from modelbest_sdk.file_format.mbtable import MbTable
from modelbest_sdk.file_format.mbtable_builder import MbTableBuilder


class Utils:
    @staticmethod
    def load_from_file(path):
        # logging.info('Read DatasetContext from file %s', path)
        mbtable = MbTable(path)
        if mbtable.get_file_entry_count() < 1:
            raise ValueError('Empty file, please double check the content.')
        '''
        Always read the latest record. Could support version lookup in the future.
        '''
        record = mbtable.read(0)
        return record
    
    @staticmethod
    def save_to_file(path, bin):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        builder = MbTableBuilder(path)
        builder.write(bin)
        builder.flush()
        logging.info('Write DatasetInfoList to file %s', path)