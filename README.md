# Computer Crash Fix

## What it is

This is a small helper for jobs that make a computer freeze, slow down, or close unexpectedly because too much work is being done at the same time.

## What it does

You enter an estimate of the job size. The helper recommends:

- how much work to keep waiting;
- how many tasks to run at once; and
- how large each group of work should be.

The recommendations help spread out a large job so the computer is less likely to be overloaded.

The recommendations are starting points, not a guarantee that every computer can safely run a job at those settings. Never use a setting higher than the limit already provided by your app or hardware. Save important work before testing, and stop the job immediately if the computer becomes hot, unstable, or unresponsive.

## Important limitation

This tool does **not** directly repair a computer that is crashing. It only helps reduce crashes caused by an app or job doing too much work at once.

It cannot fix overheating, damaged hardware, a failing power supply, malware, or a damaged operating system. If the computer crashes when no large job is running, stop using it and have it checked by a qualified technician.

## How to apply it

1. Install Python 3 on the computer running the job.
2. Open a terminal in this project folder.
3. Run the helper with the estimated job size. For example:

	```text
	python3 crash_fix.py 2048
	```

	On Windows, use `py` instead of `python3` if needed:

	```text
	py crash_fix.py 2048
	```

4. In the app or job that is causing the problem, apply the three displayed recommendations:
	- do not keep more than the suggested number of items waiting;
	- do not run more than the suggested number of tasks at once; and
	- process work in groups no larger than the suggested size.
5. Start with the recommendations. If the computer stays stable, increase the values slowly. If it becomes unstable, lower them again.

The job or app must support these limits. This helper provides the numbers; it does not change another app automatically.

Do not use this helper as a replacement for professional hardware or operating-system troubleshooting. It is intended only for reducing the amount of simultaneous work in a workload you understand.

## How to test it as a user

### Test the helper

From the project folder, run:

```text
python3 crash_fix.py 2048
```

You should see three recommendations similar to:

```text
Keep at most 4096 items waiting
Run at most 5 tasks at once
Process work in groups of 287
```

If you see these results, the helper is working. The exact values may change only if the settings in the program are changed.

### Test the project checks

Run:

```text
python3 -m unittest -v
```

A successful test shows `OK` and reports that 4 tests ran.

### Test invalid input

Run:

```text
python3 crash_fix.py 0
```

This should show a helpful error saying that the workload must be a whole number of `1` or greater. That confirms invalid input is handled safely.

## Optional program output

To receive the recommendations in JSON format for another program, run:

```text
python3 crash_fix.py 2048 --json
```
