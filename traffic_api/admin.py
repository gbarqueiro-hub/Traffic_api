from django.contrib.gis import admin
from .models import RoadSegment, TrafficReading  # importa seus modelos aqui

class RoadSegmentAdmin(admin.GISModelAdmin):
    list_display = ('id', 'speed', 'length') 

class RoadSegmentAdmin(admin.GISModelAdmin):
    list_display = ('id', 'long_start', 'lat_start', 'long_end', 'lat_end', 'length', 'speed')

class TrafficReadingAdmin(admin.ModelAdmin):
    list_display = ('id', 'road_segment', 'average_speed', 'timestamp')

admin.site.register(RoadSegment, RoadSegmentAdmin)
admin.site.register(TrafficReading, TrafficReadingAdmin)
