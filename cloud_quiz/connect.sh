if [ $# -ne 1 ]
then
	echo "Usage $0 <Master Public DNS Name>"
	exit 1
fi

ssh -o "ServerAliveInterval 10" hadoop@"$1"
