#!/bin/bash

function mycurl() {
    curl -k --cert $HOME/.omf/user_cert.pem -H 'Accept: application/json' -H 'Content-Type:application/json' "$@"
}

url=https://localhost:12346/

function get() {
    mycurl -X GET -i $url/resources/users
}

get
