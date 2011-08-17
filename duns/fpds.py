"""Imports FPDS contract data."""


from duns.models import FPDS
from duns.importer import Importer


class FPDSImporter(Importer):
    def __init__(self, dbconn):
        Importer.__init__(self, 'contracts_contract', 
                          ('unique_transaction_id', 'id',
                           'dunsnumber', 'parentdunsnumber',
                           'vendorname', 'fiscal_year'),
                          FPDS, dbconn)

    def record(self, dbrow):
        """Transforms each raw table row into data model objects."""
        raw_vndr_name = dbrow['vendorname'].strip()
        raw_duns = dbrow['dunsnumber'].strip()
        raw_parent_duns = dbrow['parentdunsnumber'].strip()

        if len(raw_vndr_name) > 0 and (len(raw_duns) > 0 or len(raw_parent_duns) > 0):
            vndr_name = self._name(raw_vndr_name)
            duns = self._duns(raw_duns) if len(raw_duns) > 0 else None
            parent_duns = self._duns(raw_parent_duns) if len(raw_parent_duns) > 0 else None

            fpds = FPDS(data_commons_id=dbrow['id'])
            fpds.unique_transaction_id = dbrow['unique_transaction_id']
            fpds.duns = duns
            fpds.duns_parent = parent_duns
            fpds.company_name = vndr_name
            fpds.fiscal_year = dbrow['fiscal_year']
            fpds.save()
