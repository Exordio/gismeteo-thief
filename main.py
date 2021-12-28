from pprint import PrettyPrinter
from fake_headers import Headers
from requests import get as rg
from lxml import html


class GismeteoThief:
    pp = PrettyPrinter(width=41, compact=True)
    header = Headers(
        browser="chrome",
        os="win",
        headers=True
    )
    hdr = header.generate()
    page = None
    tree = None

    GISMETEO_URL = 'https://www.gismeteo.ru/weather-bangkok-5993/weekly/'

    def __init__(self):
        self.__enrichment_headers()
        self.__steal_weather()
        self.__make_a_deal_with_a_jeweler()

    def __enrichment_headers(self):
        self.hdr['Upgrade-Insecure-Requests'] = '1'
        self.hdr['Sec-Fetch-Dest'] = 'document'
        self.hdr['Sec-Fetch-Mode'] = 'navigate'
        self.hdr['Sec-Fetch-Site'] = 'same-origin'
        self.hdr['Sec-Fetch-User'] = '?1'
        self.hdr['Connection'] = 'keep-alive'
        self.hdr['Cache-Control'] = 'max-age=0'
        self.hdr['TE'] = 'trailers'

    def __steal_weather(self):
        self.page = rg(self.GISMETEO_URL, headers=self.hdr)

    def __make_a_deal_with_a_jeweler(self):
        with GismeteoJeweler(self.page) as GJ:
            GJ.jeweler_please_rate_this()
            GJ.jeweler_please_cut_these_gems()
            GJ.rate_rate_rate()

            print('\nIts for u my friend : \n')

            self.pp.pprint(GJ.jeweler_prepare_gems_for_sale())


class GismeteoJeweler:
    DAYS_XPATH = '/html/body/section[2]/div[1]/section[2]/div/div/div/div/div[1]//text()'
    WEATHER_XPATH = '/html/body/section[2]/div[1]/section[2]/div/div/div/div/div[2]//@data-text'
    TEMP_XPATH = '/html/body/section[2]/div[1]/section[2]/div/div/div/div/div[3]/div/div//text()'
    MAX_WIND_XPATH = '/html/body/section[2]/div[1]/section[2]/div/div/div/div/div[4]//text()'
    WIND_XPATH = '/html/body/section[2]/div[1]/section[9]/div/div[2]/div/div/div[2]//text()'
    SR_SUT_TEMP_XPATH = '/html/body/section[2]/div[1]/section[7]/div/div[2]/div/div/div[2]/div/div//text()'
    PRESSURE_XPATH = '/html/body/section[2]/div[1]/section[10]/div/div[2]/div/div/div[2]/div/div//text()'
    HUMIDITY_XPATH = '/html/body/section[2]/div[1]/section[11]/div/div[2]/div/div/div[2]//text()'
    UFX_IDX_XPATH = '/html/body/section[2]/div[1]/section[12]/div/div[2]/div/div/div[2]//text()'
    GEOMAGNITE_ACTIVE_KP_IDX_XPATH = '/html/body/section[2]/div[1]/section[13]/div/div[2]/div/div/div[2]//text()'

    days = None
    weather = None

    temp = None
    temp_max_f = None
    temp_max_c = None
    temp_min_f = None
    temp_min_c = None

    sr_sut_temp = None
    sr_temp_f = None
    sr_temp_c = None

    max_wind = None
    wind = None
    max_wind_kp_s = None
    max_wind_mp_s = None
    wind_kp_s = None
    wind_mp_s = None

    pressure = None
    max_pressure_mm_hg_atm = None
    max_pressure_h_pa = None
    min_pressure_mm_hg_atm = None
    min_pressure_h_pa = None

    humidity = None

    ufx_idx = None

    gmagn_act_idx = None

    w_len = None

    page = None
    tree = None

    def __init__(self, page):
        self.page = page

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def jeweler_please_rate_this(self):
        self.__planting_a_tree()
        self.__tree_cutting()

    def jeweler_please_cut_these_gems(self):
        self.w_len = len(self.weather)
        self.days = self.__combine_days()

        temp_idx_shift = 4
        self.temp_max_c = self.__unpack_values(self.temp, 0, temp_idx_shift)
        self.temp_max_f = self.__unpack_values(self.temp, 1, temp_idx_shift)
        self.temp_min_c = self.__unpack_values(self.temp, 2, temp_idx_shift)
        self.temp_min_f = self.__unpack_values(self.temp, 3, temp_idx_shift)

        sr_temp_idx_shift = 2
        self.sr_temp_c = self.__unpack_values(self.sr_sut_temp, 0, sr_temp_idx_shift)
        self.sr_temp_f = self.__unpack_values(self.sr_sut_temp, 1, sr_temp_idx_shift)

        wind_idx_shift = 2
        self.wind_mp_s = self.__unpack_values(self.wind, 0, wind_idx_shift)
        self.wind_kp_s = self.__unpack_values(self.wind, 1, wind_idx_shift)
        self.max_wind_mp_s = self.__unpack_values(self.max_wind, 0, wind_idx_shift)
        self.max_wind_kp_s = self.__unpack_values(self.max_wind, 1, wind_idx_shift)

        pressure_idx_shift = 4
        self.max_pressure_mm_hg_atm = self.__unpack_values(self.pressure, 0, pressure_idx_shift)
        self.max_pressure_h_pa = self.__unpack_values(self.pressure, 1, pressure_idx_shift)
        self.min_pressure_mm_hg_atm = self.__unpack_values(self.pressure, 2, pressure_idx_shift)
        self.min_pressure_h_pa = self.__unpack_values(self.pressure, 3, pressure_idx_shift)

    def jeweler_prepare_gems_for_sale(self):
        bargain = []
        for i in range(self.w_len):
            bargain.append({
                'day': self.days[i],
                'weather': self.weather[i],
                'temp_max_c': self.temp_max_c[i],
                'temp_max_f': self.temp_max_f[i],
                'temp_min_c': self.temp_min_c[i],
                'temp_min_f': self.temp_min_f[i],
                'sr_temp_c': self.sr_temp_c[i],
                'sr_temp_f': self.sr_temp_f[i],
                'wind_mp_s': self.wind_mp_s[i],
                'wind_kp_s': self.wind_kp_s[i],
                'max_wind_mp_s': self.max_wind_mp_s[i],
                'max_wind_kp_s': self.max_wind_kp_s[i],
                'max_pressure_mm_hg_atm': self.max_pressure_mm_hg_atm[i],
                'max_pressure_h_pa': self.max_pressure_h_pa[i],
                'min_pressure_mm_hg_atm': self.min_pressure_mm_hg_atm[i],
                'min_pressure_h_pa': self.min_pressure_h_pa[i],
                'humidity_percent': self.humidity[i],
                'ufx_idx': self.ufx_idx[i],
                'gmagn_act_idx': self.gmagn_act_idx[i]
            })
        return bargain

    @staticmethod
    def __unpack_values(obj_to_unpack, i, shift):
        unpacked = []
        while i <= len(obj_to_unpack) - 1:
            unpacked.append(obj_to_unpack[i].strip())
            i += shift
        return unpacked

    def __combine_days(self):
        unpacked = []
        i = 0
        while i <= len(self.days) - 1:
            unpacked.append(' '.join([self.days[i], self.days[i + 1]]))
            i += 2
        return unpacked

    def __planting_a_tree(self):
        self.tree = html.fromstring(self.page.content)

    def __tree_cutting(self):
        self.days = self.tree.xpath(self.DAYS_XPATH)
        self.weather = [w for w in self.tree.xpath(self.WEATHER_XPATH)]
        self.temp = self.tree.xpath(self.TEMP_XPATH)
        self.max_wind = self.tree.xpath(self.MAX_WIND_XPATH)[3:]
        self.wind = self.tree.xpath(self.WIND_XPATH)
        self.sr_sut_temp = self.tree.xpath(self.SR_SUT_TEMP_XPATH)
        self.pressure = self.tree.xpath(self.PRESSURE_XPATH)
        self.humidity = self.tree.xpath(self.HUMIDITY_XPATH)
        self.ufx_idx = self.tree.xpath(self.UFX_IDX_XPATH)
        self.gmagn_act_idx = self.tree.xpath(self.GEOMAGNITE_ACTIVE_KP_IDX_XPATH)

    def rate_rate_rate(self):
        brake = '''| ============================================================================================= | '''

        print(brake)
        print(f'Дни недели :              {self.days}')
        print(f'Погода :                  {self.weather}')
        print(brake)
        print(f'Макс. темп. по цельсию :  {self.temp_max_c}')
        print(f'Макс. темп. по фарингт :  {self.temp_max_f}')
        print(f'Мин. темп. по цельсию :   {self.temp_min_c}')
        print(f'Мин. темп. по фанингт :   {self.temp_min_f}')
        print(f'Срд. темп. по цельсию :   {self.sr_temp_c}')
        print(f'Срд. темп. по фарингт :   {self.sr_temp_f}')
        print(brake)
        print(f'Скр. ветр. м в сек :      {self.wind_mp_s}')
        print(f'Скр. ветр. км в сек :     {self.wind_kp_s}')
        print(f'Макс. скр. в. м. в сек :  {self.max_wind_mp_s}')
        print(f'Макс. скр. в. км. в сек : {self.max_wind_kp_s}')
        print(brake)
        print(f'Макс. дав. мм рт. с. :    {self.max_pressure_mm_hg_atm}')
        print(f'Макс. дав. гектопаскаль : {self.max_pressure_h_pa}')
        print(f'Мин. дав. мм рт. с. :     {self.min_pressure_mm_hg_atm}')
        print(f'Мин. дав. гектопаскаль :  {self.min_pressure_h_pa}')
        print(brake)
        print(f'Процент влажности :       {self.humidity}')
        print(f'Ультр фиол. Индкс. :      {self.ufx_idx}')
        print(f'Геомагнит актив. кп-и   : {self.gmagn_act_idx}')
        print(brake)


if __name__ == '__main__':
    GT = GismeteoThief()
