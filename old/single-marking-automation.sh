#!/bin/bash

# dir=$(dirname "$(readlink -f "$0")") # ubuntu
dir=$(dirname "$(greadlink -f "$0")") # mac


# Making sure a parameter is passed in.
if [ -z $1 ]; then
	echo "you need to pass a utorid/groupid as the parameter."
	exit 1
fi

student="$1"

# Checking to see if the utorid/groupid directory exists in the handed in assignments.
if [ ! -d "${dir}/student_solutions/$student" ]; then
	echo "student utorid does not exist."
	exit 1
fi


# Deleting old text file.
echo "deleted old mark."
rm -f "${dir}/student_marks/$student-autograder-mark.txt"

# cd "${dir}/.."
# source venv/bin/activate
# cd "${dir}"

echo "Marking \"$student\""

# Deleting any potential lingering old files from the state_searching directory.
rm -f "$dir/state_searching/heuristics.py"
rm -f "$dir/state_searching/search_algorithms.py"

# Copying over solution files to state_searching.
echo "    copying over student's files to the environment."
if [ -e "$dir/student_solutions/$student/heuristics.py" ];then
	cp -r "${dir}/student_solutions/$student/heuristics.py" "$dir/state_searching"
else
	cp -r "${dir}/blanks/heuristics.py" "${dir}/state_searching"
	echo "    Warning: blank heuristics file was given since student had no heuristic file of own"
fi

if [ -e "$dir/student_solutions/$student/search_algorithms.py" ];then
	cp -r "${dir}/student_solutions/$student/search_algorithms.py" "$dir/state_searching"
else
	cp -r "${dir}/blanks/search_algorithms.py" "${dir}/state_searching"
	echo "    Warning: blank search_algorithms file was given since student had no search_algorithms file of own"

fi

# The testing was seperated since there could come a case where a group/student might have failed to code a* algorithm but was successful in coding the hueristics.

# Running search_algorithms.py tests
echo "    running tests on \"search_algorithms.py\"."
search_algorithms_output=$(timeout 400 python3 autograder-algorithms.py 2>&1)
mark_search_algorithms=$(echo "$search_algorithms_output" | grep "Total Grade - Algorithms:" | cut -d " " -f5)
search_algorithms_output=$(echo "$search_algorithms_output" | grep -v "Total Grade - Algorithms:")

# Running heuristics.py tests, but first making sure they have the correct search_algorithms.py.
echo "    running tests on \"heuristics.py\"."
cp "${dir}/perfects/search_algorithms.py" "${dir}/state_searching/"
hueristics_output=$(timeout 200 python3 autograder-hueristics.py 2>&1)
mark_hueristics=$(echo "$hueristics_output" | grep "Total Grade - Hueristics:" | cut -d " " -f5 )
hueristics_output=$(echo "$hueristics_output" | grep -v "Total Grade - Hueristics:")

# Getting student A1 final mark by adding up the two marks recieved from the two autograders.
total_mark="Total Grade: $(echo "$(echo $mark_hueristics | cut -d"/" -f1) + $(echo $mark_search_algorithms | cut -d"/" -f1)" | bc -l)/$(echo "$(echo $mark_hueristics | cut -d"/" -f2) + $(echo $mark_search_algorithms | cut -d"/" -f2)" | bc -l)"

# Documenting solution mark in designated text file.
echo "    documenting student mark."
echo -e "$search_algorithms_output\n$hueristics_output\n\n$total_mark" > "${dir}/student_marks/$student-autograder-mark.txt"

echo "    done"

# deactivate

# Copying over original stock solution files. (Take out)
cp "${dir}/perfects/search_algorithms.py" "${dir}/state_searching/"
cp "${dir}/perfects/heuristics.py" "${dir}/state_searching/"
