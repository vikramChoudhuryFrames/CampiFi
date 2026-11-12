#!/bin/sh
# Maven Wrapper script
# Downloads Maven if not present and runs it

set -e

MAVEN_PROJECTBASEDIR="${MAVEN_BASEDIR:-$(cd "$(dirname "$0")" && pwd)}"
MAVEN_WRAPPER_JAR="$MAVEN_PROJECTBASEDIR/.mvn/wrapper/maven-wrapper.jar"
MAVEN_WRAPPER_PROPERTIES="$MAVEN_PROJECTBASEDIR/.mvn/wrapper/maven-wrapper.properties"

# Read distribution URL from properties
if [ -f "$MAVEN_WRAPPER_PROPERTIES" ]; then
    distributionUrl=$(grep 'distributionUrl' "$MAVEN_WRAPPER_PROPERTIES" | cut -d'=' -f2-)
fi

MAVEN_HOME="$HOME/.m2/wrapper/dists/apache-maven-3.9.6"

if [ ! -f "$MAVEN_HOME/bin/mvn" ]; then
    echo "Downloading Maven..."
    mkdir -p "$MAVEN_HOME"
    TMP_DOWNLOAD="/tmp/maven-dist.zip"
    curl -sL "$distributionUrl" -o "$TMP_DOWNLOAD"
    unzip -qo "$TMP_DOWNLOAD" -d "$HOME/.m2/wrapper/dists/"
    rm -f "$TMP_DOWNLOAD"
fi

export M2_HOME="$MAVEN_HOME"
exec "$MAVEN_HOME/bin/mvn" "$@"
