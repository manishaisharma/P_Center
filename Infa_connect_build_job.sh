#!/usr/bin/bash

INFA_WORKDIR=/data/masharma/Jenkins/J_Informatica

LogFileDir=$INFA_WORKDIR/Logs
date=`date +'%Y-%m-%d%H%M%S'`
LogFileName=Infa_Jenkins_Login_$date.log
export USERNAME=$1
export PASSWORD=$2
export SRC_REP=$3 
export DOMAIN=$4
export INFA_INTEGRATION_SERVICE=$5
export FOLDER=$6
export WORKFLOW=$7
echo $USERNAME $PASSWORD $SRC_REP $DOMAIN $INFA_INTEGRATION_SERVICE $FOLDER $WORKFLOW

cat /dev/null>$LogFileDir/$LogFileName
cd $INFA_WORKDIR
. /data/masharma/Jenkins/J_Informatica/.bash_profile 
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