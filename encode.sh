#!/bin/bash
# encodeBeta.sh

# Transcode .iso images into format m4v for Plex media server
#	- use DVDFab Copy to create .iso DVD5 which is then burned to disk

# This script depends on two separate command line tools:
#
#   HandBrakeCLI    http://handbrake.fr/
#
# This script depends on json file of HandBrake configuration.  See README.txt
#
# Also should make windows folder case sensitive:
#  first run following in powershell as administrator.  It enables Linux.
#     Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux
#  restart the computer
#  open cmd window as Administrator.   run the following. (not sure this is needed)
#     fsutil.exe file setCaseSensitiveInfo W:\Movies enable
#     fsutil.exe file setCaseSensitiveInfo X:\Movies enable
#
# Usage:  run in folder with HandBrakeCLI.exe and RokuAndChromecaster_5chan.json
#	cd /cygdrive/w/Movies
#   ./encode.sh [input_drive may be any typecase, e.g. 'e']
#	Will automatically eject disk when done.
#   Insert new disk when ready
#   If not done successfully will not eject and can use DVDFab or WinxDVD
#   Drive that recloses automatically will not restart.  ***But it will if you rename result.m4v file before
#	re-ejecting it!!   This is annoying but don't have good solution yet.
#
die() {
    echo -en "$0: $1" >&2
    exit ${2:-1}
}
msg() {
    echo -en "\e[33m$0: $1\e[0m" >&2
}
eject() {
	powershell "(new-object -COM Shell.Application).NameSpace(17).ParseName('$1:').InvokeVerb('Eject')"
}

# Presets generated by HandBrake gui
PRESET='RokuAndChromecaster_5chan.json'

# Minimum file size test for success
SIZE_TEST=1500000000		# bytes finished file

# Time to wait between attempts
SLEEP_TIME=30  				# sec

SOURCE_SIZE_TEST=5000000	# kbytes source disc

# User input
DRIVE="$1"
if [ ! "$DRIVE" ]; then
    die 'too few arguments.   Supply a drive let
	ter (any case)\n'
fi

# Clear screen so easy to review in progress
clear

# Main
old_dest=''
SRC=$DRIVE':/VIDEO_TS'
while [ true ]; do

	# Names of source on DVD
	NAM='';	NAM=`/usr/lib/csih/getVolInfo /cygdrive/$DRIVE 2>/dev/null | sed -n '/Volume Name/p' | cut --delimiter='<' --fields=2 | sed 's/>//'`
	VOL=''; VOL=`cmd /c vol $DRIVE: 2>/dev/null | head -1 | cut -d ' ' -f 7 | tr -d '\040\011\012\015'`
	if [ ! -z "$VOL" ]; then
		DEST=$VOL'.m4v'

		# Check for shrink need
		size_source=` du $DRIVE:/ |tail -1 | cut -f 1`
		if [ $size_source -lt $SOURCE_SIZE_TEST ]; then source_too_big=0; else source_too_big=1; fi

		# Check for over-write (simplest possible error checking) for looping when DVD tray automatically closes
		if [ -f "$DEST" ]; then
			if [ ! "$DEST" = "$old_dest" ]; then
				old_dest=$DEST
				msg "WARN($DRIVE):  $DEST already exists.  Waiting for new disk or deletion of target...\n"
				eject $DRIVE
			else
				echo -en "."
			fi
		else
			clear

			# Catch DVD9 disk and force DVDfab copy to DVD5 if $source_too_big
			if [ $source_too_big -eq 0 ]; then
				echo -en "\e[102m\e[30m\e[1mMESSAGE($0):  $DEST / $VOL source DVD5 ($size_source vs $SOURCE_SIZE_TEST limit for DVD5).  OK.\e[0m\n"

				# Run HandBrake
				./jobStat.sh "  \e[102m\e[30m\e[1m--- $DRIVE: $VOL :$DRIVE ---\e[0m\n" &
				stat_id=$!
				echo "spawned $stat_id"
				trap "kill $stat_id 2>/dev/null; echo killed $stat_id" EXIT
				sleep 2  # To allow stdout of HandBrakeCLI to start
				echo running ./HandBrakeCLI --main_feature --preset-import-file $PRESET -i $SRC -o $DEST
				./HandBrakeCLI --main-feature --preset-import-file $PRESET -i $SRC -o $DEST
				handbrake_failure=$?
	#	touch $DEST # for testing, uncomment this line and comment the one above this line
			else
				msg "ERROR($0):  $DEST / $NAM source too big ($size_source vs $SOURCE_SIZE_TEST limit for DVD5).   We need to start with DVD5 size.\n"
				handbrake_failure=1
			fi

			# Check result
			LS_RESULT=`ls -la $DEST 2>/dev/null`; ls_failure=$?
			if [ $ls_failure -eq 0 ]; then
				SIZE=`echo $LS_RESULT | awk '{print $5}'`
				if [ $SIZE -lt $SIZE_TEST ]; then size_test_failure=1; else	size_test_failure=0; fi
			else
				size_test_failure=1
			fi

			# Take action
			if [ $handbrake_failure -eq 0 ] &&  [ $size_test_failure -eq 0 ] &&  [ $ls_failure -eq 0 ]; then
				echo -en "\e[92m\e[1m$DEST: SUCCESS\e[0m\n"  # Light Green, bold
			else
				if [ $source_too_big -eq 1 ]; then
					echo -en "\e[31m\e[1m\n$DEST:  source_too_big = $source_too_big.   Start DVDfab and rip it\e[0m\n\n"
				else
					echo -en "\e[31m\e[1m$DEST:\nhandbrake_failure     ls_failure      size_test_failure   source_too_big\n       $handbrake_failure                   $ls_failure                  $size_test_failure               $source_too_big\e[0m\n"
				fi
			fi
			kill $stat_id 2>/dev/null
			if [ $handbrake_failure -eq 0 ] &&  [ $size_test_failure -eq 0 ]; then
				eject $DRIVE
				printf '\7'
			else
				msg "\nWARN($DRIVE):  original DVD being used (rip it) or else Lionsgate (use WinxDVD). Look at $VOL in explorer to make decision.  Leaving disk ready in drive for that.\n\nPress any key when done ripping externally and ready to continue with checking with a new disk..."
				while [ true ] ; do
					read -t 3 -n 1
					if [ $? = 0 ] ; then
					echo ""
						continue 2;
					else
						echo -en "."
					fi
				done
			fi

			msg "\n\nMSG($DRIVE): Movie $NAM \n\nInsert a new disk...\n"
		fi
	fi
	# Skips to here if drive not available, due to $? test on info
	sleep $SLEEP_TIME
done