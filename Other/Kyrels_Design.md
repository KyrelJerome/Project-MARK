

File structure - stays similar:

```
root
    student_marks: Folder containing marking receipts of each student.
    student_solutions: Folder containing a folder for each student's solution.
    marking_containers: Folder containing all marking containers.
    blanks: Blank versions of each file.
    perfects: Perfect versions of each submitted file.
    assignment_template: template code to create a copy
```

TA's should create an automarker file for each assignment or question. 
Solely require test functions.
This solution may require imports or packages, so a base container must be built in all cases.

```
Requirements assessed [P0]
1. Isolated Mark single student
    - Met by utilizing Docker container generation for each assignment see a)
2. Use isolated to mark all students
    - Can be multi-threaded such that a maximum number of threads are created, with the goal of spinning
     up docker containers. Takes ~ 30 seconds maximum, closer to 10-15 seconds.
    - If not, a separate process can be created similar to that of.
3. Mark Breakdowns/ single student receipts as txt file.
    - Number of questions and headers labelled by config file. For simplicity, will use YAML.
4. All student outputs compiled (csv / excel)
    - Do not intake
5. Analytics (Mean, s.d , # perf, # failed)
    - Separate output excel file outlining this data. use python excel package.
6. Safe and hard-cleared data, with fully scrubbed student marks afterwards.
    - Docker containers can be scrubbed on deletion, as they exist simply as files themselves.
    - Use Python's os.system to call srm on the docker container.
7. One-time configurable for entire course, with strict schema definitions.
    - "marking_schema.yaml", a file outlining a marking schema in yaml form. This allows us to determine what commands must be run by the container manager for each assignment and/or file within the assignment.
        - Also denotes the amount of marks each assignment or question is worth.
```

a) How2Docker stolen from other projects 
```
# Container tag is a unique id in hex form, just used to label each user's environment
dock = docker.from_env()
dock.images.build(
            path=container_path, tag=container_tag, rm=True, network_mode=None)
dock.containers.run(container_tag, detach=True,\
            auto_remove=True, network_mode=None, cpu_count=1, mem_limit='512m')
```

b) Schema
```
assignments:
    - a1:
        similar_name_flag: True/False # Allow people to explicitly define which files to test for perfection or lack thereof.
        submission_files:
            - file1:
        marking_files:
            - file1 #
        test_files:
            - timeout_per_file_secs: timeout in seconds per file
            - test_file_1:
                prep_commands:
                    - command 1
                    - command 2
                    - command 3
                marking_commands:
                    - command 1
                    - command 2
                    - command 3
        perfect_files:
            - perf_file1
            - perf_file2
        total_worth: val_here
    - a1:
        similar_name_flag: True/False # Allow people to explicitly define which files to test for perfection or lack thereof.
        submission_files:
            - file1:
        marking_files:
            -
        test_files:
            - timeout_per_file_secs: timeout in seconds per file
            - test_file_1:
                prep_commands:
                    - command 1
                    - command 2
                    - command 3
                marking_commands:
                    - command 1
                    - command 2
                    - command 3
        perfect_files:
            - perf_file1
            - perf_file2
        total_worth: val_here
output:
    file_name: filename
    to_percents: True/False # final values to percents as QOL feature.
does_clean_flag: True/False # burn time full wiping the leftovers?
```
