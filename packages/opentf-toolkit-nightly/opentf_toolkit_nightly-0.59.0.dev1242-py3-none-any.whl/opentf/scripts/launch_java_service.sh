#!/bin/bash
# Copyright (c) 2021 Henix, Henix.fr
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

function proxy_host() {
    echo "$(echo $1 | awk -F[/:] '{if ($1 ~ /^http/) print $4; else print $1}')"
}
function proxy_port() {
    echo "$(echo $1 | awk -v DEFAULT=$2 -F[/:] '{if ($1 ~ /^http/) if ($5) print $5; else print DEFAULT; else if ($2) print $2; else print DEFAULT}')"
}

DEBUG_LEVEL_ARG="${DEBUG_LEVEL:-INFO}"
BUS_HOST_ARG="${BUS_HOST:-127.0.0.1}"
BUS_PORT_ARG="${BUS_PORT:-38368}"
EXTERNAL_HOSTNAME_ARG="${EXTERNAL_HOSTNAME:-127.0.0.1}"
TRUST_FILES_ARG="${TRUST_FILES:-/}"
if [ "$DEBUG_LEVEL_ARG" == "CRITICAL" ]; then DEBUG_LEVEL_ARG="ERROR"; fi;
if [ "$DEBUG_LEVEL_ARG" == "WARNING" ]; then DEBUG_LEVEL_ARG="WARN"; fi;
if [ "$DEBUG_LEVEL_ARG" == "NOTSET" ]; then DEBUG_LEVEL_ARG="TRACE"; fi;
BASE_COMMAND="-Dorg.opentestfactory.insecure=true -Dorg.opentestfactory.auth.trustedAuthorities=$TRUST_FILES_ARG -Dorg.opentestfactory.bus.baseUrl=http://$BUS_HOST_ARG:$BUS_PORT_ARG -Dorg.opentestfactory.tf2.external-hostname=$EXTERNAL_HOSTNAME_ARG -Dlogging.level.org.squashtest.tf2=$DEBUG_LEVEL_ARG -Dlogging.level.web=$DEBUG_LEVEL_ARG -Dlogging.level.org.opentestfactory=$DEBUG_LEVEL_ARG"
if [ -z "$BUS_TOKEN" ]; then OPTIONAL_COMMAND=""; else  OPTIONAL_COMMAND="-Dorg.opentestfactory.bus.authToken=$BUS_TOKEN"; fi;

if [ -z "${NO_PROXY}" ]
then
    NOPROXY_ARG=""
else
    NOPROXY_ARG=" -Dhttp.nonProxyHosts=$(echo $NO_PROXY | sed 's/,/|/g')"
fi
if [ -z "${HTTPS_PROXY}" ]
then
    HTTPSPROXY_ARG=""
else
    HTTPSPROXY_ARG=" -Dhttps.proxyHost=$(proxy_host $HTTPS_PROXY) -Dhttps.proxyPort=$(proxy_port $HTTPS_PROXY 443)"
fi
if [ -z "${HTTP_PROXY}" ]
then
    HTTPPROXY_ARG=""
else
    HTTPPROXY_ARG=" -Dhttp.proxyHost=$(proxy_host $HTTP_PROXY) -Dhttp.proxyPort=$(proxy_port $HTTP_PROXY 80)"
fi
PROXY_COMMAND="${HTTPSPROXY_ARG}${HTTPPROXY_ARG}${NOPROXY_ARG}"

java $BASE_COMMAND $OPTIONAL_COMMAND $PROXY_COMMAND $*
