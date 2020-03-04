#!/bin/bash
filename='/home/dregmi/dailyCMDS.txt'
while read line;
do
$line
done < $filename
