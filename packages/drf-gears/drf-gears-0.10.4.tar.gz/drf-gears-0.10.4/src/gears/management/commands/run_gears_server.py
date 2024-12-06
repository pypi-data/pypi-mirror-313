import signal
import os
from typing import Iterable

from django.core.management.commands.runserver import Command as RunServerOriginal
from django.utils.module_loading import import_string
from gears.settings import get_settings


class Command(RunServerOriginal):
    option_prefix: str = "run_gears_server_"

    def __init__(self):
        super().__init__()
        self.settings = get_settings()
        self.server_has_stopped = None

    def handle(self, *args, **options):
        # Set up signal handlers in the main thread
        signal.signal(signal.SIGINT, self.server_stop_handler)
        signal.signal(signal.SIGTERM, self.server_stop_handler)

        if options.get('use_reloader', True):
            # Check if our custom environment variable is set
            if os.environ.get("DJANGO_MAIN_PROCESS") != "True":  # main process
                os.environ["DJANGO_MAIN_PROCESS"] = "True"
                self.server_has_stopped = False
            else:  # chile process
                pass

        # Now call the super().handle which will start the server
        super().handle(*args, **options)

    def inner_run(self, *args, **options):
        self.server_start_handler()
        return super().inner_run(*args, **options)

    def server_start_handler(self, *args, **kwargs):
        tasks = self._get_tasks('up')
        self.stdout.write(
            self.style.SUCCESS(f'GEARS detected {len(tasks)} tasks to be '
                               f'run on the server`s starting up.')
        )
        self._run_tasks(tasks)

    def server_stop_handler(self, signum, frame):
        if self.server_has_stopped is False:  # never stopped before
            self.server_has_stopped = True

            tasks = self._get_tasks('down')
            self.stdout.write(
                self.style.SUCCESS(f'GEARS detected {len(tasks)} tasks to be '
                                   f'run on the server`s down.')
            )
            self._run_tasks(tasks)

        raise KeyboardInterrupt

    def _run_tasks(self, tasks: Iterable):
        for task, kw in tasks:
            self.stdout.write(self.style.SUCCESS(task))
            import_string(task)(**kw)

    def _get_tasks(self, t: str):
        # Example:
        # dict(
        #     run_gears_server_up_tasks=[
        #         # Dotted path to the function
        #         "path.to.task1",
        #     ],
        #     run_gears_server_down_tasks=[
        #         # Dotted path to the function with keyword arguments
        #         (
        #             "path.to.task2",
        #             {'a': "A", 'b': "B"},
        #         ),
        #     ],
        # )
        tasks = []
        for task in self.settings[f'{self.option_prefix}{t}_tasks']:
            kw = {}
            if isinstance(task, list) or isinstance(task, tuple):
                if len(task) != 2:
                    raise AttributeError(
                        "Run GEARS server tasks must be a set of dotted path of "
                        "functions or a set of pairs: dotted path to function "
                        "and list of kwargs."
                    )
                kw = task[1]
                task = task[0]
            tasks.append((task, kw,))
        return tasks
