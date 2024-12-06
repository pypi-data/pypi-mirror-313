#!/usr/bin/env python
import socket
import subprocess
import httpx
import json
import codefast as cf
from codefast.utils import timeout
import os
import argparse
from .utils import get_system_info


class FastPing(argparse.ArgumentParser):
    def __init__(self):
        super().__init__(description='Ping a host.')
        self.add_argument('host', type=str, help='hostname or IP address')
        self.add_argument('-c', '--count', type=int, default=9,
                          help='number of packets to send')

    @property
    def os(self):
        return get_system_info()['system']

    @property
    def cmd(self):
        args = self.parse_args()
        os_name = self.os.lower()
        if 'darwin' in os_name:
            return "ping -c {} -i 0.2 -W 500 {}".format(args.count, args.host)
        elif 'linux' in os_name:
            return "ping -c {} -4 -i 0.5 -W 1 {}".format(args.count, args.host)

    def parse_ping_output(self, output):
        lines = output.decode('utf-8').split('\n')
        stats = {}

        for line in lines:
            if 'packets transmitted' in line:
                parts = line.split(',')
                stats['transmitted'] = parts[0].split()[0]
                stats['received'] = parts[1].split()[0]
                stats['packet_loss'] = parts[2].strip().split()[0]
            elif 'min/avg/max' in line:
                rtt_stats = line.split('=')[1].strip().split('/')
                stats['min'] = float(rtt_stats[0])
                stats['avg'] = float(rtt_stats[1])
                stats['max'] = float(rtt_stats[2])
                stats['mdev'] = float(rtt_stats[3].split()[0])

        return stats

    def print_stats(self, stats):
        print("\nPing Statistics:")
        print(
            f"{'Packets:':<15} {stats['transmitted']} transmitted, {stats['received']} received")
        print(f"{'Packet Loss:':<15} {stats['packet_loss']}")
        print("\nResponse Times:")
        print(f"{'Minimum:':<15} {stats['min']:.3f} ms")
        print(f"{'Average:':<15} {stats['avg']:.3f} ms")
        print(f"{'Maximum:':<15} {stats['max']:.3f} ms")
        print(f"{'Std Dev:':<15} {stats['mdev']:.3f} ms")

    @staticmethod
    def entrypoint():
        fp = FastPing()
        try:
            process = subprocess.Popen(
                fp.cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

            output_lines = []
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output.strip())
                    output_lines.append(output)

            return_code = process.poll()

            if return_code == 0:
                output = ''.join(output_lines)
                stats = fp.parse_ping_output(output.encode())
                fp.print_stats(stats)
                return True
            return False

        except Exception as e:
            print(f"Ping failed: {str(e)}")
            return False


class Cufo(object):
    @staticmethod
    def entrypoint():
        return os.system(
            "curl ipinfo.io"
        )


class ProxyCheck(argparse.ArgumentParser):
    def __init__(self):
        super().__init__(description='Check if a proxy is working.')
        self.add_argument('host', type=str, help='hostname or IP address')
        self.add_argument('port', type=int, help='port number')
        self.args = self.parse_args()

    def is_reachable(self):
        try:
            socket.gethostbyname(self.args.host)
            return True
        except socket.error:
            return False

    def is_port_open(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        try:
            sock.connect((self.args.host, self.args.port))
            sock.shutdown(socket.SHUT_RDWR)
            return True
        except:
            return False
        finally:
            sock.close()

    def is_socks5_working(self):
        proxies = {
            'http://': 'socks5://{}:{}'.format(self.args.host, self.args.port),
            'https://': 'socks5://{}:{}'.format(self.args.host, self.args.port)
        }

        @timeout(5)
        def _worker():
            with httpx.Client(proxies=proxies) as client:
                response = client.get('http://www.google.com')
                return response.status_code == 200

        try:
            return _worker()
        except Exception:
            return False

    def is_http_working(self):
        proxies = {'http://': 'http://{}:{}'.format(self.args.host, self.args.port),
                   'https://': 'http://{}:{}'.format(self.args.host, self.args.port)}
        with httpx.Client(proxies=proxies) as client:
            try:
                response = client.get('http://www.google.com')
                return response.status_code == 200
            except:
                return False

    @staticmethod
    def entrypoint():
        pc = ProxyCheck()
        msgs = [
            ("Is [HOST] reachable", pc.is_reachable),
            ("Is [PORT] open", pc.is_port_open),
            ("Is [SOCKS5] proxy working", pc.is_socks5_working),
            ("Is [HTTP] proxy working", pc.is_http_working)
        ]
        for msg, f in msgs:
            b = f()
            btext = cf.fp.green(b) if b else cf.fp.red(b)
            print(f"{msg:<{30}}: {btext}")


'''
优化这个脚本，模拟 curl 命令，支持 POST 请求，支持输出到文件。
1. 使用示例一：`jcurl http://httpbin.org/post key1=value1 key2=value2`
可能有多个 k, v 对，也可能没有，所以要动态解析参数。等同于 `
curl -X POST http://httpbin.org/post -d 'key1=value1&key2=value2'`
2. `jcurl http://httpbin.org/post key1=value1 key2=value2 -o output.png`
如果有 `-o` 参数这时候，输出到文件 output.png。
'''


class JsonCurl:
    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Simulate curl for JSON APIs with POST support.')
        parser.add_argument('url', type=str, help='URL of the API')
        parser.add_argument('data', nargs='*', type=str,
                            help='Data for POST request in key=value format')
        parser.add_argument('-o', '--output', type=str,
                            help='Output file', default=None)
        self.args = parser.parse_args()

    def post(self):
        data = {}
        if self.args.data:
            for item in self.args.data:
                key, value = item.split('=', 1)
                data[key] = value
        cf.info("data: {}".format(data))
        cf.info("url: {}".format(self.args.url))
        cmd = 'curl -s -X POST -H "Content-Type: application/json" -d \'{}\' {}'.format(
            json.dumps(data), self.args.url)
        cf.info("cmd: {}".format(cmd))

        process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
                if self.args.output:
                    with open(self.args.output, 'a') as f:
                        f.write(output)

    @staticmethod
    def entrypoint():
        JsonCurl().post()
