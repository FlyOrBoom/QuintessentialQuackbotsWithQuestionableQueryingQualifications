cd staging
find . -type f -name 'leithold-4-*' | while read FILE ; do
	n=$(echo ${FILE})
	n=${n: -7: 3}
	n=$(echo $n | sed 's/^0*//')
	n=$(($n + 312))
	mv "${FILE}" "leithold-$n.png"
done
cd ..
