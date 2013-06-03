if [ $# -ne 1 ]
then
	echo "Usage $0 <Master Public DNS Name>"
	exit 1
fi

ssh -L 9100:localhost:9100 -L 9101:localhost:9101 hadoop@"$1"
