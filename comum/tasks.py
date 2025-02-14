import csv
from celery import shared_task
from .models import Part

@shared_task
def process_csv_upload(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:

        reader = csv.DictReader(file)
        for row in reader:
            try:

                part = Part.objects.create(
                    part_number=row['part_number'],
                    name=row['name'],
                    details=row['details'],
                    price=row['price'],
                    quantity=row['quantity']
                )
                part.save()
            except Exception as e:
                print(f"Erro ao processar linha: {row}. Erro: {e}")