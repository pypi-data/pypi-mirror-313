from django.core.management.base import BaseCommand
from django.core.management import CommandError
from .silica_commands.create import Command as CreateCommand
from .silica_commands.mv import Command as MvCommand
from .silica_commands.rm import Command as RmCommand

class Command(BaseCommand):
    help = 'Wrapper command for silica subcommands'

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(dest='subcommand', help='Silica subcommands')

        # Create subcommand
        create_cmd = CreateCommand()
        create_parser = subparsers.add_parser('create', help='Create command')
        create_cmd.add_arguments(create_parser)

        # Mv subcommand
        mv_cmd = MvCommand()
        mv_parser = subparsers.add_parser('mv', help='Move command')
        mv_cmd.add_arguments(mv_parser)
        
        # Rm subcommand
        rm_cmd = RmCommand()
        rm_parser = subparsers.add_parser('rm', help='Remove command')
        rm_cmd.add_arguments(rm_parser)


    def handle(self, *args, **options):
        subcommand = options['subcommand']

        if subcommand == 'create':
            cmd = CreateCommand()
        elif subcommand == 'mv':
            cmd = MvCommand()
        elif subcommand == 'rm':
            cmd = RmCommand()
        else:
            raise CommandError('Unknown subcommand "%s"' % subcommand)

        # Delegate to the appropriate command
        cmd.handle(*args, **options)
