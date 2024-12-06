class CatalogGranulesFactory:
    UNITY = 'UNITY'

    def get_class(self, upload_type):
        if upload_type == CatalogGranulesFactory.UNITY:
            from mdps_ds_lib.stage_in_out.catalog_granules_unity import CatalogGranulesUnity
            return CatalogGranulesUnity()
        raise ValueError(f'unknown search_type: {upload_type}')
