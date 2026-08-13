#!/usr/bin/env python3

import json, os, platform, time, urllib.request

def main() -> None:
	max_retries = 5

	version = ''
	version_url = 'https://product-details.mozilla.org/1.0/firefox_versions.json'
	for attempt in range(max_retries):
		try:
			with urllib.request.urlopen(version_url, timeout=10) as response:
				version = json.load(response)['FIREFOX_ESR']
			break 
		except:
			if attempt + 1 == max_retries: raise
			time.sleep(2**(attempt + 1))

	base_url = f'https://download-installer.cdn.mozilla.net/pub/firefox/releases/{version}'

	app_path= f'linux-{platform.machine()}/en-US/firefox-{version}.tar.xz'
	langpack_path = f'linux-{platform.machine()}/xpi'
	app: tuple[str, str | None] = ('', None)
	langpacks: dict[str, str] = {}
	hashsums_url = f'{base_url}/SHA512SUMS'
	for attempt in range(max_retries):
		try:
			with urllib.request.urlopen(hashsums_url, timeout=10) as response:
				for line in response:
					[hash, path] = line.decode().strip().split('  ', 1)

					if not app[1] and path == app_path:
						app= (f'{base_url}/{path}', hash)
					elif path.startswith(langpack_path):
						langpacks[path[len(langpack_path) + 1: -4]] = hash
			break
		except:
			if attempt + 1 == max_retries: raise
			time.sleep(2**(attempt + 1))
	app_mf: list[dict[str, str | dict[str, str]]] = [{
		'type': 'archive',
		'url': app[0],
		'sha512': str(app[1]),
		'x-checker-data': {
			'type': 'rotating-url',
			'url': 'https://download.mozilla.org/?product=firefox-esr-latest&os=linux64&lang=en-US',
			'pattern': 'https://download-installer.cdn.mozilla.net/pub/firefox/releases/[0-9.]+esr/linux-x86_64/en-US/firefox-([0-9.]+esr).tar.xz',
		},
	}]
	langpacks_mf = [{
		'type': 'file',
		'url': os.path.join(base_url, langpack_path, f'{lang}.xpi'),
		'sha512': langpacks[lang],
		'dest': 'langpacks',
		'dest-filename': f'langpack-{lang}@firefox.mozilla.org.xpi',
	} for lang in langpacks]
	if not os.path.exists('generated'):
		os.mkdir('generated')
	with open('generated/firefox_esr.json', 'w') as fp:
		json.dump(app_mf, fp, indent='\t')
	with open('generated/langpacks.json', 'w') as fp:
		json.dump(langpacks_mf, fp, indent='\t')


if __name__ == '__main__':
	main()
