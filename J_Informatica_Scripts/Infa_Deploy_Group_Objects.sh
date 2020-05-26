#!/usr/bin/bash

export USERNAME=$1
export PASSWORD=$2
export WORKSPACE=$3
Jenkins_workspace=$WORKSPACE
#Jenkins_workspace=/var/lib/jenkins/workspace/Informatica_Start_Pull_Artifcats

SRC_REP=`cat $Jenkins_workspace/Informatica_Job_config.prm | grep SRC_REP | cut -d "=" -f 2`
TGT_REP=`cat $Jenkins_workspace/Informatica_Job_config.prm | grep SRC_REP | cut -d "=" -f 2`
DOMAIN=`cat $Jenkins_workspace/Informatica_Job_config.prm | grep DOMAIN | cut -d "=" -f 2`
INFA_INTEGRATION_SERVICE=`cat $Jenkins_workspace/Informatica_Job_config.prm | grep INFA_INTEGRATION_SERVICE | cut -d "=" -f 2`
FOLDER=`cat $Jenkins_workspace/Informatica_Job_config.prm | grep FOLDER | cut -d "=" -f 2`
#WORKFLOW=`cat $Jenkins_workspace/Informatica_Job_config.prm | grep WORKFLOW | cut -d "=" -f 2`
INFA_WORKDIR=`cat $Jenkins_workspace/Informatica_Job_config.prm | grep INFA_WORKDIR | cut -d "=" -f 2`
DEPLOYMENT_GROUP_NAME=`cat $Jenkins_workspace/Informatica_Job_config.prm | grep DEPLOYMENT_GROUP_NAME | cut -d "=" -f 2`
Label_Query_Name=`cat $Jenkins_workspace/Informatica_Job_config.prm | grep Label_Query_Name | cut -d "=" -f 2`
BASH_PROFILE_FILE=`cat $Jenkins_workspace/Informatica_Job_config.prm | grep BASH_PROFILE_FILE | cut -d "=" -f 2`


LogFileDir=$INFA_WORKDIR/Logs
date=`date +'%Y-%m-%d%H%M%S'`
LogFileName=Infa_Objects_Deploy_Status_$date.log


#export Label_Query_Name=$4
#export SRC_REP=$3 
#export DOMAIN=$4
#export INFA_INTEGRATION_SERVICE=$5
#export FOLDER=$6
#export WORKFLOW=$7


cat /dev/null>$LogFileDir/$LogFileName
cd $INFA_WORKDIR
. $BASH_PROFILE_FILE 
pmrep connect -r $SRC_REP -d $DOMAIN -n $USERNAME -x $PASSWORD >>$LogFileDir/$LogFileName
RETURN_CODE=$?
if [ $RETURN_CODE == 0 ]
then 
	echo " Connected to the Repository INFA_REPO, check logs at $LogFileDir/$LogFileName "
	echo $DEPLOYMENT_GROUP_NAME  $Label_Query_Name
	
	pmrep deploydeploymentgroup -p $DEPLOYMENT_GROUP_NAME -c $Jenkins_workspace/sample_dg.xml -r $TGT_REP -n $USERNAME -s native -x $PASSWORD -d $DOMAIN -l $LogFileDir/$DEPLOYMENT_GROUP_NAME.log
	
	RETURN_CODE=$?
	echo "RETURN_CODE: "$RETURN_CODE  >>$LogFileDir/$LogFileName

	if [ $RETURN_CODE == 0 ]
	then 
	echo "Deployment of "$DEPLOYMENT_GROUP_NAME" to target Repository "$TGT_REP" was successful."
	echo 
	echo "Deployment of "$DEPLOYMENT_GROUP_NAME" to target Repository "$TGT_REP" was successful." >>$LogFileDir/$LogFileName
	date
	else
	echo "Deployment of "$DEPLOYMENT_GROUP_NAME" failed."
	echo "Deployment of "$DEPLOYMENT_GROUP_NAME" failed." >>$LogFileDir/$LogFileName
	echo "Check the log file "$LogFileDir/$LogFileName
	echo "Check the deployment log file "$LogFileDir/$DEPLOYMENT_GROUP_NAME.log
	echo
	exit 1
	fi
else
   	echo "Failed to Connect to  Repository INFA_REPO,  check logs at $LogFileDir/$LogFileName"
   	exit 1
fi


