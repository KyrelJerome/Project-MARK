#!/bin/bash



# Get current working directory of the file being run.
dir=$(dirname "$(readlink -f "$0")") # ubuntu
# dir=$(dirname "$(greadlink -f "$0")") # mac

# rm -f student_marks/*
echo "deleted old marks."

# cd "${dir}/.."
# source venv/bin/activate
# cd "${dir}"

Class_Mark_Sum=0

# Take sister directory of student_solutions
# 
for i in  $(ls "${dir}/student_solutions");do

	echo "Marking \"$i\""

	# Deleting old files.
	rm -f "$dir/state_searching/heuristics.py"
	rm -f "$dir/state_searching/search_algorithms.py"

	# copying over student(s) files to environment(Folder).
	echo "    copying over student(s) files to environment."
	if [ -e "$dir/student_solutions/$i/heuristics.py" ];then
		cp -r "${dir}/student_solutions/$i/heuristics.py" "$dir/state_searching"
	else
		# Copy blank version if it does
		cp -r "${dir}/blanks/heuristics.py" "${dir}/state_searching"
	fi

	if [ -e "$dir/student_solutions/$i/search_algorithms.py" ];then
		cp -r "${dir}/student_solutions/$i/search_algorithms.py" "$dir/state_searching"
	else
		cp -r "${dir}/blanks/search_algorithms.py" "${dir}/state_searching"
	fi

	# running tests on "search_algorithms.py".
	echo "    running tests on \"search_algorithms.py\"."
	search_algorithms_output=$(timeout 400 python3 autograder-algorithms.py 2>&1)
	mark_search_algorithms=$(echo "$search_algorithms_output" | grep "Total Grade - Algorithms:" | cut -d " " -f5)
	search_algorithms_output=$(echo "$search_algorithms_output" | grep -v "Total Grade - Algorithms:")

	# running tests on "heuristics.py".
	echo "    running tests on \"heuristics.py\"."

	cp "${dir}/perfects/search_algorithms.py" "${dir}/state_searching/"	# giving the students perfect search_algorithms.py do they don't get double penalized.

	hueristics_output=$(timeout 200 python3 autograder-hueristics.py 2>&1)
	mark_hueristics=$(echo "$hueristics_output" | grep "Total Grade - Hueristics:" | cut -d " " -f5 )
	hueristics_output=$(echo "$hueristics_output" | grep -v "Total Grade - Hueristics:")

	numerator=$(echo "$(echo $mark_hueristics | cut -d"/" -f1) + $(echo $mark_search_algorithms | cut -d"/" -f1)" | bc)
	denominator=$(echo "$(echo $mark_hueristics | cut -d"/" -f2) + $(echo $mark_search_algorithms | cut -d"/" -f2)" | bc)
	total_mark="Total Grade: $numerator/$denominator"

	# documenting student mark.
	echo "    documenting student mark."
	echo -e "$search_algorithms_output\n$hueristics_output\n\n$total_mark" > "${dir}/student_marks/$i-autograder-mark.txt"

	# For Calculating Average on the Spot
	Class_Mark_Sum=$(echo "$Class_Mark_Sum + $numerator" | bc)

	echo "    done"
done

# Setting up perfects back into the state_searching incase someone just wants to see a demo of how this stuff works.
cp "${dir}/perfects/heuristics.py" "${dir}/state_searching/"
cp "${dir}/perfects/search_algorithms.py" "${dir}/state_searching/"


# Calculating Mean, Standard Deviation, and Median
num_of_students=$(ls "${dir}/student_solutions" | wc -l)
mean=$(echo "((${Class_Mark_Sum} / ${num_of_students})/28)*100" | bc -l)
# echo "Class Average is: ${mean}"
