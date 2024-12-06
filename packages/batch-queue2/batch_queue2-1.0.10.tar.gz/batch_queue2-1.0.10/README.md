# batch_queue2

**batch_queue2** is a simple task queuing system built using Python's
`asyncio`. It allows you to submit, manage, and track tasks using a
lightweight, XML-RPC-based interface.  It's main purpose is to allow
queueing up more tasks to run on the local machine than we can support
running simultaneously; either because the number of tasks is more
than the number of CPUs or because running all those tasks
simultaneously will use too much memory.

## Features
- Submit, list, suspend, resume, and kill tasks using command-line commands.
- Tasks can be queued, paused, or resumed based on available CPUs.
- XML-RPC server for managing task requests.
- Ability to run tasks using multiple CPUs.
- Tasks can be paused and resumed.

## Requirements
- Python 3.7+
- `aiohttp`
- `requests`

## Installation
You can install **batch_queue2** from PyPI:

```sh
pip install batch_queue2
```

Or clone the repository from [Sourcehut](https://hg.sr.ht/~ndbecker2/batch_queue2/):

```sh
hg clone https://hg.sr.ht/~ndbecker2/batch_queue2
cd batch_queue2
python -m pip install .
```

## Usage

After installing, you can use the `batch_queue` command to manage tasks. Below are the available options:

### Starting the Server
To start the server:

```sh
batch_queue start --max-cpus 4
```

- `--max-cpus`: (Optional) Specify the maximum number of CPUs to use. Defaults to the number of CPUs available on your system.

The server will start in daemon mode by default.

### Submitting a Task
To submit a task, use the `submit` command:

```sh
batch_queue submit <command>
```
For example:

```sh
batch_queue submit sleep 10
```

You can also optionally specify:
- `--log-stdout <file>`: Redirect the standard output of the task to a file.
- `--log-stderr <file>`: Redirect the standard error of the task to a file.

### Listing Tasks
To list all tasks:

```sh
batch_queue list
```
This will display:
- Max CPUs available.
- Active tasks.
- Queued tasks.
- Paused tasks.
- Runnable paused tasks.

### Suspending and Resuming Tasks
To suspend task(s) (running or queued):

```sh
batch_queue suspend <task_ids>
```

To resume a paused task(s):

```sh
batch_queue resume <task_ids>
```

### Killing Task(s)
To kill specific task(s):

```sh
batch_queue kill <task_ids> <signal>
```
You can also optionally specify the signal to use, default is `SIGTERM`.

### Getting Task Information
To get detailed information about a specific task:

```sh
batch_queue id <task_id>
```
This command provides detailed information about the task including command, user, working directory, environment variables, and logs.

### Change #cpus
You can reset the max #cpus.  When you do this, if the new maximum is
greater than the number of active tasks the scheduler is recalled and
queued tasks can be started.  If the new maximum is smaller than the
number of active tasks tasks will be suspended, but marked runnable to
be continued later.

```sh
batch_queue setcpus #cpus
```

### Stopping the Server
To stop the server:

```sh
batch_queue stop
```
This command gracefully stops the server, ensuring no tasks are left in a zombie state.

## Example Workflow
1. Start the server using:
   ```sh
   batch_queue start --max-cpus 4
   ```

2. Submit a couple of tasks:
   ```sh
   batch_queue submit sleep 10
   batch_queue submit echo "Hello World"
   ```

3. List the tasks to see the active, queued, and paused tasks:
   ```sh
   batch_queue list
   ```

4. Suspend running tasks:
   ```sh
   batch_queue suspend 0
   ```

5. Resume paused tasks:
   ```sh
   batch_queue resume 0
   ```

6. Stop the server:
   ```sh
   batch_queue stop
   ```

## Logging
The server logs all activity to `~/batch_queue.log`. You can view the log to monitor task submissions, task status changes, server starts and stops, etc.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Security
The server listens on a unix domain socket normally in the user's home
directory who starts it.  Only users with access to this socket can
use it.
