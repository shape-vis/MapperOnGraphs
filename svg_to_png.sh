#!/bin/bash

echo "INFO: This script requires Imagemagick to be installed and available on the path."
echo "INFO: If you see errors, it may not be installed properly."
# mogrify -format png docs/figures/*.svg

for FSVG in docs/figures/*.svg;
do
  FPNG=${FSVG::${#FSVG}-4}".png"
  if [ ! -f "$FPNG" ]; then
    echo "Converting $FSVG to $FPNG"
    # mogrify -format png $FSVG
    inkscape --export-type="png" $FPNG -w 512 $FSVG
  fi
done

