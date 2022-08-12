#example:
#./single-ffuf http://www.baidu.com

echo "Which dict to use?"
echo "1: content-dirsearch-0.6w.txt"
echo "2: content-all-9w.txt"
echo "3: content-all-37w.txt"
read n

case $n in
 1) dict="content-dirsearch-0.6w.txt";;
 2) dict="content-all-9w.txt";;
 3) dict="content-all-37w.txt";;
 *) exit;;
esac
echo -e "\033[92mffuf -w dict/$dict -u $1/FUZZ -ac\033[0m"
ffuf -w dict/$dict -u $1/FUZZ -ac
