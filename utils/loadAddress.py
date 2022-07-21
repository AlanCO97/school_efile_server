import os
import sys
from django.db.transaction import atomic
from dataclasses import dataclass
from io import TextIOWrapper
import json
from typing import Any, Dict

from efile.models import City, SepomexCatalog, Suburb, Town, ZipCode, State


@dataclass
class LoadAddress:
    path: str

    def load_json_file(self) -> TextIOWrapper:
        return open(file=self.path)

    def json_file_to_dict(self, file: TextIOWrapper) -> Dict[str,Any]:
        return json.load(file)

    def manipulate_dic(self, dict:Dict[str, Any]) -> None:
        address_tuple = dict.items()

        city_dict:Dict = {}
        town_dict:Dict = {}
        state_dict:Dict = {}

        porcentage = lambda n: (n * 100) / len(address_tuple)

        with atomic():
            counter: int = 0

            for key, value in address_tuple:
                os.system('cls' if os.name == 'nt' else 'clear')

                print('%.1f'%(porcentage(counter)),'%')
            
                zip_code = ZipCode.objects.create(zip_code=key)

                if value.get('ciudad'):
                    if city_dict.get(value.get('ciudad'), None) == None:
                        city = City.objects.create(name=value.get('ciudad'))
                        city_dict[value.get('ciudad')] = city.id
                    else:
                        city = City.objects.get(id=city_dict.get(value.get('ciudad')))

                if value.get('estado'):
                    if state_dict.get(value.get('estado'), None) == None:
                        state = State.objects.create(name=value.get('estado'))
                        state_dict[value.get('estado')] = state.id
                    else:
                        state = State.objects.get(id=state_dict.get(value.get('estado')))

                municipio: Dict = value.get('municipio')
                municipio_tuple = municipio.items()

                for municipio_key, municipio_value in municipio_tuple:
                    if municipio_key:
                        if town_dict.get(municipio_key, None) == None:
                            town = Town.objects.create(name=municipio_key)
                            town_dict[municipio_key] = town.id
                        else:
                            town = Town.objects.get(id=town_dict.get(municipio_key))

                    for suburb_info in municipio_value:
                        sepomex_catalog_instance = SepomexCatalog()

                        if suburb_info:
                            suburb = Suburb.objects.create(name=suburb_info)
                            
                            sepomex_catalog_instance.zip_code = zip_code
                            sepomex_catalog_instance.city = city
                            sepomex_catalog_instance.state = state
                            sepomex_catalog_instance.town = town
                            sepomex_catalog_instance.suburb = suburb
                            
                            sepomex_catalog_instance.save()
                
                counter += 1