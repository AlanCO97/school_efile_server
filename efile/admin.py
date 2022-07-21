from django.contrib import admin

from efile.models import Address, BloodType, City, Efile, InsuranceHealth, RelationshipType, SepomexCatalog, State, Student, Suburb, Town, Tutor, ZipCode

# Register your models here.
class InsuranceHealthAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ('name',)
    search_fields = ('name',)

class BloodTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'blood_type')
    list_filter = ('blood_type',)
    search_fields = ('blood_type',)

class RelationshipTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'relation_name')
    list_filter = ('relation_name',)
    search_fields = ('relation_name',)

class ZipCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'zip_code')
    list_filter = ('zip_code',)
    search_fields = ('zip_code',)

class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ('name',)
    search_fields = ('name',)

class SuburbAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ('name',)
    search_fields = ('name',)

class StateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ('name',)
    search_fields = ('name',)

class TownAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ('name',)
    search_fields = ('name',)

class SepomexCatalogAdmin(admin.ModelAdmin):
    list_display = ('id', 'town', 'suburb', 'state', 'zip_code')
    list_filter = ('state',)
    search_fields = ('state__name', 'suburb__name', 'zip_code__zip_code')
    list_select_related = ('zip_code', 'suburb', 'city', 'town', 'state',)

class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'street',)
    list_filter = ('sepomex_catalog__state__name',)
    search_fields = ('sepomex_catalog__state__name', 'street',)
    list_select_related = ('sepomex_catalog',)

class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name' ,'father_lastname', 'mother_lastname',)
    list_filter = ('is_active',)
    search_fields = ('curp', 'name' ,'father_lastname', 'mother_lastname',)
    list_select_related = ('insurance_health', 'blood_type', 'who_enroll')

class TutorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name' ,'father_lastname', 'mother_lastname',)
    list_filter = ('name',)
    search_fields = ('curp', 'name' ,'father_lastname', 'mother_lastname',)
    list_select_related = ('relationship_kind', 'address',)

class EfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'student',)
    search_fields = (
        'student__curp', 
        'student__name',
        'student__father_lastname', 
        'student__mother_lastname',
    )
    list_select_related = (
        # 'school', 
        # 'academic_year',
        'efile_config',
        'student',
        'tutor_one',
        'tutor_two',
        'emergency_one',
        'emergency_two',
        'emergency_three'
    )

admin.site.register(InsuranceHealth, InsuranceHealthAdmin)
admin.site.register(BloodType, BloodTypeAdmin)
admin.site.register(RelationshipType, RelationshipTypeAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Tutor, TutorAdmin)
admin.site.register(Efile, EfileAdmin)
admin.site.register(Town, TownAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Suburb, SuburbAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(ZipCode, ZipCodeAdmin)
admin.site.register(SepomexCatalog, SepomexCatalogAdmin)

