from django.contrib import admin

from school_config.models import AcademicYear, Employee, Grade, GradeGroupConfig, Position, SchoolConfig, SchoolTurns, EfileConfig, Group

# Register your models here.
class SchoolTurnsAdmin(admin.ModelAdmin):
    list_display = ('id', 'turn')
    list_filter = ('turn',)
    search_fields = ('turn',)

class SchoolConfigAdmin(admin.ModelAdmin):
    list_display = ('id', 'school_name')
    list_select_related = ('turn',)
    list_filter = ('school_name',)
    search_fields = ('school_name',)

class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('id', 'init_day', 'end_day',)
    list_filter = ('init_day',)
    search_fields = ('init_day',)

class PositionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ('name', 'is_active', )
    search_fields = ('name',)

class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'name', 
        'father_lastname', 
        'mother_lastname', 
        'position'
    )
    list_filter = ('position', 'is_active')
    list_select_related = ('position', 'user', 'school',)
    search_fields = ('name',)

class EfileConfigAdmin(admin.ModelAdmin):
    list_display = ('id', 'folio', 'academic_year', 'school','current_config')
    list_filter = ('school__school_name',)
    list_select_related = ('academic_year', 'school',)
    search_fields = ('school__school_name',)

class GradeAdmin(admin.ModelAdmin):
    list_display = ('id', 'grade',)
    list_filter = ('grade',)
    search_fields = ('grade',)

class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'group',)
    list_filter = ('group',)
    search_fields = ('group',)

class GradeGroupConfigAdmin(admin.ModelAdmin):
    list_display = ('id', 'grade', 'group',)
    list_select_related = ('grade', 'group',)
    search_fields = ('grade__name', 'group__name',)


admin.site.register(SchoolTurns, SchoolTurnsAdmin)
admin.site.register(SchoolConfig, SchoolConfigAdmin)
admin.site.register(AcademicYear, AcademicYearAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(EfileConfig, EfileConfigAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(GradeGroupConfig, GradeGroupConfigAdmin)