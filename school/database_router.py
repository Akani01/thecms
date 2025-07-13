class CMSDatabaseRouter:
    """
    Directs universities & bursaries queries to `cms_db`, 
    and all other queries to `default`.
    """

    routed_models = {'bursary_bursary', 'college_collegeanduniversities', 'main_app_newsandevents', 'main_app_grade', 'questpaper_prospectors', 'questpaper_questionpaper'}  # Correct table names

    def db_for_read(self, model, **hints):
        """ Reads universities & bursaries from CMS_DB """
        if model._meta.db_table in self.routed_models:
            return 'cms_db'
        return 'default'

    def db_for_write(self, model, **hints):
        """ Prevent writes to CMS_DB """
        if model._meta.db_table in self.routed_models:
            return None  # No writes allowed
        return 'default'

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """ Prevent migrations for universities & bursaries in CMS_DB """
        if model_name in self.routed_models:
            return False  # Don't migrate these
        return True  # Allow migrations for other models
