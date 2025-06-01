import json
from django.core.management.base import BaseCommand
from errors.models import ErrorCodeFanuc

class Command(BaseCommand):
    help = 'Import Fanuc errors from JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file')

    def handle(self, *args, **options):
        json_file = options['json_file']
        
        try:
            with open(json_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            created_count = 0
            updated_count = 0
            
            for item in data:
                if item['model'] == 'errors.errorcodefanuc':
                    fields = item['fields']
                    
                    error, created = ErrorCodeFanuc.objects.update_or_create(
                        code=fields['code'],
                        defaults={
                            'title': fields['title'],
                            'cause_en': fields['cause_en'],
                            'remedy_en': fields['remedy_en'],
                            'cause_fr': fields['cause_fr'],
                            'remedy_fr': fields['remedy_fr'],
                        }
                    )
                    
                    if created:
                        created_count += 1
                    else:
                        updated_count += 1
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully imported {created_count} new errors and updated {updated_count} existing errors'
                )
            )
            
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'File {json_file} not found')
            )
        except json.JSONDecodeError:
            self.stdout.write(
                self.style.ERROR(f'Invalid JSON in file {json_file}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error importing data: {str(e)}')
            )