from json import dumps, loads
from pathlib import Path
from random import choice
from re import Match, compile, search
from tempfile import gettempdir
from urllib.parse import urlparse

from httpx import Client


class FakeUserAgentError(Exception):
    pass


def fetch_latest_chrome_version():
    url = 'https://chromiumdash.appspot.com/fetch_milestone_schedule?offset=1&n=1'
    with Client(timeout=15, verify=False, follow_redirects=True) as client:
        response = client.get(url)
        response.raise_for_status()
        data = response.json()

        mstones = data.get("mstones", [])
        if mstones:
            mstone_version = mstones[0].get('mstone')
            return float(mstone_version)
        else:
            return None


def is_writable_directory(path: str | Path) -> bool:
    directory = Path(path)
    if not directory.is_dir():
        return False
    try:
        test_file = directory / '.write_test'
        test_file.touch(exist_ok=False)
        test_file.unlink()
        return True
    except Exception:
        return False


def get_path_for_data() -> Path:
    fallback_file = Path(__file__).parent.resolve() / 'browsers.json'
    temp_file = Path(gettempdir()).resolve() / 'browsers.json'
    if is_writable_directory(Path(__file__).parent):
        data_path = fallback_file
    else:
        temp_file.touch(mode=0o777, exist_ok=True)
        temp_file.write_text(fallback_file.read_text())
        data_path = temp_file
    return data_path


def increment_version_in_useragent(useragent, increment):
    version_pattern = compile(r'(Version/|Edg(?:e|iOS|A)?/|Firefox/|Chrome/|CriOS/|Safari/|OP(?:TX|X)/|RD(?:Documents|Web)/)(\d+\.\d+(?:\.\d+)?(?:\.\d+)?)')

    def replace_version(match: Match) -> str:
        prefix, version = match.groups()
        version_parts = version.split('.')
        new_version = '.'.join([str(float(part) + increment if index == 0 else part) for index, part in enumerate(version_parts)])
        new_version_parts = new_version.split('.')
        if len(new_version_parts) > 2 and new_version_parts[1] == '0':
            new_version_parts.pop(1)
            new_version = '.'.join(new_version_parts)
        return f'{prefix}{new_version}'

    new_useragent = version_pattern.sub(replace_version, useragent)
    return new_useragent


def actualize_browsers_version(input_file_path: Path, output_file_path: Path | None = None) -> str:
    if not input_file_path.exists():
        return ''
    with open(input_file_path, 'r') as input_file:
            lines = input_file.readlines()
    try:
        latest_chrome_version = fetch_latest_chrome_version()
        max_version = 0
        for line in lines:
            data = loads(line.strip())
            if 'version' in data:
                try:
                    version = float(data['version'])
                    if version > max_version:
                        max_version = version
                except ValueError:
                    pass
        if latest_chrome_version is not None:
            increment_value = latest_chrome_version - max_version
        else:
            increment_value = 0
        updated_lines = ''
        with open(output_file_path or input_file_path, 'w') as output_file:
            for line in lines:
                data = loads(line.strip())
                if 'version' in data:
                    try:
                        old_version = int(data['version'])
                        new_version = (old_version + increment_value) if old_version > 100 else (old_version + 1.0)
                        data['version'] = new_version
                    except ValueError:
                        continue
                if 'useragent' in data:
                    data['useragent'] = increment_version_in_useragent(data['useragent'], increment_value)
                fresh_data = dumps(data) + '\n'
                output_file.write(fresh_data)
                updated_lines += fresh_data
        return fresh_data
    except Exception as exc:
        print('actualize_browsers_version:', exc)
        return input_file_path.read_text()


UserAgentError = FakeUserAgentError
BROWSER_DATA_URL = 'https://github.com/fake-useragent/fake-useragent/raw/refs/heads/main/src/fake_useragent/data/browsers.json'
BROWSERS_DATA = get_path_for_data()
FALLBACK_UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
FALLBACK_UA_DICT = {'useragent': FALLBACK_UA, 'system': 'Chrome 131.0 Win10', 'browser': 'chrome', 'version': 131.0, 'os': 'win10', }
REPLACEMENTS = {' ': '', '_': ''}
OS_REPLACEMENTS = {'windows': ['win10', 'win7']}
SHORTCUTS = {'microsoft edge': 'edge', 'google': 'chrome', 'googlechrome': 'chrome', 'ff': 'firefox'}
BROWSERS_NAMES = ['chrome', 'edge', 'firefox', 'safari']
OS_NAMES = ['windows', 'macos', 'linux', 'android', 'ios']
PLATFORMS = ['pc', 'mobile', 'tablet']


def get_browsers_data(url: str) -> str:
    try:
        with Client(timeout=15, verify=False, follow_redirects=True) as client:
            return client.get(url).text
    except Exception as exc:
        print('get_browsers_data:', url, exc)
        return ''


def load_browsers_data(browsers_data: Path) -> list[dict]:
    if not browsers_data.exists():
        new_browsers_data = get_browsers_data(BROWSER_DATA_URL)
        if not new_browsers_data:
            raise FakeUserAgentError('не удалось загрузить данные с сервера', new_browsers_data)
        browsers_data.write_text(new_browsers_data)
        data = [loads(line) for line in actualize_browsers_version(browsers_data).splitlines()]
    else:
        try:
            json_lines = browsers_data.read_text()
            data = [loads(line) for line in json_lines.splitlines()]
        except Exception as exc:
            print('load_browsers_data:', browsers_data, exc)
            data = []
    if not data:
        raise FakeUserAgentError('список данных пуст', data)
    if not isinstance(data, list):
        raise FakeUserAgentError('данные — это не список', data)
    return data


class FakeUserAgent:
    def __init__(self,
                 browsers: list[str] | str = BROWSERS_NAMES,
                 os: list[str] | str = OS_NAMES,
                 min_version: float = 0.0, min_percentage: float = 0.0,
                 platforms: list[str] | str = PLATFORMS, fallback: str = FALLBACK_UA,
                 safe_attrs: list[str] | set[str] | tuple[str, ...] = (), ):
        self.browsers = self._ensure_list(browsers)
        self.os = self._expand_os(self._ensure_list(os))
        self.min_version = float(min_version)
        self.min_percentage = float(min_percentage)
        self.platforms = self._ensure_list(platforms)
        self.fallback = fallback
        self.safe_attrs = set(safe_attrs)
        self.data_browsers = load_browsers_data(BROWSERS_DATA)

    @staticmethod
    def _ensure_list(value: list[str] | str) -> list[str]:
        return value if isinstance(value, list) else [value]

    @staticmethod
    def _expand_os(os_list: list[str]) -> list[str]:
        expanded_os = []
        for os_name in os_list:
            expanded_os.extend(OS_REPLACEMENTS.get(os_name, [os_name]))
        return expanded_os

    def _filter_useragents(self, request: str | None = None) -> list[dict]:
        filtered_useragents = [ua for ua in self.data_browsers if ua['browser'] in self.browsers and ua['os'] in self.os and ua['type'] in self.platforms and ua['version'] >= self.min_version and ua['percent'] >= self.min_percentage]
        if request:
            filtered_useragents = [ua for ua in filtered_useragents if ua['browser'] == request]
        return filtered_useragents

    def get_browser(self, request: str) -> dict:
        try:
            request = self._normalize_request(request)
            filtered_browsers = self._filter_useragents(request if request != 'random' else None)
            return choice(filtered_browsers)
        except (KeyError, IndexError):
            if self.fallback:
                return FALLBACK_UA_DICT
            raise FakeUserAgentError(f'ошибка при получении браузера: {request}')

    @staticmethod
    def _normalize_request(request: str) -> str:
        for value, replacement in REPLACEMENTS.items():
            request = request.replace(value, replacement)
        return SHORTCUTS.get(request.lower(), request.lower())

    def __getitem__(self, attr: str) -> str:
        return self.__getattr__(attr)

    def __getattr__(self, attr: str) -> str:
        if attr in self.safe_attrs:
            return super().__getattribute__(attr)
        try:
            attr = self._normalize_request(attr)
            filtered_browsers = self._filter_useragents(attr if attr != 'random' else None)
            return choice(filtered_browsers).get('useragent')
        except (KeyError, IndexError):
            if self.fallback:
                return self.fallback
            raise FakeUserAgentError(f'ошибка при получении браузера: {attr}')

    @property
    def chrome(self) -> str:
        return self.__getattr__('chrome')

    @property
    def googlechrome(self) -> str:
        return self.chrome

    @property
    def edge(self) -> str:
        return self.__getattr__('edge')

    @property
    def firefox(self) -> str:
        return self.__getattr__('firefox')

    @property
    def ff(self) -> str:
        return self.firefox

    @property
    def safari(self) -> str:
        return self.__getattr__('safari')

    @property
    def random(self) -> str:
        return self.__getattr__('random')

    @property
    def get_firefox(self) -> dict:
        return self.get_browser('firefox')

    @property
    def get_chrome(self) -> dict:
        return self.get_browser('chrome')

    @property
    def get_edge(self) -> dict:
        return self.get_browser('edge')

    @property
    def get_safari(self) -> dict:
        return self.get_browser('safari')

    @property
    def get_random(self) -> dict:
        return self.get_browser('random')


UserAgent = FakeUserAgent


def extract_browser_info(user_agent):
    major_version_match = search(r'(?:Chrome|Firefox|Safari)/(\d+)', user_agent)
    major_version = major_version_match.group(1) if major_version_match else None

    platform_match = search(r'\(([^;]+)', user_agent)
    platform = platform_match.group(1).split()[0] if platform_match else None
    platform = platform if platform.lower() in ['macintosh', 'windows', 'linux', 'android', 'iphone', 'ipad'] else 'Linux'

    branded_name_match = search(r'Safari/\d+\.\d+\s+(\w+)/', user_agent)
    if branded_name_match:
        branded_name = branded_name_match.group(1)
    else:
        branded_name_match = search(r'(Chrome|Firefox|Safari)/\d+', user_agent)
        branded_name = branded_name_match.group(1) if branded_name_match else 'Safari'

    branded_name = branded_name.replace('Edg', 'Edge') if branded_name else ''

    return {
        'major_version': major_version,
        'platform': platform,
        'branded_name': branded_name
    }


def random_headers(url: str | None = None, lowercase: bool = False) -> dict:
    if not url:
        fallback_url = 'https://google.com'
    else:
        fallback_url = None
    parsed_url = urlparse(url or fallback_url)
    referer = f'{parsed_url.scheme}://{parsed_url.netloc}'
    useragent = UserAgent().random
    browser_info = extract_browser_info(useragent)
    major_version = browser_info['major_version']
    platform = browser_info['platform']
    is_mobile = '?1' if platform in ['Android', 'iPhone', 'iPad'] else '?0'
    branded_name = browser_info['branded_name']

    common_headers = {
        'User-Agent': useragent,
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': referer,
        'Origin': referer,
        'Connection': 'keep-alive',
    }
    if not url:
        common_headers.pop('Origin')

    if 'Chrome' in useragent or 'Chromium' in useragent:
        common_headers.update({
            'Content-type': 'application/json',
            'Sec-CH-UA': f'"Chromium";v="{major_version}", "{branded_name}";v="{major_version}", "Not?A_Brand";v="99"',
            'Sec-CH-UA-Mobile': is_mobile,
            'Sec-CH-UA-Platform': f'"{platform}"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
        })
    elif 'Firefox' in useragent:
        common_headers.update({
            'Accept-Encoding': 'gzip, deflate, br',
            'Access-Control-Request-Headers': 'content-type',
            'DNT': '1',
            'Sec-GPC': '1',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'TE': 'trailers'
        })
    elif 'Safari' in useragent:
        common_headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
        })

    return common_headers if not lowercase else {k.lower(): v for k, v in common_headers.items()}

try:
    if BROWSERS_DATA.exists():
        actualize_browsers_version(BROWSERS_DATA)
except Exception as ext:
    print('actualize_browsers_version:', ext)
