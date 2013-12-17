#!/bin/bash

VERSION="3.7.10"
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PKG_DIR="pkg/rsv-consumers-zabbix-${VERSION}"

[ -d "SOURCES" ] || mkdir SOURCES
[ -d "SRPMS" ] || mkdir SRPMS
[ -d "RPMS" ] || mkdir RPMS
[ -d "${PKG_DIR}" ] || mkdir -p ${PKG_DIR}

cp -r etc libexec logrotate Makefile ${PKG_DIR}

cd $(dirname ${PKG_DIR})

tar czf ../SOURCES/rsv-consumers-zabbix-${VERSION}.tar.gz rsv-consumers-zabbix-${VERSION}

cd $DIR

rpmbuild -bs --define 'dist .el5' --define 'rhel 5' --define '_source_filedigest_algorithm md5' --define '_binary_filedigest_algorithm md5' ${DIR}/rsv-consumers-zabbix.spec

rpmbuild -bs --define 'dist .el6' --define 'rhel 6' --define '_source_filedigest_algorithm sha256' --define '_binary_filedigest_algorithm sha256' ${DIR}/rsv-consumers-zabbix.spec

exit 0

