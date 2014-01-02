prefix := /usr
localstatedir := /var
sysconfdir := /etc
libexecdir := $(prefix)/libexec
datadir := $(prefix)/share


_default:
	@echo "No default. Try 'make install'"

install:
	# Install executables
	install -d $(DESTDIR)/$(libexecdir)/rsv/consumers
	cp -f libexec/consumers/zabbix-consumer $(DESTDIR)/$(libexecdir)/rsv/consumers/
	# Install configuration
	install -d $(DESTDIR)/$(sysconfdir)/rsv/meta/consumers
	cp -f etc/meta/consumers/zabbix-consumer.meta $(DESTDIR)/$(sysconfdir)/rsv/meta/consumers/
	install -d $(DESTDIR)/$(sysconfdir)/rsv/consumers
	cp -f etc/consumers/zabbix-consumer.conf $(DESTDIR)/$(sysconfdir)/rsv/consumers/
	cp -f etc/rsv-zabbix.conf $(DESTDIR)/$(sysconfdir)/rsv/
	# Create the log dir
	install -d $(DESTDIR)/$(localstatedir)/log/rsv/consumers
	# Put log rotation in place
	install -d $(DESTDIR)/$(sysconfdir)/logrotate.d
	install -m 0644 logrotate/rsv-consumers-zabbix.logrotate $(DESTDIR)/$(sysconfdir)/logrotate.d/rsv-consumers-zabbix

.PHONY: _default install
