from django.contrib.gis import admin
from django.contrib import admin as djadmin
from .models import RoadSegment, TrafficReading, Passage, Car, Sensor

# Inline para mostrar as leituras dentro do segmento no admin
class TrafficReadingInline(admin.TabularInline):
    model = TrafficReading
    extra = 0

class RoadSegmentAdmin(admin.GISModelAdmin):
    list_display = ('id', 'long_start', 'lat_start', 'long_end', 'lat_end', 'length', 'speed', 'get_intensity_display')
    inlines = [TrafficReadingInline]

    def get_intensity_display(self, obj):
        if obj.speed is None:
            return "Desconhecida"
        if obj.speed > 50:
            return "Baixa"
        elif 20 < obj.speed <= 50:
            return "Média"
        else:
            return "Elevada"
    get_intensity_display.short_description = 'Intensidade de Tráfego'

class TrafficReadingAdmin(djadmin.ModelAdmin):
    list_display = ('id', 'road_segment', 'average_speed', 'timestamp')

class PassageAdmin(djadmin.ModelAdmin):
    list_display = ('id', 'car', 'road_segment', 'sensor', 'timestamp')
    list_filter = ('timestamp', 'road_segment')
    search_fields = ('car__license_plate',)

class CarAdmin(djadmin.ModelAdmin):
    list_display = ('id', 'license_plate', 'registered_at')
    search_fields = ('license_plate',)

class SensorAdmin(djadmin.ModelAdmin):
    list_display = ('id', 'name', 'uuid')
    search_fields = ('name', 'uuid')

admin.site.register(RoadSegment, RoadSegmentAdmin)
admin.site.register(TrafficReading, TrafficReadingAdmin)
admin.site.register(Passage, PassageAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Sensor, SensorAdmin)
