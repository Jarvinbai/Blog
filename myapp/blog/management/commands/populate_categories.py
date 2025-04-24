from blog.models import Category
from django.core.management.base import BaseCommand



class Command(BaseCommand):
    help = "This commands inserts category data"

    def handle(self, *args, **options):

        # Delete existing data
        Category.objects.all().delete()

        categories = ['Brother','Deacon','rector','spiritual director','Formator','Priest']




        for category_name in categories:
            Category.objects.create(name = category_name)
        
        self.stdout.write(self.style.SUCCESS("Completed Inserting Data!"))


