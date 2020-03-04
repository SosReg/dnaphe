#!/bin/bash
filename='/home/dregmi/commands.txt'
while read line; 
do
$line
done < $filename
