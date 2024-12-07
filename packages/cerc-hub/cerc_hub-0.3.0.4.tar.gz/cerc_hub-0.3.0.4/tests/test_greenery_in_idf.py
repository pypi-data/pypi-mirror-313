"""
Greenery in idf test
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""
from pathlib import Path
from unittest import TestCase

import hub.helpers.constants as cte
from hub.city_model_structure.greenery.plant import Plant
from hub.city_model_structure.greenery.soil import Soil
from hub.city_model_structure.greenery.vegetation import Vegetation
from hub.exports.energy_building_exports_factory import EnergyBuildingsExportsFactory
from hub.imports.construction_factory import ConstructionFactory
from hub.imports.geometry_factory import GeometryFactory
from hub.imports.usage_factory import UsageFactory
from hub.imports.weather_factory import WeatherFactory


class GreeneryInIdf(TestCase):
  """
  GreeneryInIdf TestCase 1
  """
  def test_greenery_in_idf(self):

    self._example_path = (Path(__file__).parent / 'tests_data').resolve()
    output_path = (Path(__file__).parent / 'tests_outputs').resolve()
    city_file = (self._example_path / "one_building_in_kelowna.gml").resolve()
    city = GeometryFactory('citygml', path=city_file).city
    for building in city.buildings:
      building.year_of_construction = 2006
    ConstructionFactory('nrel', city).enrich()
    UsageFactory('comnet', city).enrich()
    WeatherFactory('epw', city).enrich()
    vegetation_name = 'BaseEco'
    soil_thickness = 0.18
    soil_name = 'EcoRoofSoil'
    roughness = 'MediumSmooth'
    dry_conductivity = 0.4
    dry_density = 641
    dry_specific_heat = 1100
    thermal_absorptance = 0.95
    solar_absorptance = 0.8
    visible_absorptance = 0.7
    saturation_volumetric_moisture_content = 0.4
    residual_volumetric_moisture_content = 0.01
    soil = Soil(soil_name, roughness, dry_conductivity, dry_density, dry_specific_heat, thermal_absorptance,
                solar_absorptance, visible_absorptance, saturation_volumetric_moisture_content,
                residual_volumetric_moisture_content)
    soil.initial_volumetric_moisture_content = 0.2
    plant_name = 'plant'
    height = 0.5
    leaf_area_index = 5
    leaf_reflectivity = 0.2
    leaf_emissivity = 0.95
    minimal_stomatal_resistance = 180
    co2_sequestration = 0
    grows_on_soils = [soil]
    plant = Plant(plant_name, height, leaf_area_index, leaf_reflectivity, leaf_emissivity, minimal_stomatal_resistance,
                  co2_sequestration, grows_on_soils)
    plant.percentage = 1
    plants = [plant]
    vegetation = Vegetation(vegetation_name, soil, soil_thickness, plants)
    for building in city.buildings:
      for surface in building.surfaces:
        if surface.type == cte.ROOF:
          surface.vegetation = vegetation

    _idf = EnergyBuildingsExportsFactory('idf', city, output_path).export()
    self.assertIsNotNone(_idf)
    city = GeometryFactory('citygml', path=city_file).city
    for building in city.buildings:
      building.year_of_construction = 2006
    ConstructionFactory('nrel', city).enrich()
    UsageFactory('comnet', city).enrich()
    WeatherFactory('epw', city).enrich()
    _idf = EnergyBuildingsExportsFactory('idf', city, output_path).export()
    self.assertIsNotNone(_idf)
