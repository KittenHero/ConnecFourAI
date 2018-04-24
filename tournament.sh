#!/bin/sh

red=${1:-"python ConnectFour.py"}
yellow=${2:-"python ConnectFour.py"}
state=$(python stateio.py -n)

for i in $(seq 1 25);
do
	# loop unrolling
	move=$(timeout 1 $red $state)
	state=$(python stateio.py $state $move)
	if [ $? -eq 1 ]; then
		printf "%s %s\nred wins" "$(echo $state | tr ',' '\n')"
		break
	fi
	printf "%s %s\n" "$(echo $state | tr ',' '\n')"

	move=$(timeout 1 $yellow $state)
	state=$(python stateio.py $state $move)
	if [ $? -eq 1 ]; then
		printf "%s %s\nyellow wins" "$(echo $state | tr ',' '\n')"
		break
	fi
	printf "%s %s\n" "$(echo $state | tr ',' '\n')"
done;

printf "\n"
