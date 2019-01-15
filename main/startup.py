from django.core.management import call_command


def start_up_commands():
    """
    upon server startup, makes migrations
    """
    # call_command('makemigrations', interactive=True)
    # call_command('migrate', interactive=True)
