#!/usr/bin/sh
while true;do
  output="$(pytest -vv tests/test_subtopic.py)"
  if [[ $(grep -i "FAILED" <<< "$output") ]];then
    echo "$output" >> some_file_putput
    notify-send "Ja Acabou Finalmente!!"
    exit -1
  else
    echo "You Good"
 fi
done
################################################
#
# valor de pi precisao tipo 10
#                           3.2412384
# dicionario valor precisao a um valor de pi
# 10 : 3.241241235
# 12
# 13
# 14
# 15
