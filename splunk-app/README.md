To build the app into a package, simply:
   
   tar -c tippingpoint >> tippingpoint.spl

otherwise you can just copy the whole tippingpoint dir to $SPLUNK_HOME/etc/apps/

caveat, the path to the inputs might be incorrect depending on $SPLUNK_HOME,
modify tippingpoint/default/inputs.conf to the correct paths.