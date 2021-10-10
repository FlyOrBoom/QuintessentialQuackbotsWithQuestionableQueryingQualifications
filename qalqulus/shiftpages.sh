cd staging
ITER=64
find . -type f -name '*' | while read FILE ; do
	let ITER=${ITER}-1
	mv "${FILE}" "leithold-n-$ITER.jpg"
done
cd ..
