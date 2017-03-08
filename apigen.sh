#! /bin/bash
echo "Generating Yang, tree and swagger files for uml files in ${1}"
mkdir project
cp config.txt project/
cp ${1}/*.uml project
nodejs Eagle/UmlYangTools/xmi2yang/main.js
cd project
for file in $(find . -name '*.yang'); do
  treefile=`echo ${file##*/} | sed 's/yang/tree/g'`;
  echo "Generating ${treefile} for ${file}";
  pyang -f tree -p ../Snowmass/YANG/ ${file} -o ${treefile};
  swagfile=`echo ${file##*/} | sed 's/yang/swagger/g'`;
  echo "Generating ${swagfile} for ${file}";
  pyang -f swagger -p ../Snowmass/YANG/ ${file} -o ${swagfile}
done
cd ..
mv project/*.yang ${1}
mv project/*.tree ${1}
mv project/*.swagger ${1}
rm -rf project 
