#!/usr/bin/bash 
#

ABCDE_SUB_TYPES='alpha bravo charlie delta echo'
NON_STD_SUB_TYPES='ACCLE AIRCRASH ALERT1 ALERT2 ALERT3 ALS AMMO ARSON BOMB C13F CARFIRE CODET DUMPFIRE ECHO ELEVATOR FFINJ FIREA FIREB FIREC FIREI GASLEAK GRASFIRE GROUND HAZ1 HAZ3 HAZ2 HAZ2I HAZPKG LIFTASST MED MEDA MEDB MEDC MEDD MEDE MEDFD MEDLE MEDOA MEDSD MUTAID NOEMD ODOR OMEGA OMEGAD PLAN REFUEL RSAlarm SERVCALL SPECDUTY STANDBY STILL SUSPART SWAT TEST WALKIN WIRES'

# NON_STD_SUB_TYPES='ACCLE|AIRCRASH|ALERT1|ALERT2|ALERT3|ALS|AMMO|ARSON|BOMB|C13F|CARFIRE|CODET|DUMPFIRE|ECHO|ELEVATOR|FFINJ|FIREA|FIREB|FIREC|FIREI|GASLEAK|GRASFIRE|GROUND|HAZ1|HAZ3|HAZ2|HAZ2I|HAZPKG|LIFTASST|MED|MEDA|MEDB|MEDC|MEDD|MEDE|MEDFD|MEDLE|MEDOA|MEDSD|MUTAID|NOEMD|ODOR|OMEGA|OMEGAD|PLAN|REFUEL|RSAlarm|SERVCALL|SPECDUTY|STANDBY|STILL|SUSPART|SWAT|TEST|WALKIN|WIRES'

ALPHA_COUNT=$(grep -i alpha 2025-08-02_emerg_data_organized_step_four.csv | wc -l)

printf "alpha records: %s\n" "$ALPHA_COUNT" 

for non_std_subtype in ${NON_STD_SUB_TYPES[@]}; do
	for abcde_subtype in ${ABCDE_SUB_TYPES[@]}; do
		printf "%s records: %s of %s type\n" "$non_std_subtype" "$(grep -i $non_std_subtype ./2025-08-02_emerg_data_organized_step_four.csv | grep -i $abcde_subtype | wc -l)" "$abcde_subtype"

	done
	# printf "%s records: %s\n" "$non_std_subtype" "$(grep -i $non_std_subtype ./2025-08-02_emerg_data_organized_step_four.csv | wc -l)"
done

#            if [ -f "$(which python2)" ] && pip2_lib_req "$pipdep"; then
#                sudo -H $PIP2_BIN install "$pipdep"
#            fi
#            if [ -f "$(which python3)" ] && pip3_lib_req "$pipdep"; then
#                sudo -H $PIP3_BIN install "$pipdep"
#            fi
#        done

LINE_SEPARATOR="------------------------------------------------"
#
printf "%s\n" "$LINE_SEPARATOR"
#
printf "Current OS: %s '%s' (%s %s %s) - %sK mem avail\n" "$SHORT_DISTRIB_DESC" "$CODE_NAME" "$(uname -o)" "$(uname -r)" "$(uname -m)" "$AVAILABLE_MEM"
#
printf "%s\n" "$LINE_SEPARATOR"

