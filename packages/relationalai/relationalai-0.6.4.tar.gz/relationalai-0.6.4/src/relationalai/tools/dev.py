import json
import sys
import time
import threading
import subprocess
from typing import cast
import click
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import os
import rich
import multiprocessing
from relationalai import metagen


from .cli_controls import divider, Spinner

#--------------------------------------------------
# Root
#--------------------------------------------------

@click.group()
def cli():
    pass

#--------------------------------------------------
# Watch
#--------------------------------------------------

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class ChangeHandler(PatternMatchingEventHandler):

    def __init__(self):
        super().__init__(patterns = ["*.py", "*.rel", "raiconfig.toml"])
        self.script = None
        self.process = None
        self.event_lock = threading.Lock()
        self.has_queued_events = False

    def check_event(self, event):
        if not event.src_path.endswith(".py"):
            return

        if "examples/" in event.src_path or "tests/end2end/test_cases/" in event.src_path:
            self.script = event.src_path

    def on_any_event(self, event):
        self.check_event(event)
        with self.event_lock:
            if self.process and self.process.poll() is None:
                # Mark that there are queued events
                self.has_queued_events = True
            else:
                self.start_process()

    def start_process(self):
        if self.script is None:
            return

        clear()
        rich.print(f"[yellow bold]{os.path.basename(self.script)}")
        rich.print("[yellow]------------------------------------------------------")
        rich.print("")

        # Start or restart the script
        self.process = subprocess.Popen(['python', self.script], shell=False)
        # Use a thread to wait for the process to finish without blocking
        wait_thread = threading.Thread(target=self.wait_and_restart_if_needed)
        wait_thread.start()

    def wait_and_restart_if_needed(self):
        if self.process is not None:
            self.process.wait()

        with self.event_lock:
            if self.has_queued_events:
                # Reset the flag and restart the process for batched events
                self.has_queued_events = False
                # Delay added to allow for potentially more events to accumulate
                # Adjust or remove the delay as needed
                time.sleep(0.5)
                self.start_process()

@cli.command()
@click.argument('directory', type=click.Path(exists=True))
def watch(directory):
    """Watch a DIRECTORY and re-run a SCRIPT on file changes."""
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=directory, recursive=True)  # Now recursive
    observer.start()

    clear()
    rich.print(f"[yellow]Watching for changes in '{directory}'.")
    rich.print("[yellow]Save a script in examples/ to run it.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

#--------------------------------------------------
# Code stats
#--------------------------------------------------

def cloc(paths):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    src_dir = os.path.join(script_dir, '..')
    core_paths = [os.path.join(src_dir, f) for f in paths]
    process = subprocess.Popen(['cloc', '--json', *core_paths], stdout=subprocess.PIPE, text=True)
    output, _ = process.communicate()

    try:
        # Parse the JSON output
        data = json.loads(output)
        # The total number of source lines is under 'SUM'/'code'
        total_lines = data['SUM']['code'] if 'SUM' in data else 0
        return cast(int, total_lines)
    except Exception as e:
        print(f"Error while parsing cloc output: {e}")
        return 0

@cli.command()
def stats():
    dsl = cloc(["dsl.py"])
    compiler = cloc(["compiler.py"])
    metamodel = cloc(["metamodel.py"])
    emitter = cloc(["rel_emitter.py"])
    rel = cloc(["rel.py"])
    metagen = cloc(["metagen.py"])
    gentest = cloc(["metagen.py"])
    tools = cloc(["tools/"])
    clients = cloc(["clients/"])
    std = cloc(["std/"])
    non_test_total = cloc(["."]) - metagen
    total = non_test_total + gentest
    core = dsl + compiler + metamodel + emitter + rel

    max_width = len(f"{total:,}")

    # Print statements with numbers right-aligned
    divider()
    rich.print(f"[yellow]RelationalAI  {non_test_total:>{max_width},} loc")
    rich.print(f"[yellow]  Core        {core:>{max_width},} loc")
    rich.print(f"[yellow]    dsl       {dsl:>{max_width},} loc")
    rich.print(f"[yellow]    rel       {rel:>{max_width},} loc")
    rich.print(f"[yellow]    emitter   {emitter:>{max_width},} loc")
    rich.print(f"[yellow]    metamodel {metamodel:>{max_width},} loc")
    rich.print(f"[yellow]    compiler  {compiler:>{max_width},} loc")
    rich.print(f"[yellow]  Clients     {clients:>{max_width},} loc")
    rich.print(f"[yellow]  Std         {std:>{max_width},} loc")
    rich.print(f"[yellow]  Tools       {tools:>{max_width},} loc")
    rich.print("")
    rich.print(f"[cyan]Gentest       {gentest:>{max_width},} loc")
    rich.print("")
    rich.print(f"[magenta]All           {total:>{max_width},} loc")
    divider()


#--------------------------------------------------
# Metagen
#--------------------------------------------------

@cli.command("gen")
@click.option('--total', default=50000, help='Total number of models to generate.')
@click.option('--threads', default=multiprocessing.cpu_count(), help='Threads to use, default is CPU count.')
@click.option('--internal', default=False, is_flag=True)
def gen(total, threads, internal):
    if not internal:
        divider()
    with Spinner(f"Testing {total:,.0f} models on {threads:,.0f} threads", f"Tested {total:,.0f} models"):
        if threads > 1:
            (elapsed, results) = metagen.batches(total, threads)
        else:
            gen = metagen.batch(total)
            results = [gen]
            elapsed = gen.elapsed

    rich.print("")

    for result in results:
        rich.print(result)

    failed = False
    for result in results:
        if len(result.failures) > 0:
            failed = True
            rich.print()
            result.print_failures(1)
            rich.print("")
            break

    rich.print("")
    rich.print(f"[yellow bold]Total time: {elapsed:,.3f}s")
    rich.print("")
    if not internal:
        divider()
        sys.exit(failed)

#--------------------------------------------------
# Metagen Watch
#--------------------------------------------------

class MetagenWatcher(PatternMatchingEventHandler):

    def __init__(self, total, threads):
        super().__init__(patterns = ["*.py"])
        self.process = None
        self.event_lock = threading.Lock()
        self.has_queued_events = False
        self.total = total
        self.threads = threads
        self.start_process()

    def on_any_event(self, event):
        with self.event_lock:
            if self.process and self.process.poll() is None:
                # Mark that there are queued events
                self.has_queued_events = True
            else:
                self.start_process()

    def start_process(self):
        clear()
        rich.print("[yellow bold]Metagen")
        rich.print("[yellow]------------------------------------------------------")
        rich.print("")

        # Start or restart the script
        self.process = subprocess.Popen(['rai-dev', 'gen', '--total', str(self.total), '--threads', str(self.threads), "--internal"], shell=False)
        # Use a thread to wait for the process to finish without blocking
        wait_thread = threading.Thread(target=self.wait_and_restart_if_needed)
        wait_thread.start()

    def wait_and_restart_if_needed(self):
        if self.process is not None:
            self.process.wait()

        with self.event_lock:
            if self.has_queued_events:
                # Reset the flag and restart the process for batched events
                self.has_queued_events = False
                # Delay added to allow for potentially more events to accumulate
                # Adjust or remove the delay as needed
                time.sleep(0.5)
                self.start_process()


@cli.command("gen:watch")
@click.argument('directory', type=click.Path(exists=True))
@click.option('--total', default=20000, help='Total number of models to generate')
@click.option('--threads', default=multiprocessing.cpu_count(), help='Threads to use')
def gen_watch(directory, total, threads):
    clear()
    event_handler = MetagenWatcher(total, threads)
    observer = Observer()
    observer.schedule(event_handler, path=directory, recursive=True)  # Now recursive
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
