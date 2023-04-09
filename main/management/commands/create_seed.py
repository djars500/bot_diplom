from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from main.models import City, MedicalCenter, Special, Employee


class Command(BaseCommand):

    def handle(self, *args, **options):

        cities = [
            City(name='Шымкент', id=1),
            City(name='Алматы', id=2),
            City(name='Астана', id=3),
            City(name='Актау', id=4),
            City(name='Караганды', id=5),
        ]

        medical_centers = [
            MedicalCenter(name='Даумед', address='Пр.Абая 30/2', id=1),
            MedicalCenter(name='Роща', address='Пр.Абая 30/2', id=2),
            MedicalCenter(name='Городская больница', address='Пр.Абая 30/2', id=3),
            MedicalCenter(name='INVIVO', address='Пр.Абая 30/2', id=4),
            MedicalCenter(name='Айболит', address='Пр.Абая 30/2', id=5),
            MedicalCenter(name='INVIVO Алматы', address='Пр.Абая 30/2', id=6)
        ]
        City.objects.bulk_create(cities,
                                 update_conflicts=True,
                                 update_fields=['name'],
                                 unique_fields=['id'])
        MedicalCenter.objects.bulk_create(medical_centers,
                                          update_conflicts=True,
                                          update_fields=['name'],
                                          unique_fields=['id'])
        for medical_center in medical_centers:
            medical_center.city.set(cities)

        specials = [
            Special(name='Дерматолог', id=1),
            Special(name='Стоматолог', id=2),
            Special(name='Кардиолог', id=3),
            Special(name='Терапевт', id=4)
        ]

        employees = [
            Employee(fio='Усербаев Ержигит', medical_center_id=1, price=3000, id=1),
            Employee(fio='Юльчиев Азамат', medical_center_id=2, price=4000, id=2),
            Employee(fio='Толкынбаев Бекарыс', medical_center_id=3, price=5000, id=3),
            Employee(fio='Усманов Алишер', medical_center_id=4, price=6000, id=4),
            Employee(fio='Бахыт Менеев', medical_center_id=5, price=10000, id=5),
            Employee(fio='Болат Мадияр', medical_center_id=6, price=8000, id=6),
        ]

        Special.objects.bulk_create(specials,
                                    update_conflicts=True,
                                    unique_fields=['id'],
                                    update_fields=['name'])
        Employee.objects.bulk_create(employees,
                                     update_conflicts=True,
                                     unique_fields=['id'],
                                     update_fields=['fio']
                                     )
        for employee in employees:
            employee.specail.set(specials)

        try:
            User.objects.create_superuser(username='admin', email='djars500@gmail.com', password='123')
        except Exception as e:
            print('e', e)
