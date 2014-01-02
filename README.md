# OSG-RSV zabbix-consumer

THe RSV zabbix-consumer sends RSV metric results to Zabbix.

## Usage

1. Install the rsv-consumers-zabbix RPM.
2. Edit /etc/rsv/rsv-zabbix.conf to suite your needs.

  * *RSV_HOST* - Sets the name of the host in Zabbix that has the trapper items assigned.
  * *ZABBIX_SERVER* - The hostname or IP address of the Zabbix server.
  * *ZABBIX_TRAPPER_PORT* - The Zabbix Trapper port.  Defaults to 10051.
  * *ZABBIX_ITEM_KEY* - The item key used for the RSV metrics in Zabbix.

3. Optionally edit /etc/rsv/consumers/zabbix-consumer.conf.

  * Add `--zabbix-sender` to use zabbix_sender for sending metrics

4. Enable the zabbix-consumer

        rsv-control --enable zabbix-consumer

5. If RSV is already running you can turn on the zabbix-consumer immediately

        rsv-control --on zabbix-consumer

## Zabbix Setup

The items in Zabbix should have their keys defined using the value set for *ZABBIX_ITEM_KEY* and their parameter set to the RSV metric.

For example an item with type Zabbix trapper with key *org.osg.rsv.status[org.osg.general.ping-host]* will trap metrics for the org.osg.general.ping-host metric.

The file **zabbix_template.xml** contains an importable Zabbix template as an example of the items and triggers that can be used with this consumer.

## Compatibility

This consumer has been tested with the following versions of OSG and Zabbix.

* OSG 3 
* Zabbix 1.8.x
* Zabbix 2.0.x

## License

See LICENSE file

## Authors

See AUTHORS file

## Acknowledgements ##

* Initial code for implementing Zabbix sender in Python - https://www.zabbix.com/forum/showpost.php?p=90132&postcount=1
