#example:
#./batc-ffuf baidu.txt baidu

echo "ffuf quick content discovery"
mkdir $2
for i in $(cat $1); do echo -e "\033[92mffuf -w dict/content-dirsearch-0.6w.txt -u $i/FUZZ -mc 200\033[0m";ffuf -w dict/content-dirsearch-0.6w.txt -u $i/FUZZ -mc 200  -o $2/$(date +%s).csv -of csv; done &
wait
python3 sum-results.py $2/ $2/ffuf-all-ori-temp.txt
cat $2/ffuf-all-ori-temp.txt | sort | uniq  >$2/ffuf-all-ori.txt
rm $2/ffuf-all-ori-temp.txt
python3 reduplication-ffuf.py $2/ffuf-all-ori.txt $2/ffuf-all-reduplication-final.txt
# filter
cat $2/ffuf-all-reduplication-final.txt | ./bin/qsreplace -a > $2/ffuf-all-url.txt



