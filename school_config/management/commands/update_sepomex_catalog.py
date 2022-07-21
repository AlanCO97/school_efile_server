from io import TextIOWrapper
from typing import Any, Dict
from django.core.management.base import BaseCommand

from utils.loadAddress import LoadAddress

import datetime

class Command(BaseCommand):
    help = 'Update sepomex catalog'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Indicates the path of the json file')

    def handle(self, *args, **kwargs):
        start:datetime = datetime.datetime.now()
        path = kwargs['file_path']
        
        load_address = LoadAddress(path=path)
        file:TextIOWrapper = load_address.load_json_file()
        json_dic:Dict[str, Any] = load_address.json_file_to_dict(file=file)

        load_address.manipulate_dic(dict=json_dic)

        finish:datetime = datetime.datetime.now()
        self.stdout.write(
            f"The catalog its up to date. start at {str(start.time())} - finish at {str(finish.time())}"
        )