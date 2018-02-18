from django.core.management.base import BaseCommand, CommandError
from factcoin.models import Document
import json
from tqdm import tqdm

class Command(BaseCommand):
    help = 'Read new data'

    def add_arguments(self, parser):
        parser.add_argument('file_path')

    def handle(self, *args, **options):
        lines = open(options['file_path']).read().split('\n')
        for line in tqdm(lines):
            if not line:
                continue
            json_data = json.loads(line)
            try:
                Document.add_document_from_json(json_data)
            except:
                pass
        Document.recreate_connections()
