#!/usr/bin/env bash
echo "record_user,name,email,user,home"
getent passwd | egrep '^[a-z]{2}[0-9]{5}:' | while read  line
do
    user=$(echo $line | cut -f1 -d:) 
    uid=$(echo $line | cut -f3 -d:) 
    gid=$(echo $line | cut -f4 -d:) 
    name=$(echo $line | cut -f5 -d:) 
    if [[ "$name" =~ "A Really-Long-Name Surname" ]]
    then
        name="Shortname Surname"
    fi
    shell=$(echo $line | cut -f7 -d:) 
    email=$(echo $name | tr '[:upper:]' '[:lower:]' | sed 's/ /\./g')"@institute.ac.uk"
    record_user=person_$(echo $name | tr '[:upper:]' '[:lower:]' | sed 's/ /\_/g')_id
    echo "$record_user,$name,$email,$user,$home"
done 

echo "external-user,External User Name,external.user.name@gmail.com,,"


