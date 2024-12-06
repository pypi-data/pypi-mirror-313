from import_export.admin import ImportExportModelAdmin


class JfkAdmin(ImportExportModelAdmin):
    save_as = True
    save_as_continue = True
    list_display = ("id",)
    list_search = ("id",)
    readonly_fields = ("id",)
