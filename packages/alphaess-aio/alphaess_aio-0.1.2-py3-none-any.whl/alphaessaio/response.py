"""Response classes for alphaess requests."""

import logging
import datetime
from typing import List
from pydantic import BaseModel, Field, model_validator, ConfigDict, AliasChoices


class DataSn(BaseModel):
    "Response data model for Sn"

    model_config = ConfigDict(extra="allow")

    @model_validator(mode="after")
    def check_extras(self):
        logging.debug(f"extra fields detected: {self.model_extra}")
        return self


class DataVerificationCode(BaseModel):
    "Response data model for VerificationCode"

    model_config = ConfigDict(extra="allow")

    @model_validator(mode="after")
    def check_extras(self):
        logging.debug(f"extra fields detected: {self.model_extra}")
        return self


class DataControlEvCharger(BaseModel):
    "Response data model for ControlEvCharger"

    model_config = ConfigDict(extra="allow")

    @model_validator(mode="after")
    def check_extras(self):
        logging.debug(f"extra fields detected: {self.model_extra}")
        return self


class DataEvChargerConfigList(BaseModel):
    "Response data model for getEvChargerConfigList"

    evcharger_sn: str = Field(..., alias="evchargerSn", description="EV-charger SN")
    evcharger_model: str = Field(
        ..., alias="evchargerModel", description="EV-charger model"
    )

    model_config = ConfigDict(extra="allow")

    @model_validator(mode="after")
    def check_extras(self):
        if self.model_extra:
            logging.debug(f"extra fields detected: {self.model_extra }")
        return self


class EvChargerConfigList(BaseModel):
    "Response data model for getEvChargerConfigList"

    code: int = Field(..., alias="code", description="Return Code")
    info: str = Field(
        ..., validation_alias=AliasChoices("info", "msg"), description="Return Message"
    )
    data: List[DataEvChargerConfigList] = Field(
        ..., alias="data", description="Data List"
    )

    model_config = ConfigDict(extra="allow")

    @model_validator(mode="after")
    def check_extras(self):
        if self.model_extra:
            logging.debug(f"extra fields detected: {self.model_extra }")
        return self


class DataEvChargerCurrentsBySn(BaseModel):
    "Response data model for getEvChargerCurrentsBySn"

    currentsetting: float = Field(
        ..., alias="currentsetting", description="Household current setup"
    )

    model_config = ConfigDict(extra="allow")

    @model_validator(mode="after")
    def check_extras(self):
        if self.model_extra:
            logging.debug(f"extra fields detected: {self.model_extra }")
        return self


class EvChargerCurrentsBySn(BaseModel):
    "Response data model for set and getEvChargerCurrentsBySn"

    code: int = Field(..., alias="code", description="Return Code")
    info: str = Field(
        ..., validation_alias=AliasChoices("info", "msg"), description="Return Message"
    )
    data: DataEvChargerCurrentsBySn = Field(..., alias="data", description="Data")

    model_config = ConfigDict(extra="allow")

    @model_validator(mode="after")
    def check_extras(self):
        if self.model_extra:
            logging.debug(f"extra fields detected: {self.model_extra }")
        return self


class DataEvChargerStatusBySn(BaseModel):
    "Response data model for getEvChargerStatusBySn"

    evcharger_status: int = Field(
        ...,
        alias="evchargerStatus",
        description="1: Available state (not plugged in)2: Preparing state of insertion (plugged in and not activated)3: Charging state (charging with power output)4: SuspendedEVSE pile Suspended at the terminal (already started but no available power)5: SuspendedEV Suspended at the vehicle end (with available power, waiting for the car to respond)6: Finishing The charging end state (actively swiping the card to stop or EMS stop control)9: Faulted fault state (pile failure)",
    )

    model_config = ConfigDict(extra="allow")

    @model_validator(mode="after")
    def check_extras(self):
        if self.model_extra:
            logging.debug(f"extra fields detected: {self.model_extra }")
        return self


class EvChargerStatusBySn(BaseModel):
    "Response data model for getEvChargerStatusBySn"

    code: int = Field(..., alias="code", description="Return Code")
    info: str = Field(
        ..., validation_alias=AliasChoices("info", "msg"), description="Return Message"
    )
    data: List[DataEvChargerStatusBySn] = Field(
        ..., alias="data", description="Data List"
    )

    model_config = ConfigDict(extra="allow")

    @model_validator(mode="after")
    def check_extras(self):
        if self.model_extra:
            logging.debug(f"extra fields detected: {self.model_extra }")
        return self


class ControlEvCharger(BaseModel):
    "Response data model for remoteControlEvCharger"

    code: int = Field(..., alias="code", description="Return Code")
    info: str = Field(
        ..., validation_alias=AliasChoices("info", "msg"), description="Return Message"
    )
    data: DataControlEvCharger = Field(..., alias="data", description="Data")

    model_config = ConfigDict(extra="allow")

    @model_validator(mode="after")
    def check_extras(self):
        if self.model_extra:
            logging.debug(f"extra fields detected: {self.model_extra }")
        return self


class DataSumDataForCustomer(BaseModel):
    "Response data model for getSumDataForCustomer"

    epvtoday: float = Field(
        ..., alias="epvtoday", description="Today's Generation,unit：kwh"
    )
    epvtotal: float = Field(
        ..., alias="epvtotal", description="Total Generation,unit：kwh"
    )
    eload: float = Field(..., alias="eload", description="Today's Load,unit：kwh")
    eoutput: float = Field(
        ..., alias="eoutput", description="Today's Feed-in,unit：kwh"
    )
    einput: float = Field(..., alias="einput", description="Today's Consumed,unit：kwh")
    echarge: float = Field(
        ..., alias="echarge", description="Today's Charged,unit：kwh"
    )
    edischarge: float = Field(
        ..., alias="edischarge", description="Today's DisCharged,unit：kwh"
    )
    today_income: float = Field(..., alias="todayIncome", description="Today's Income")
    total_income: float = Field(..., alias="totalIncome", description="Total Profit")
    eself_consumption: float = Field(
        ..., alias="eselfConsumption", description="Self-consumption,unit：%"
    )
    eself_sufficiency: float = Field(
        ..., alias="eselfSufficiency", description="Self-sufficiency,unit：%"
    )
    tree_num: float = Field(..., alias="treeNum", description="Trees Planted")
    carbon_num: float = Field(
        ..., alias="carbonNum", description="CO2 Reduction,unit：kg"
    )
    money_type: str = Field(..., alias="moneyType", description="Currencies")

    model_config = ConfigDict(extra="allow")

    @model_validator(mode="after")
    def check_extras(self):
        if self.model_extra:
            logging.debug(f"extra fields detected: {self.model_extra }")
        return self


class SumDataForCustomer(BaseModel):
    "Response data model for getSumDataForCustomer"

    code: int = Field(..., alias="code", description="Return Code")
    info: str = Field(
        ..., validation_alias=AliasChoices("info", "msg"), description="Return Message"
    )
    data: DataSumDataForCustomer = Field(..., alias="data", description="Return Data")

    model_config = ConfigDict(extra="allow")

    @model_validator(mode="after")
    def check_extras(self):
        if self.model_extra:
            logging.debug(f"extra fields detected: {self.model_extra }")
        return self


class PevDetail(BaseModel):
    "Response data model for getLastPowerData"

    ev1_power: float = Field(..., alias="ev1Power", description="ev1Power")
    ev2_power: float = Field(..., alias="ev2Power", description="ev2Power")
    ev3_power: float = Field(..., alias="ev3Power", description="ev3Power")
    ev4_power: float = Field(..., alias="ev4Power", description="ev4Power")

    model_config = ConfigDict(extra="allow")

    @model_validator(mode="after")
    def check_extras(self):
        if self.model_extra:
            logging.debug(f"extra fields detected: {self.model_extra }")
        return self


class PgridDetail(BaseModel):
    "Response data model for getLastPowerData"

    pmeter_l1: float = Field(..., alias="pmeterL1", description="pmeterL1")
    pmeter_l2: float = Field(..., alias="pmeterL2", description="pmeterL2")
    pmeter_l3: float = Field(..., alias="pmeterL3", description="pmeterL3")

    model_config = ConfigDict(extra="allow")

    @model_validator(mode="after")
    def check_extras(self):
        if self.model_extra:
            logging.debug(f"extra fields detected: {self.model_extra }")
        return self


class PpvDetail(BaseModel):
    "Response data model for getLastPowerData"

    ppv1: float = Field(..., alias="ppv1", description="ppv1")
    ppv2: float = Field(..., alias="ppv2", description="ppv2")
    ppv3: float = Field(..., alias="ppv3", description="ppv3")
    ppv4: float = Field(..., alias="ppv4", description="ppv4")
    pmeter_dc: float = Field(..., alias="pmeterDc", description="pmeterDc")

    model_config = ConfigDict(extra="allow")

    @model_validator(mode="after")
    def check_extras(self):
        if self.model_extra:
            logging.debug(f"extra fields detected: {self.model_extra }")
        return self


class DataLastPowerData(BaseModel):
    "Response data model for getLastPowerData"

    ppv: float = Field(..., alias="ppv", description="Pv total power, unit: W")
    ppv_detail: PpvDetail = Field(..., alias="ppvDetail", description="Data entity")
    pload: float = Field(..., alias="pload", description="Load, unit: W")
    soc: float = Field(..., alias="soc", description="soc")
    pgrid: float = Field(
        ...,
        alias="pgrid",
        description="When pgrid is positive, it means taking electricity from the mains; when pgrid is negative, it means selling electricity. Unit:W",
    )
    pgrid_detail: PgridDetail = Field(
        ..., alias="pgridDetail", description="data entity"
    )
    pbat: float = Field(..., alias="pbat", description="Battery power, unit: W")
    preal_l1: float = Field(..., alias="prealL1", description="prealL1")
    preal_l2: float = Field(..., alias="prealL2", description="prealL2")
    preal_l3: float = Field(..., alias="prealL3", description="prealL3")
    pev: float = Field(
        ..., alias="pev", description="Total power of charging pile, unit: W"
    )
    pev_detail: PevDetail = Field(..., alias="pevDetail", description="Data entity")

    model_config = ConfigDict(extra="allow")

    @model_validator(mode="after")
    def check_extras(self):
        if self.model_extra:
            logging.debug(f"extra fields detected: {self.model_extra }")
        return self


class LastPowerData(BaseModel):
    "Response data model for getLastPowerData"

    code: int = Field(
        ...,
        alias="code",
        description="Return status. If 200 is returned, the operation is successful. If other codes are returned, you need to check the return code to indicate the description corresponding to this code.",
    )
    info: str = Field(
        ...,
        validation_alias=AliasChoices("info", "msg"),
        description="Return information",
    )
    data: DataLastPowerData = Field(..., alias="data", description="return data set")

    model_config = ConfigDict(extra="allow")

    @model_validator(mode="after")
    def check_extras(self):
        if self.model_extra:
            logging.debug(f"extra fields detected: {self.model_extra }")
        return self


class DataOneDayPowerBySn(BaseModel):
    "Response data model for getOneDayPowerBySn"

    cbat: float = Field(
        ..., validation_alias=AliasChoices("cbat", "cobat"), description="BAT"
    )
    feed_in: float = Field(..., alias="feedIn", description="Feed-in")
    grid_charge: float = Field(
        ..., alias="gridCharge", description="Grid purchase real-time power"
    )
    load: float = Field(..., alias="load", description="Load")
    pcharging_pile: float = Field(
        ..., alias="pchargingPile", description="Charging pile power"
    )
    ppv: float = Field(..., alias="ppv", description="PV power")
    sys_sn: str = Field(..., alias="sysSn", description="System S/N")
    upload_time: datetime.datetime = Field(
        ..., alias="uploadTime", description="upload Time"
    )

    model_config = ConfigDict(extra="allow")

    @model_validator(mode="after")
    def check_extras(self):
        if self.model_extra:
            logging.debug(f"extra fields detected: {self.model_extra }")
        return self


class OneDayPowerBySn(BaseModel):
    "Response data model for getOneDayPowerBySn"

    code: int = Field(..., alias="code", description="Return Code")
    info: str = Field(
        ..., validation_alias=AliasChoices("info", "msg"), description="Return Message"
    )
    data: List[DataOneDayPowerBySn] = Field(
        ..., alias="data", description="Return Data"
    )

    model_config = ConfigDict(extra="allow")

    @model_validator(mode="after")
    def check_extras(self):
        if self.model_extra:
            logging.debug(f"extra fields detected: {self.model_extra }")
        return self


class DataOneDateEnergyBySn(BaseModel):
    "Response data model for getOneDateEnergyBySn"

    e_charge: float = Field(
        ..., alias="eCharge", description="total energy charged from battery，unit：kWh"
    )
    e_charging_pile: float = Field(
        ...,
        alias="eChargingPile",
        description="Total energy consumed by charging piles，unit：kWh",
    )
    e_discharge: float = Field(
        ..., alias="eDischarge", description="Discharge，unit：kWh"
    )
    e_grid_charge: float = Field(
        ..., alias="eGridCharge", description="Grid-charge，unit：kWh"
    )
    e_input: float = Field(
        ..., alias="eInput", description="Grid consumption，unit：kWh"
    )
    e_output: float = Field(..., alias="eOutput", description="Feed-in，unit：kWh")
    epv: float = Field(..., alias="epv", description="PV generation，unit：kWh")
    sys_sn: str = Field(..., alias="sysSn", description="System S/N")
    the_date: str = Field(..., alias="theDate", description="Date")

    model_config = ConfigDict(extra="allow")

    @model_validator(mode="after")
    def check_extras(self):
        if self.model_extra:
            logging.debug(f"extra fields detected: {self.model_extra }")
        return self


class OneDateEnergyBySn(BaseModel):
    "Response data model for getOneDateEnergyBySn"

    code: int = Field(..., alias="code", description="Return Code")
    info: str = Field(
        ..., validation_alias=AliasChoices("info", "msg"), description="Return Message"
    )
    data: DataOneDateEnergyBySn = Field(..., alias="data", description="Return Data")

    model_config = ConfigDict(extra="allow")

    @model_validator(mode="after")
    def check_extras(self):
        if self.model_extra:
            logging.debug(f"extra fields detected: {self.model_extra }")
        return self


class DataChargeConfigInfo(BaseModel):
    "Response data model for getChargeConfigInfo"

    bat_high_cap: float = Field(
        ..., alias="batHighCap", description="Charging Stops at SOC [%]"
    )
    grid_charge: int = Field(
        ..., alias="gridCharge", description="Enable Grid Charging Battery"
    )
    time_chae1: str = Field(
        ..., alias="timeChae1", description="Charging Period 1 end time"
    )
    time_chae2: str = Field(
        ..., alias="timeChae2", description="Charging Period 2 end time"
    )
    time_chaf1: str = Field(
        ..., alias="timeChaf1", description="Charging Period 1 start time"
    )
    time_chaf2: str = Field(
        ..., alias="timeChaf2", description="Charging Period 2 start time"
    )

    model_config = ConfigDict(extra="allow")

    @model_validator(mode="after")
    def check_extras(self):
        if self.model_extra:
            logging.debug(f"extra fields detected: {self.model_extra }")
        return self


class ChargeConfigInfo(BaseModel):
    "Response data model for update and getChargeConfigInfo"

    code: int = Field(..., alias="code", description="Return Code")
    info: str = Field(
        ..., validation_alias=AliasChoices("info", "msg"), description="Return Message"
    )
    data: DataChargeConfigInfo = Field(..., alias="data", description="Return Data")

    model_config = ConfigDict(extra="allow")

    @model_validator(mode="after")
    def check_extras(self):
        if self.model_extra:
            logging.debug(f"extra fields detected: {self.model_extra }")
        return self


class DataDisChargeConfigInfo(BaseModel):
    "Response data model for getDisChargeConfigInfo"

    bat_use_cap: float = Field(
        ..., alias="batUseCap", description="Discharging Cutoff SOC [%]"
    )
    ctr_dis: int = Field(
        ..., alias="ctrDis", description="Enable Battery Discharge Time Control"
    )
    time_dise1: str = Field(
        ..., alias="timeDise1", description="Discharging Period 1 End time"
    )
    time_dise2: str = Field(
        ..., alias="timeDise2", description="Discharging Period 2 End time"
    )
    time_disf1: str = Field(
        ..., alias="timeDisf1", description="Discharging Period 1 Start time"
    )
    time_disf2: str = Field(
        ..., alias="timeDisf2", description="Discharging Period 2 Start time"
    )

    model_config = ConfigDict(extra="allow")

    @model_validator(mode="after")
    def check_extras(self):
        if self.model_extra:
            logging.debug(f"extra fields detected: {self.model_extra }")
        return self


class DisChargeConfigInfo(BaseModel):
    "Response data model for update and getDisChargeConfigInfo"

    code: int = Field(..., alias="code", description="Return Code")
    info: str = Field(
        ..., validation_alias=AliasChoices("info", "msg"), description="Return Message"
    )
    data: DataDisChargeConfigInfo = Field(..., alias="data", description="Return Data")

    model_config = ConfigDict(extra="allow")

    @model_validator(mode="after")
    def check_extras(self):
        if self.model_extra:
            logging.debug(f"extra fields detected: {self.model_extra }")
        return self


class VerificationCode(BaseModel):
    "Response data model for getVerificationCode"

    code: int = Field(..., alias="code", description="Return Code")
    info: str = Field(
        ..., validation_alias=AliasChoices("info", "msg"), description="Return Message"
    )
    data: DataVerificationCode = Field(..., alias="data", description="Return Data")

    model_config = ConfigDict(extra="allow")

    @model_validator(mode="after")
    def check_extras(self):
        if self.model_extra:
            logging.debug(f"extra fields detected: {self.model_extra }")
        return self


class Sn(BaseModel):
    "Response data model for bindSn"

    code: int = Field(..., alias="code", description="Return Code")
    info: str = Field(
        ..., validation_alias=AliasChoices("info", "msg"), description="Return Message"
    )
    data: DataSn = Field(..., alias="data", description="Return Data")

    model_config = ConfigDict(extra="allow")

    @model_validator(mode="after")
    def check_extras(self):
        if self.model_extra:
            logging.debug(f"extra fields detected: {self.model_extra }")
        return self


class BindSn(BaseModel):
    "Response data model for unBindSn"

    code: int = Field(..., alias="code", description="Return Code")
    info: str = Field(
        ..., validation_alias=AliasChoices("info", "msg"), description="Return Message"
    )
    data: DataSn = Field(..., alias="data", description="Return Data")

    model_config = ConfigDict(extra="allow")

    @model_validator(mode="after")
    def check_extras(self):
        if self.model_extra:
            logging.debug(f"extra fields detected: {self.model_extra }")
        return self


class DataEssList(BaseModel):
    "Response data model for getEssList"

    cbat: float = Field(
        ...,
        validation_alias=AliasChoices("cbat", "cobat"),
        description="battery capacity",
    )
    ems_status: str = Field(..., alias="emsStatus", description="EMS status")
    mbat: str = Field(..., alias="mbat", description="battery model")
    minv: str = Field(..., alias="minv", description="Inverter model")
    poinv: float = Field(..., alias="poinv", description="Inverter nominal Power")
    popv: float = Field(..., alias="popv", description="Pv nominal Power")
    surplus_cobat: float = Field(
        ..., alias="surplusCobat", description="Battery capacity remaining"
    )
    sys_sn: str = Field(..., alias="sysSn", description="System S/N")
    us_capacity: float = Field(
        ..., alias="usCapacity", description="Battery Available Percentage"
    )

    model_config = ConfigDict(extra="allow")

    @model_validator(mode="after")
    def check_extras(self):
        if self.model_extra:
            logging.debug(f"extra fields detected: {self.model_extra }")
        return self


class EssList(BaseModel):
    "Response data model for getEssList"

    code: int = Field(..., alias="code", description="Return Code")
    info: str = Field(
        ..., validation_alias=AliasChoices("info", "msg"), description="Return Message"
    )
    data: List[DataEssList] = Field(..., alias="data", description="Return Data")

    model_config = ConfigDict(extra="allow")

    @model_validator(mode="after")
    def check_extras(self):
        if self.model_extra:
            logging.debug(f"extra fields detected: {self.model_extra }")
        return self
