#!/usr/bin/bash
export USERNAME=$1
export PASSWORD=$2
export WORKSPACE=$3
WORKFLOW=''
export WORKFLOW=$4

Jenkins_workspace=$WORKSPACE


SRC_REP=`cat $Jenkins_workspace/Informatica_Job_config.prm | grep SRC_REP | cut -d "=" -f 2`
DOMAIN=`cat $Jenkins_workspace/Informatica_Job_config.prm | grep DOMAIN | cut -d "=" -f 2`
INFA_INTEGRATION_SERVICE=`cat $Jenkins_workspace/Informatica_Job_config.prm | grep INFA_INTEGRATION_SERVICE | cut -d "=" -f 2`
FOLDER=`cat $Jenkins_workspace/Informatica_Job_config.prm | grep FOLDER | cut -d "=" -f 2`
#WORKFLOW=`cat $Jenkins_workspace/Informatica_Job_config.prm | grep WORKFLOW | cut -d "=" -f 2`
INFA_WORKDIR=`cat $Jenkins_workspace/Informatica_Job_config.prm | grep INFA_WORKDIR | cut -d "=" -f 2`
BASH_PROFILE_FILE=`cat $Jenkins_workspace/Informatica_Job_config.prm | grep BASH_PROFILE_FILE | cut -d "=" -f 2`



LogFileDir=$INFA_WORKDIR/Logs
date=`date +'%Y-%m-%d%H%M%S'`
LogFileName=Infa_Jenkins_Login_$date.log

#export SRC_REP=$3 
#export DOMAIN=$4
#export INFA_INTEGRATION_SERVICE=$5
#export FOLDER=$6
#export WORKFLOW=$7
echo $SRC_REP $DOMAIN $INFA_INTEGRATION_SERVICE $FOLDER $WORKFLOW

cat /dev/null>$LogFileDir/$LogFileName
cd $INFA_WORKDIR
. $BASH_PROFILE_FILE
pmrep connect -r $SRC_REP -d $DOMAIN -n $USERNAME -x $PASSWORD >>$LogFileDir/$LogFileName
RETURN_CODE=$?
if [ $RETURN_CODE == 0 ]
then 
	echo " Connected to the Repository INFA_REPO, check logs at /data/masharma/Jenkins "
	pmcmd startworkflow -sv $INFA_INTEGRATION_SERVICE -d $DOMAIN -u $USERNAME -p $PASSWORD -f $FOLDER -wait $WORKFLOW
			if [ $? == 0 ]
			then 
				echo "Job executed, check logs at $LogFileDir/$LogFileName "
			else
				echo "Failed to EXECUTE job,  check logs at $LogFileDir/$LogFileName"
				exit 1
            fi
else
   	echo "Failed to Connect to  Repository INFA_REPO,  check logs at $LogFileDir/$LogFileName"
   	exit 1
fi