"""
Import station related data.
"""
from eve_db.ccp_importer.importers.importer_classes import parse_char_notnull
from eve_db.models import *
from importer_classes import SQLImporter, parse_int_bool



class Importer_ramActivities(SQLImporter):
    model = RamActivity
    pks = (('id', 'activityID'),)
    field_map = (('name', 'activityName'),
                 ('icon_filename', 'iconNo'),
                 ('description', 'description'),
                 ('is_published', 'published', parse_int_bool))


class Importer_ramAssemblyLineTypes(SQLImporter):
    DEPENDENCIES = ['ramActivities']
    model = RamAssemblyLineType
    pks = (('id', 'assemblyLineTypeID'),)
    field_map = (('name', 'assemblyLineTypeName'),
                 ('base_time_multiplier', 'baseTimeMultiplier'),
                 ('description', 'description'),
                 ('base_material_multiplier', 'baseMaterialMultiplier'),
                 ('volume', 'volume'),
                 ('activity_id', 'activityID'),
                 ('min_cost_per_hour', 'minCostPerHour'))


class Importer_staOperationServices(SQLImporter):
    DEPENDENCIES = ['staOperations', 'staServices']
    model = StaOperationServices
    pks = (('operation', 'operationID'), ('service', 'serviceID'))

class Importer_ramAssemblyLineTypeDetailPerCategory(SQLImporter):
    DEPENDENCIES = ['ramAssemblyLineTypes', 'invCategories']
    model = RamAssemblyLineTypeDetailPerCategory
    pks = (('assembly_line_type', 'assemblyLineTypeID'),
           ('category', 'categoryID'))
    field_map = (('time_multiplier', 'timeMultiplier'),
                 ('material_multiplier', 'materialMultiplier'), ('cost_multiplier', 'costMultiplier'))

class Importer_ramAssemblyLineTypeDetailPerGroup(SQLImporter):
    DEPENDENCIES = ['ramAssemblyLineTypes', 'invGroups']
    model = RamAssemblyLineTypeDetailPerGroup
    pks = (('assembly_line_type', 'assemblyLineTypeID'),
           ('group', 'groupID'))
    field_map = (('time_multiplier', 'timeMultiplier'),
                 ('material_multiplier', 'materialMultiplier'), ('cost_multiplier', 'costMultiplier'))


class Importer_staServices(SQLImporter):
    model = StaService
    pks = (('id', 'serviceID'),)
    field_map = (('name', 'serviceName'),
                 ('description', 'description', parse_char_notnull))


def get_operation(operation_id):
    if operation_id:
        return StaOperation.objects.get_or_create(id=operation_id)[0]
    return None

class Importer_staStationTypes(SQLImporter):
    DEPENDENCIES = ['staOperations', 'invTypes']
    model = StaStationType
    pks = (('id', 'stationTypeID'),)
    field_map = (('dock_entry_x', 'dockEntryX'),
                 ('dock_orientation_x', 'dockOrientationX'),
                 ('dock_entry_y', 'dockEntryY'),
                 ('dock_orientation_y', 'dockOrientationY'),
                 ('dock_entry_z', 'dockEntryZ'),
                 ('dock_orientation_z', 'dockOrientationZ'),
                 ('office_slots', 'officeSlots'),
                 ('reprocessing_efficiency', 'reprocessingEfficiency'),
                 ('operation', 'operationID', get_operation),
                 ('is_conquerable', 'conquerable', parse_int_bool))


class Importer_staOperations(SQLImporter):
    DEPENDENCIES = ['staStationTypes']
    model = StaOperation
    pks = (('id', 'operationID'),)
    field_map = (('activity_id', 'activityID'),
                 ('name', 'operationName'),
                 ('description', 'description', parse_char_notnull),
                 ('fringe', 'fringe'),
                 ('corridor', 'corridor'),
                 ('hub', 'hub'),
                 ('border', 'border'),
                 ('ratio', 'ratio'),
                 ('caldari_station_type_id', 'caldariStationTypeID'),
                 ('minmatar_station_type_id', 'minmatarStationTypeID'),
                 ('amarr_station_type_id', 'amarrStationTypeID'),
                 ('gallente_station_type_id', 'gallenteStationTypeID'),
                 ('jove_station_type_id', 'joveStationTypeID'))


class Importer_ramAssemblyLineStations(SQLImporter):
    DEPENDENCIES = ['staStations', 'ramAssemblyLineTypes', 'staStationTypes',
                    'chrNPCCorporations', 'mapSolarSystems',
                    'mapRegions']
    model = RamAssemblyLineStations
    pks = (('station', 'stationID'), ('assembly_line_type', 'assemblyLineTypeID'))
    field_map = (('station_type_id', 'stationTypeID'),
                 ('owner_id', 'ownerID'),
                 ('solar_system_id', 'solarSystemID'),
                 ('region_id', 'regionID'),
                 ('quantity', 'quantity'))


#class Importer_ramTypeRequirements(SQLImporter):
#    DEPENDENCIES = ['invTypes', 'ramActivities']
#    model = RamTypeRequirement
#    pks = (('type', 'typeID'), ('activity_type', 'activityID'),
#           ('required_type', 'requiredTypeID'))
#    field_map = (('quantity', 'quantity'),
#                 ('damage_per_job', 'damagePerJob'),
#                 ('recycle', 'recycle', parse_int_bool))


class Importer_staStations(SQLImporter):
    DEPENDENCIES = ['invTypes', 'staOperations', 'staStationTypes',
                    'chrNPCCorporations', 'mapSolarSystems',
                    'mapConstellations', 'mapRegions']
    model = StaStation
    pks = (('id', 'stationID'),)
    field_map = (('security', 'security'),
                 ('docking_cost_per_volume', 'dockingCostPerVolume'),
                 ('max_ship_volume_dockable', 'maxShipVolumeDockable'),
                 ('office_rental_cost', 'officeRentalCost'),
                 ('name', 'stationName'),
                 ('x', 'x'),
                 ('y', 'y'),
                 ('z', 'z'),
                 ('reprocessing_efficiency', 'reprocessingEfficiency'),
                 ('reprocessing_stations_take', 'reprocessingStationsTake'),
                 ('reprocessing_hangar_flag', 'reprocessingHangarFlag'),
                 ('operation_id', 'operationID'),
                 ('type_id', 'stationTypeID'),
                 ('corporation_id', 'corporationID'),
                 ('solar_system_id', 'solarSystemID'),
                 ('constellation_id', 'constellationID'),
                 ('region_id', 'regionID'))

class Importer_ramInstallationTypeContents(SQLImporter):
    DEPENDENCIES = ['ramAssemblyLineTypes']
    model = RamInstallationTypeContent
    pks = (('installation_type', 'installationTypeID'), ('assembly_line_type', 'assemblyLineTypeID'),)
    field_map = (('assembly_line_type_id', 'assemblyLineTypeID'),
                 ('quantity', 'quantity'),)
