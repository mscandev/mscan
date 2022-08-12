import subprocess
import json
import os
import re
import time
import requests

requests.packages.urllib3.disable_warnings()


# from subprocess import PIPE,Popen


def run_popen(command):
	# 对象创建后, 主程序不会自动等待子进程完成
	# subprocess.PIPE
	# 在创建Popen对象时，subprocess.PIPE可以初始化stdin, stdout或stderr参数。表示与子进程通信的标准流
	# subprocess.STDOUT
	# 创建Popen对象时，用于初始化stderr参数，表示将错误通过标准输出流输出
	p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	while True:
		try:
			out_data = p.stdout.readline().decode("utf-8").strip('\n')
			# 如果执行结束并且从标准输出流取出的日志内容为空，则结束取值
			if not out_data and p.poll() is not None:
				break
			# 只有日志不为空才输出日志内容
			# if out_data:
			else:
				# pass
				print(str(out_data))
		except:
			continue


def reads(data):
	with open(data, 'r', encoding='utf-8') as f:
		# 将处理好的每一行组成一个列表返回
		text = f.readlines()
	return text


def save_files(file_name, data):
	with open(file_name, 'a', encoding='utf-8') as f:
		# 将处理好的每一行组成一个列表返回
		text = f.write(data)
	return text


def times():
	return time.strftime('%Y%m%d%H%M%S')


def amass():
	run_popen('bin/./amass enum -passive -df domain.txt -config config/amass.ini -o data/amass/domain.txt')


def httpx():
	run_popen('bin/./httpx -t 50 -rl 150 -fc 404 -l data/amass/domain.txt -o data/httpx/url.txt')


def POC_bomber():
	run_popen('rm -fr data/POC-bomber/poc.txt')
	run_popen('cd web/POC-bomber/ && python3 pocbomber.py -f ../../data/httpx/url.txt -o ../../data/POC-bomber/poc.txt')

def saucerframe():
	run_popen('rm -fr data/saucerframe/poc.txt')
	run_popen('cd web/saucerframe/ && python3 saucerframe.py -s all -t 300 -eG -v 2 -iF ../../data/httpx/url.txt -o ../../data/saucerframe/poc.txt')
	
def afrog():
	run_popen('rm -fr data/afrog/poc.txt')
	run_popen('bin/./afrog -silent -T data/httpx/url.txt -o ../data/afrog/result.html')


def nuclei():
	# run_popen('/data/scan/bin/./nuclei -silent -t web/nuclei-templates/ -severity low,medium,high,critical -retries 3 -rl 150 -list data/httpx/url.txt -o data/nuclei/poc.txt')
	# run_popen('/data/scan/bin/./nuclei -silent -t web/nuclei-templates/ -severity medium,high,critical -retries 3 -rl 150 -list data/httpx/url.txt -o data/nuclei/poc.txt')
	run_popen(
		'bin/./nuclei -silent -disable-update-check -t web/nuclei-templates/cves/,web/nuclei-templates/cnvd/ -severity medium,high,critical -retries 1 -rl 150 -list data/httpx/url.txt -o data/nuclei/poc.txt')


def fuzz():
	run_popen('rm -fr data/fuzz/url.log')
	url = reads('data/httpx/url.txt')
	for line in url:
		# 去掉空行,否则导致不会拼接到一行
		line = line.strip('\n')
		# print(line)
		# print('ffuf -w fuzz_wordlist.txt -mc 200 -o 1.txt -u {0}/FUZZ'.format(line))
		# run_popen('/data/scan/bin/./ffuf -w web/fuzz/dict/content-dirsearch-0.6w.txt -mc 200 -o data/fuzz/data.json -u {0}/FUZZ'.format(line))
		run_popen(
			'bin/./ffuf -t 200 -w web/fuzz/dict/content-dirsearch-0.9w.txt -ac -o data/fuzz/data.json -u {0}/FUZZ'.format(
				line))
	fuzz_data = reads('data/fuzz/data.json')
	# fuzz_data = reads('/data/scans/data.json')
	for i in fuzz_data:
		# print(i)
		i = json.loads(i)
		'''print(json.loads(i)['results'][0])
		data = json.loads(i)['results'][0]
		print(data['url'])'''
		for key in range(len(i['results'])):
			fuzz_name = i['results'][key]['input']['FUZZ']
			fuzz_url = i['results'][key]['url']
			fuzz_urls = fuzz_name + ' [+] ' + fuzz_url + '\n'
			print(fuzz_urls)
			save_files('data/fuzz/url.log', fuzz_urls)


def cdn_nslookup():
	run_popen('rm -fr data/dig/cdn.txt')
	domain = reads('data/amass/domain.txt')
	# 判断CDN
	for domains in domain:
		domains = domains.strip("\n")
		# ubuntu : apt-get install dnsutils
		result = os.popen("nslookup " + domains).read()
		results = re.findall(r'\d\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', result, re.S)
		if len(results) == 2:
			print(domains + "   没有ip地址")
		if len(results) == 3:
			print(domains + "   不存在CDN")
			print(results[-1])
		if len(results) > 3:
			print(domains + "   存在CDN")


def cdn_dig():
	run_popen('rm -fr data/dig/cdn.txt')
	domain = reads('data/amass/domain.txt')
	# 判断CDN
	for domains in domain:
		domains = domains.strip("\n")
		# print(domains)
		# ubuntu : apt-get install dnsutils
		result = os.popen("dig +noall +answer " + domains).read()
		results = re.findall(r'\d\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', result, re.S)
		# print(len(results))
		'''if len(results) > 1:
			print("[-] 存在CDN   " + domains)'''
		if len(results) == 1:
			# print("[+] 不存在CDN " + domains)
			# 只显示 ip
			# result = os.popen("dig + short " + domains).read()
			save_files('data/dig/cdn.txt', domains + '\n')


def dnsx_ip():
	run_popen('bin/./dnsx -a -resp-only -l data/dig/cdn.txt -o data/dnsx/ip.txt')


def ipcdn():
	"""cdn = reads('data/dnsx/ip.txt')
	# 判断CDN
	for domains in cdn:
		domains = domains.strip("\n")
		print(domains)"""
	run_popen('cat data/dnsx/ip.txt | bin/./qsreplace -a > data/ipcdn/ips.txt')
	run_popen('cat data/dnsx/ip.txt | bin/./ipcdn -m not > data/ipcdn/ip.txt')


def txport():
	run_popen('bin/./txport -p 1-65535 -l data/ipcdn/ip.txt -o data/txport/hosts.txt')


def xray():
	url = reads('data/httpx/url.txt')
	# 对象创建后, 主程序不会自动等待子进程完成
	# run_popen('web/xray_1.9.1/./xray webscan --listen 0.0.0.0:7777 --html-output test666.html')
	# subprocess.Popen('web/xray_1.9.1/./xray webscan --listen 0.0.0.0:7777 --html-output data/xray/{0}.html'.format(times()), shell=True, stderr=subprocess.STDOUT)
	'''p = subprocess.Popen(
		'web/xray_1.9.1/./xray webscan --listen 0.0.0.0:7777 --html-output data/xray/{0}.html'.format(times()),
		shell=True, stderr=subprocess.STDOUT)
	
	# 暂停6秒, 避免程序太早退出
	time.sleep(6)'''
	
	for urls in url:
		urls = urls.strip("\n")
		# print(urls)
		
		head = {
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:94.0) Gecko/20100101 Firefox/94.0',
			'Accept-Encoding': 'gzip, deflate, kaipule',
			'Connection': 'close'}
		
		proxies = {
			"http": "http://127.0.0.1:7777",
			"https": "http://127.0.0.1:7777"
		}
		
		try:
			url = requests.get(urls, headers=head, proxies=proxies, verify=False)
			# print(urls)
			print("[+] " + str(url.status_code) + ' ' + urls)
		except:
			continue
	# p.communicate()
	# p.kill()


def main():
	# 获取子域名
	amass()
	# 检测http状态
	httpx()
	# poc 批量检测
	POC_bomber()
	# poc 批量检测
	saucerframe()
    # poc 批量检测
	afrog()
	# poc 批量检测
	nuclei()
	# 文件泄露检测
	fuzz()
	# 检测是否存在cdn
	cdn_dig()
	# 域名转ip
	dnsx_ip()
	# 检测是否存在cdn
	ipcdn()
	# 端口扫描
	txport()
	# xray扫描器
	xray()


if __name__ == '__main__':
	print('start' + '\n')
	main()
