#!/usr/bin/env python3
import argparse
import json
import os
from pathlib import Path
import re
import signal
import socket
import subprocess
import sys
import time
from urllib.request import urlopen
from urllib.error import URLError

ROOT = Path(__file__).resolve().parents[1]
ENV = {**os.environ, 'GRADLE_USER_HOME': str(ROOT / '.cache/gradle'),
       'npm_config_cache': str(ROOT / '.cache/npm')}


def run(args, folder):
  subprocess.run(args, cwd=ROOT / folder, env=ENV, check=True)


def doctor():
  node = subprocess.check_output(['node', '--version'], text=True).strip()
  java = subprocess.run(['java', '-version'], capture_output=True, text=True, check=True)
  if not node.startswith('v24.'):
    raise RuntimeError('Node 24 LTS가 필요합니다. nvm use를 실행하세요.')
  if not re.search(r'version "21\.', java.stderr + java.stdout):
    raise RuntimeError('JDK 21이 필요합니다. JAVA_HOME을 확인하세요.')
  print(f'환경 확인: Node {node}, Java 21', flush=True)


def servers(smoke=False):
  processes = []
  for port in (5173, 8080):
    with socket.socket() as probe:
      try:
        probe.bind(('127.0.0.1', port))
      except OSError as error:
        raise RuntimeError(f'{port} 포트 사용 중: 기존 서버를 종료하세요.') from error
  def stop(signum, frame):
    raise KeyboardInterrupt
  signal.signal(signal.SIGTERM, stop)
  try:
    for command, folder in [(['./gradlew', '--no-daemon', 'bootRun'], 'backend'),
                            (['npm', 'run', 'dev'], 'frontend')]:
      processes.append(subprocess.Popen(command, cwd=ROOT / folder, env=ENV, start_new_session=True))
    print('Frontend: http://localhost:5173 | Backend: http://localhost:8080', flush=True)
    deadline = time.monotonic() + 180
    while all(p.poll() is None for p in processes):
      if smoke:
        try:
          for port in (8080, 5173):
            with urlopen(f'http://127.0.0.1:{port}/api/health', timeout=2) as response:
              if response.status != 200 or json.load(response) != {'status': 'UP'}:
                raise RuntimeError('Health API 응답 불일치')
          with urlopen('http://127.0.0.1:5173', timeout=2) as response:
            if '<div id="root"></div>' not in response.read().decode():
              raise RuntimeError('프런트엔드 HTML 응답 불일치')
          print('HTTP 연동 통과: 백엔드 health, Vite 프록시, 프런트엔드 HTML', flush=True)
          return
        except (URLError, TimeoutError, ConnectionError):
          if time.monotonic() > deadline:
            raise RuntimeError('서버 준비 대기 시간 초과')
      time.sleep(0.5)
    raise RuntimeError('개발 서버가 종료되었습니다.')
  finally:
    for p in processes:
      try:
        os.killpg(p.pid, signal.SIGTERM)
      except ProcessLookupError:
        pass
    for p in processes:
      try:
        p.wait(timeout=10)
      except subprocess.TimeoutExpired:
        try:
          os.killpg(p.pid, signal.SIGKILL)
        except ProcessLookupError:
          pass
        p.wait()


def main():
  parser = argparse.ArgumentParser(description='프로젝트 설치·실행·검증')
  parser.add_argument('command', choices=['doctor', 'setup', 'dev', 'verify', 'smoke'])
  command = parser.parse_args().command
  doctor()
  if command == 'setup':
    run(['npm', 'ci'], 'frontend')
    run(['./gradlew', '--no-daemon', 'classes', 'testClasses'], 'backend')
  elif command == 'verify':
    run(['npm', 'run', 'lint'], 'frontend')
    run(['npm', 'run', 'build'], 'frontend')
    run(['./gradlew', '--no-daemon', 'check', 'bootJar'], 'backend')
  elif command in ('dev', 'smoke'):
    servers(command == 'smoke')


if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    sys.exit(130)
  except (RuntimeError, OSError, subprocess.CalledProcessError) as error:
    print(f'실패: {error}', file=sys.stderr)
    sys.exit(1)
