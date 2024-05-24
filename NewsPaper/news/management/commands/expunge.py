from django.core.management.base import BaseCommand, CommandError
import news.models

class Command(BaseCommand):
    help = 'Delete all posts'

    def handle(self, *args, **options):
        self.stdout.readable()
        self.stdout.write('Do you realy wanto to delete all posts? yes/no')
        answer = input()

        if answer == 'yes':
            Posts.objects.all().delete
            self.stdout.write(self.style.SUCCESS('Succesfully wiped products!'))
            return

        self.stdout.write(self.style.ERROR('Access denied!'))
