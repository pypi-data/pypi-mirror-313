"""Sending requests to AlphaESS API"""

import logging
import time
import hashlib
import json
import aiohttp
import pydantic
from alphaessaio import response

logger = logging.getLogger(__name__)


class AlphaEssRequestError(Exception):
    def __init__(self, response_data: dict):
        message = f"Error: {response_data}"
        super().__init__(message)


class AlphaEssAuth(pydantic.BaseModel):
    appid: str
    appsecret: pydantic.SecretStr

    def _get_signature(self, timestamp) -> str:
        return str(
            hashlib.sha512(
                (f"{self.appid}{self.appsecret.get_secret_value()}{timestamp}").encode(
                    "ascii"
                )
            ).hexdigest()
        )

    def create_headers(self):
        timestamp = str(int(time.time()))
        sign = self._get_signature(timestamp)
        return {"appId": self.appid, "timeStamp": timestamp, "sign": sign}


class AlphaEssAPI:
    def __init__(self, auth: AlphaEssAuth):
        self.auth = auth

    async def _get(self, url, params) -> dict:
        headers = self.auth.create_headers()
        async with aiohttp.ClientSession() as session:
            logger.debug(f"Sending get request to {url=} with {params=}")
            async with session.get(url, headers=headers, params=params) as resp:
                return await self._evaluate_response(resp)

    async def _post(self, url, params) -> dict:
        headers = self.auth.create_headers()
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=params) as resp:
                return await self._evaluate_response(resp)

    @staticmethod
    async def _evaluate_response(resp: aiohttp.ClientResponse) -> dict:
        try:
            data = await resp.json()
            logger.debug(f"api response: {data}")
        except json.JSONDecodeError as json_decode_error:
            raise AlphaEssRequestError(
                {"msg": "returned data is not valid json", "err": json_decode_error}
            )
        if resp.status == 200 and data.get("code", 0) == 200:
            logger.debug(f"Request successful. {resp.url}")
            return data
        logger.error(f"Request error: {data=}")
        raise AlphaEssRequestError(data)

    @pydantic.validate_call
    async def get_ev_charger_config_list(
        self, sys_sn: str
    ) -> response.EvChargerConfigList:
        """Obtain the SN of the charging pile according to the SN, and set the model

        Args:
            sys_sn (str): System S/N

        Returns:
            (response.EvChargerConfigList): response data
        """

        raw_response: dict = await self._get(
            "https://openapi.alphaess.com/api/getEvChargerConfigList", {"sysSn": sys_sn}
        )

        return response.EvChargerConfigList(**raw_response)

    @pydantic.validate_call
    async def get_ev_charger_currents_by_sn(
        self, sys_sn: str
    ) -> response.EvChargerCurrentsBySn:
        """Obtain the current setting of charging pile household according to SN

        Args:
            sys_sn (str): sys sn

        Returns:
            (response.EvChargerCurrentsBySn): response data
        """

        raw_response: dict = await self._get(
            "https://openapi.alphaess.com/api/getEvChargerCurrentsBySn",
            {"sysSn": sys_sn},
        )

        return response.EvChargerCurrentsBySn(**raw_response)

    @pydantic.validate_call
    async def set_ev_charger_currents_by_sn(
        self, sys_sn: str, currentsetting: float
    ) -> response.EvChargerCurrentsBySn:
        """Set charging pile household current setting according to SN

        Args:
            sys_sn (str): SN
        currentsetting (float): Household current setup

        Returns:
            (response.EvChargerCurrentsBySn): response data
        """

        raw_response: dict = await self._post(
            "https://openapi.alphaess.com/api/setEvChargerCurrentsBySn",
            {"sysSn": sys_sn, "currentsetting": currentsetting},
        )

        return response.EvChargerCurrentsBySn(**raw_response)

    @pydantic.validate_call
    async def get_ev_charger_status_by_sn(
        self, sys_sn: str, evcharger_sn: str
    ) -> response.EvChargerStatusBySn:
        """Obtain charging pile status according to SN+charging pile SN

        Args:
            sys_sn (str): sys SN
        evcharger_sn (str): EV-charger SN

        Returns:
            (response.EvChargerStatusBySn): response data
        """

        raw_response: dict = await self._get(
            "https://openapi.alphaess.com/api/getEvChargerStatusBySn",
            {"sysSn": sys_sn, "evchargerSn": evcharger_sn},
        )

        return response.EvChargerStatusBySn(**raw_response)

    @pydantic.validate_call
    async def remote_control_ev_charger(
        self, sys_sn: str, evcharger_sn: str, control_mode: int
    ) -> response.ControlEvCharger:
        """According to SN+ charging pile SN remote control charging pile to start charging/stop charging

        Args:
            sys_sn (str): sys sn
        evcharger_sn (str): EV-charger SN
        control_mode (int): 0-Stop Charging，1-Start Charging

        Returns:
            (response.ControlEvCharger): response data
        """

        raw_response: dict = await self._post(
            "https://openapi.alphaess.com/api/remoteControlEvCharger",
            {"sysSn": sys_sn, "evchargerSn": evcharger_sn, "controlMode": control_mode},
        )

        return response.ControlEvCharger(**raw_response)

    @pydantic.validate_call
    async def get_sum_data_for_customer(
        self, sys_sn: str
    ) -> response.SumDataForCustomer:
        """According  SN to get System Summary data

        Args:
            sys_sn (str): System S/N

        Returns:
            (response.SumDataForCustomer): response data
        """

        raw_response: dict = await self._get(
            "https://openapi.alphaess.com/api/getSumDataForCustomer", {"sysSn": sys_sn}
        )

        return response.SumDataForCustomer(**raw_response)

    @pydantic.validate_call
    async def get_last_power_data(self, sys_sn: str) -> response.LastPowerData:
        """Get real-time power data based on SN

        Args:
            sys_sn (str): system SN

        Returns:
            (response.LastPowerData): response data
        """

        raw_response: dict = await self._get(
            "https://openapi.alphaess.com/api/getLastPowerData", {"sysSn": sys_sn}
        )

        return response.LastPowerData(**raw_response)

    @pydantic.validate_call
    async def get_one_day_power_by_sn(
        self, query_date: str, sys_sn: str
    ) -> response.OneDayPowerBySn:
        """According  SN to get system power data

        Args:
            query_date (str): Date，Format：yyyy-MM-dd
        sys_sn (str): System S/N

        Returns:
            (response.OneDayPowerBySn): response data
        """

        raw_response: dict = await self._get(
            "https://openapi.alphaess.com/api/getOneDayPowerBySn",
            {"queryDate": query_date, "sysSn": sys_sn},
        )

        return response.OneDayPowerBySn(**raw_response)

    @pydantic.validate_call
    async def get_one_date_energy_by_sn(
        self, query_date: str, sys_sn: str
    ) -> response.OneDateEnergyBySn:
        """According  SN to get System Energy Data

        Args:
            query_date (str): Date，Format：yyyy-MM-dd
        sys_sn (str): System S/N

        Returns:
            (response.OneDateEnergyBySn): response data
        """

        raw_response: dict = await self._get(
            "https://openapi.alphaess.com/api/getOneDateEnergyBySn",
            {"queryDate": query_date, "sysSn": sys_sn},
        )

        return response.OneDateEnergyBySn(**raw_response)

    @pydantic.validate_call
    async def get_charge_config_info(self, sys_sn: str) -> response.ChargeConfigInfo:
        """According  SN to get charging setting information

        Args:
            sys_sn (str): System S/N

        Returns:
            (response.ChargeConfigInfo): response data
        """

        raw_response: dict = await self._get(
            "https://openapi.alphaess.com/api/getChargeConfigInfo", {"sysSn": sys_sn}
        )

        return response.ChargeConfigInfo(**raw_response)

    @pydantic.validate_call
    async def update_charge_config_info(
        self,
        sys_sn: str,
        bat_high_cap: float,
        grid_charge: int,
        time_chae1: str,
        time_chae2: str,
        time_chaf1: str,
        time_chaf2: str,
    ) -> response.ChargeConfigInfo:
        """According SN to Set charging information，Setting frequency 24 hours, set once a day

        Args:
            sys_sn (str): System S/N
        bat_high_cap (float): Charging Stops at SOC [%]
        grid_charge (int): Enable Grid Charging Battery
        time_chae1 (str): Charging Period 1 end time, the time format is HH:mm, such as: 00:00, the maximum is 23:45, the minimum is 00:00, and the interval is 15 minutes, such as: 00:15, 00:30, 00:45, otherwise no effect
        time_chae2 (str): Charging Period 2 end time, the time format is HH:mm, such as: 00:00, the maximum is 23:45, the minimum is 00:00, and the interval is 15 minutes, such as: 00:15, 00:30, 00:45, otherwise no effect
        time_chaf1 (str): Charging Period 1 start time, the time format is HH:mm, such as: 00:00, the maximum is 23:45, the minimum is 00:00, and the interval is 15 minutes, such as: 00:15, 00:30, 00:45, otherwise no effect
        time_chaf2 (str): Charging Period 2 start time, the time format is HH:mm, such as: 00:00, the maximum is 23:45, the minimum is 00:00, and the interval is 15 minutes, such as: 00:15, 00:30, 00:45, otherwise no effect

        Returns:
            (response.ChargeConfigInfo): response data
        """

        raw_response: dict = await self._post(
            "https://openapi.alphaess.com/api/updateChargeConfigInfo",
            {
                "sysSn": sys_sn,
                "batHighCap": bat_high_cap,
                "gridCharge": grid_charge,
                "timeChae1": time_chae1,
                "timeChae2": time_chae2,
                "timeChaf1": time_chaf1,
                "timeChaf2": time_chaf2,
            },
        )

        return response.ChargeConfigInfo(**raw_response)

    @pydantic.validate_call
    async def get_dis_charge_config_info(
        self, sys_sn: str
    ) -> response.DisChargeConfigInfo:
        """According to SN discharge setting information

        Args:
            sys_sn (str): System S/N

        Returns:
            (response.DisChargeConfigInfo): response data
        """

        raw_response: dict = await self._get(
            "https://openapi.alphaess.com/api/getDisChargeConfigInfo", {"sysSn": sys_sn}
        )

        return response.DisChargeConfigInfo(**raw_response)

    @pydantic.validate_call
    async def update_dis_charge_config_info(
        self,
        bat_use_cap: float,
        ctr_dis: int,
        time_dise1: str,
        time_dise2: str,
        time_disf1: str,
        time_disf2: str,
        sys_sn: str,
    ) -> response.DisChargeConfigInfo:
        """According to SN Set discharge information，Setting frequency 24 hours, set once a day

        Args:
            bat_use_cap (float): Discharging Cutoff SOC [%]
        ctr_dis (int): Enable Battery Discharge Time Control
        time_dise1 (str): Discharging Period 1 End time, the time format is HH:mm, such as: 00:00, the maximum is 23:45, the minimum is 00:00, and the interval is 15 minutes, such as: 00:15, 00:30, 00:45, otherwise no effect
        time_dise2 (str): Discharging Period 2 End time, the time format is HH:mm, such as: 00:00, the maximum is 23:45, the minimum is 00:00, and the interval is 15 minutes, such as: 00:15, 00:30, 00:45, otherwise no effect
        time_disf1 (str): Discharging Period 1 Start time, the time format is HH:mm, such as: 00:00, the maximum is 23:45, the minimum is 00:00, and the interval is 15 minutes, such as: 00:15, 00:30, 00:45, otherwise no effect
        time_disf2 (str): Discharging Period 2 Start time, the time format is HH:mm, such as: 00:00, the maximum is 23:45, the minimum is 00:00, and the interval is 15 minutes, such as: 00:15, 00:30, 00:45, otherwise no effect
        sys_sn (str): System S/N

        Returns:
            (response.DisChargeConfigInfo): response data
        """

        raw_response: dict = await self._post(
            "https://openapi.alphaess.com/api/updateDisChargeConfigInfo",
            {
                "batUseCap": bat_use_cap,
                "ctrDis": ctr_dis,
                "timeDise1": time_dise1,
                "timeDise2": time_dise2,
                "timeDisf1": time_disf1,
                "timeDisf2": time_disf2,
                "sysSn": sys_sn,
            },
        )

        return response.DisChargeConfigInfo(**raw_response)

    @pydantic.validate_call
    async def get_verification_code(
        self, sys_sn: str, check_code: str
    ) -> response.VerificationCode:
        """According to SN get the check code according to SN

        Args:
            sys_sn (str): System S/N
        check_code (str): checkCode

        Returns:
            (response.VerificationCode): response data
        """

        raw_response: dict = await self._get(
            "https://openapi.alphaess.com/api/getVerificationCode",
            {"sysSn": sys_sn, "checkCode": check_code},
        )

        return response.VerificationCode(**raw_response)

    @pydantic.validate_call
    async def bind_sn(self, sys_sn: str, code: str) -> response.Sn:
        """According to SN and check code Bind the system bind the system

        Args:
            sys_sn (str): System S/N
        code (str): Verification Code

        Returns:
            (response.Sn): response data
        """

        raw_response: dict = await self._post(
            "https://openapi.alphaess.com/api/bindSn", {"sysSn": sys_sn, "code": code}
        )

        return response.Sn(**raw_response)

    @pydantic.validate_call
    async def un_bind_sn(self, sys_sn: str) -> response.BindSn:
        """According to SN and check code Unbind the system

        Args:
            sys_sn (str): System S/N

        Returns:
            (response.BindSn): response data
        """

        raw_response: dict = await self._post(
            "https://openapi.alphaess.com/api/unBindSn", {"sysSn": sys_sn}
        )

        return response.BindSn(**raw_response)

    @pydantic.validate_call
    async def get_ess_list(
        self,
    ) -> response.EssList:
        """According to SN  to get system list data

        Args:


        Returns:
            (response.EssList): response data
        """

        raw_response: dict = await self._get(
            "https://openapi.alphaess.com/api/getEssList", {}
        )

        return response.EssList(**raw_response)
