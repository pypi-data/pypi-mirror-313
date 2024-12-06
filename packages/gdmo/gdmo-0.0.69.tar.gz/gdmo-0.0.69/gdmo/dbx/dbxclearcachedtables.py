class DbxClearCachedTables:
    def __new__(self, spark, cachedtables = []):
        if isinstance(cachedtables, list):
            for t in cachedtables:
                try:
                    spark.sql(f'UNCACHE TABLE IF EXISTS {t}')
                except:
                    pass
                try:
                    spark.sql(f'DROP VIEW IF EXISTS {t}')
                except:
                    pass
                print(f'Uncached {t}')