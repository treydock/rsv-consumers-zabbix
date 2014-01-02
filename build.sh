#!/bin/bash

# User defined variables
VERSION="0.0.1"
RELEASE="1"

# Script constants
NAME="rsv-consumers-zabbix"
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PKG_DIR="pkg/rsv-consumers-zabbix-${VERSION}"

# Default variables that have command line flags
QUIET=1
DEBUG=0
TRACE=0
MOCK=0

usage () {

cat << EOF
usage: $(basename $0) [OPTIONS]

This script builds RPMs for $NAME.

OPTIONS:

  --mock          Run mock rebuild of SRPMs
  --debug         Show debug output
                  This option also removes the mock --quiet option.
  --trace         Show the mock debug output
  -h, --help      Show this message

EXAMPLE:

Build SRPMs

$(basename $0)

Build SRPMs and run mock rebuild

$(basename $0) --mock

EOF
}

ARGS=`getopt -o h -l mock,help,debug,trace -n "$0" -- "$@"`

[ $? -ne 0 ] && { usage; exit 1; }

eval set -- "${ARGS}"

while true; do
  case "$1" in
    -h|--help)
      usage
      exit 0
      ;;
    --mock)
      MOCK=1
      shift
      ;;
    --debug)
      DEBUG=1
      QUIET=0
      shift
      ;;
    --trace)
      TRACE=1
      shift
      ;;
    --)
      shift
      break
      ;;
    *)
      break
      ;;
  esac
done

exec_cmd() {
  cmd="$1"

  echo "Executing: ${cmd}"
  eval $cmd
}

# Set variables based on command line flags
[ $DEBUG -eq 1 ] && set -x
[ $TRACE -eq 1 ] && mock_trace="--trace" || mock_trace=""
[ $QUIET -eq 1 ] && mock_quiet="--quiet" || mock_quiet=""

# Build necessary directories if they do not exist
[ -d "SOURCES" ] || mkdir SOURCES
[ -d "SRPMS" ] || mkdir SRPMS
[ -d "RPMS" ] || mkdir RPMS

# Clean and create PKG directory for copying files for tar
[ -d "${PKG_DIR}" ] && rm -rf ${PKG_DIR}
mkdir -p ${PKG_DIR}

# Copy all packaged files to temporary directory for tar
cp -r etc libexec logrotate Makefile README.md AUTHORS LICENSE zabbix_template.xml ${PKG_DIR}

cd $(dirname ${PKG_DIR})

# Create tarball for rpmbuild
tar czf ../SOURCES/rsv-consumers-zabbix-${VERSION}.tar.gz rsv-consumers-zabbix-${VERSION}

cd $DIR

# build SRPMs
rpmbuild -bs --define 'dist .el5' --define 'rhel 5' --define '_source_filedigest_algorithm md5' --define '_binary_filedigest_algorithm md5' ${DIR}/rsv-consumers-zabbix.spec
rpmbuild -bs --define 'dist .el6' --define 'rhel 6' --define '_source_filedigest_algorithm sha256' --define '_binary_filedigest_algorithm sha256' ${DIR}/rsv-consumers-zabbix.spec

# if --mock was passed, run mock rebuild
if [ $MOCK -eq 1 ]; then
  # Build EL5
  exec_cmd "mock -r epel-5-x86_64 ${mock_quiet} ${mock_trace} --define 'dist .el5' --resultdir=${DIR}/RPMS --rebuild ${DIR}/SRPMS/${NAME}-${VERSION}-${RELEASE}.el5.src.rpm"

  # Build EL6
  exec_cmd "mock -r epel-6-x86_64 ${mock_quiet} ${mock_trace} --define 'dist .el6' --resultdir=${DIR}/RPMS --rebuild ${DIR}/SRPMS/${NAME}-${VERSION}-${RELEASE}.el6.src.rpm"
fi

exit 0
