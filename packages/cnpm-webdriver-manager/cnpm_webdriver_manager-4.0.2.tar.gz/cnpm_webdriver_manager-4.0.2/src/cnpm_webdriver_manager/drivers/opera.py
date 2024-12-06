from datetime import datetime

from webdriver_manager.core.logger import log
from webdriver_manager.drivers import opera


class OperaDriver(opera.OperaDriver):
    def __init__(
        self,
        name,
        driver_version,
        url,
        latest_release_url,
        opera_release_tag,
        http_client,
        os_system_manager
    ):
        super().__init__(
            name=name,
            driver_version=driver_version,
            url=url,
            latest_release_url=latest_release_url,
            opera_release_tag=opera_release_tag,
            http_client=http_client,
            os_system_manager=os_system_manager
        )

    def get_latest_release_version(self) -> str:
        resp = self._http_client.get(self.latest_release_url)
        resp = resp.json()
        resp.sort(key=lambda x: datetime.fromisoformat(x['date'].replace('Z', '+00:00')), reverse=True)
        return resp[0]['name'][:-1]

    def get_driver_download_url(self, os_type) -> str:
        '''Like https://registry.npmmirror.com/-/binary/operadriver/v.2.45/operadriver_linux64.zip'''
        driver_version_to_download = self.get_driver_version_to_download()
        log(f'Getting latest opera release info for {driver_version_to_download}')
        resp = self._http_client.get(self.tagged_release_url(driver_version_to_download))
        assets = resp.json()
        name = '{0}_{1}'.format(self.get_name(), os_type)
        output_dict = [asset for asset in assets if asset['name'].startswith(name)]
        return output_dict[0]['url']