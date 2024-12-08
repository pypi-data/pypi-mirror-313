from zur_ecu_client.senml.senml import Senml
from zur_ecu_client.senml.senml_msg import SenmlMessage
from zur_ecu_client.senml.senml_unit import SenmlUnit
from zur_ecu_client.senml.senml_zur_names import SenmlNames


class Ecu:

    class Inverter:
        class Info(SenmlMessage):
            def __init__(
                self,
                FLon: bool = None,
                FRon: bool = None,
                RLon: bool = None,
                RRon: bool = None,
                FLdcOn: bool = None,
                FRdcOn: bool = None,
                RLdcOn: bool = None,
                RRdcOn: bool = None,
                FLready: bool = None,
                FRready: bool = None,
                RLready: bool = None,
                RRready: bool = None,
            ) -> None:
                super().__init__(
                    SenmlNames.ECU_INVERTER_INFO,
                    [
                        Senml.Record(
                            SenmlNames.ECU_INVERTER_INFO_INVERTERON_FL,
                            v=FLon,
                        ),
                        Senml.Record(
                            SenmlNames.ECU_INVERTER_INFO_INVERTERON_FR,
                            v=FRon,
                        ),
                        Senml.Record(
                            SenmlNames.ECU_INVERTER_INFO_INVERTERON_RL,
                            v=RLon,
                        ),
                        Senml.Record(
                            SenmlNames.ECU_INVERTER_INFO_INVERTERON_RR,
                            v=RRon,
                        ),
                        Senml.Record(
                            SenmlNames.ECU_INVERTER_INFO_INVERTERDCON_FL,
                            v=FLdcOn,
                        ),
                        Senml.Record(
                            SenmlNames.ECU_INVERTER_INFO_INVERTERDCON_FR,
                            v=FRdcOn,
                        ),
                        Senml.Record(
                            SenmlNames.ECU_INVERTER_INFO_INVERTERDCON_RL,
                            v=RLdcOn,
                        ),
                        Senml.Record(
                            SenmlNames.ECU_INVERTER_INFO_INVERTERDCON_RR,
                            v=RRdcOn,
                        ),
                        Senml.Record(
                            SenmlNames.ECU_INVERTER_INFO_INVERTERSYSTEMREADY_FL,
                            v=FLready,
                        ),
                        Senml.Record(
                            SenmlNames.ECU_INVERTER_INFO_INVERTERSYSTEMREADY_FR,
                            v=FRready,
                        ),
                        Senml.Record(
                            SenmlNames.ECU_INVERTER_INFO_INVERTERSYSTEMREADY_RL,
                            v=RLready,
                        ),
                        Senml.Record(
                            SenmlNames.ECU_INVERTER_INFO_INVERTERSYSTEMREADY_RR,
                            v=RRready,
                        ),
                    ],
                )

        class Status(SenmlMessage):
            def __init__(
                self,
                FLderating: bool = None,
                FRderating: bool = None,
                RLderating: bool = None,
                RRderating: bool = None,
                FLerror: bool = None,
                FRerror: bool = None,
                RLerror: bool = None,
                RRerror: bool = None,
                FLerrorCode: int = None,
                FRerrorCode: int = None,
                RLerrorCode: int = None,
                RRerrorCode: int = None,
            ) -> None:
                super().__init__(
                    SenmlNames.ECU_INVERTER_STATUS,
                    [
                        Senml.Record(
                            SenmlNames.ECU_INVERTER_STATUS_INVERTERDERATNG_FL,
                            v=FLderating,
                        ),
                        Senml.Record(
                            SenmlNames.ECU_INVERTER_STATUS_INVERTERDERATNG_FR,
                            v=FRderating,
                        ),
                        Senml.Record(
                            SenmlNames.ECU_INVERTER_STATUS_INVERTERDERATNG_RL,
                            v=RLderating,
                        ),
                        Senml.Record(
                            SenmlNames.ECU_INVERTER_STATUS_INVERTERDERATNG_RR,
                            v=RRderating,
                        ),
                        Senml.Record(
                            SenmlNames.ECU_INVERTER_STATUS_INVERTERERROR_FL, v=FLerror
                        ),
                        Senml.Record(
                            SenmlNames.ECU_INVERTER_STATUS_INVERTERERROR_FR, v=FRerror
                        ),
                        Senml.Record(
                            SenmlNames.ECU_INVERTER_STATUS_INVERTERERROR_RL, v=RLerror
                        ),
                        Senml.Record(
                            SenmlNames.ECU_INVERTER_STATUS_INVERTERERROR_RR, v=RRerror
                        ),
                        Senml.Record(
                            SenmlNames.ECU_INVERTER_STATUS_INVERTERERRORCODE_FL,
                            v=FLerrorCode,
                        ),
                        Senml.Record(
                            SenmlNames.ECU_INVERTER_STATUS_INVERTERERRORCODE_FR,
                            v=FRerrorCode,
                        ),
                        Senml.Record(
                            SenmlNames.ECU_INVERTER_STATUS_INVERTERERRORCODE_RL,
                            v=RLerrorCode,
                        ),
                        Senml.Record(
                            SenmlNames.ECU_INVERTER_STATUS_INVERTERERRORCODE_RR,
                            v=RRerrorCode,
                        ),
                    ],
                )

        class Sensor(SenmlMessage):
            def __init__(
                self,
                FLtorque: int = None,
                FRtorque: int = None,
                RLtorque: int = None,
                RRtorque: int = None,
                FLinverterVoltage: int = None,
                FRinverterVoltage: int = None,
                RLinverterVoltage: int = None,
                RRinverterVoltage: int = None,
                FLinverterTemp: int = None,
                FRinverterTemp: int = None,
                RLinverterTemp: int = None,
                RRinverterTemp: int = None,
                FLspeed: int = None,
                FRspeed: int = None,
                RLspeed: int = None,
                RRspeed: int = None,
            ) -> None:
                super().__init__(
                    SenmlNames.ECU_INVERTER_SENSOR,
                    [
                        Senml.Record(
                            SenmlNames.ECU_INVERTER_SENSOR_INVERTERACTUALTORQUE_FL,
                            SenmlUnit.NEWTON,
                            v=FLtorque,
                        ),
                        Senml.Record(
                            SenmlNames.ECU_INVERTER_SENSOR_INVERTERACTUALTORQUE_FR,
                            SenmlUnit.NEWTON,
                            v=FRtorque,
                        ),
                        Senml.Record(
                            SenmlNames.ECU_INVERTER_SENSOR_INVERTERACTUALTORQUE_RL,
                            SenmlUnit.NEWTON,
                            v=RLtorque,
                        ),
                        Senml.Record(
                            SenmlNames.ECU_INVERTER_SENSOR_INVERTERACTUALTORQUE_RR,
                            SenmlUnit.NEWTON,
                            v=RRtorque,
                        ),
                        Senml.Record(
                            SenmlNames.ECU_INVERTER_SENSOR_INVERTERSVOLTAGE_FL,
                            SenmlUnit.VOLT,
                            v=FLinverterVoltage,
                        ),
                        Senml.Record(
                            SenmlNames.ECU_INVERTER_SENSOR_INVERTERSVOLTAGE_FR,
                            SenmlUnit.VOLT,
                            v=FRinverterVoltage,
                        ),
                        Senml.Record(
                            SenmlNames.ECU_INVERTER_SENSOR_INVERTERSVOLTAGE_RL,
                            SenmlUnit.VOLT,
                            v=RLinverterVoltage,
                        ),
                        Senml.Record(
                            SenmlNames.ECU_INVERTER_SENSOR_INVERTERSVOLTAGE_RR,
                            SenmlUnit.VOLT,
                            v=RRinverterVoltage,
                        ),
                        Senml.Record(
                            SenmlNames.ECU_INVERTER_SENSOR_INVERTERTEMP_FL,
                            SenmlUnit.DEGREES_CELSIUS,
                            v=FLinverterTemp,
                        ),
                        Senml.Record(
                            SenmlNames.ECU_INVERTER_SENSOR_INVERTERTEMP_FR,
                            SenmlUnit.DEGREES_CELSIUS,
                            v=FRinverterTemp,
                        ),
                        Senml.Record(
                            SenmlNames.ECU_INVERTER_SENSOR_INVERTERTEMP_RL,
                            SenmlUnit.DEGREES_CELSIUS,
                            v=RLinverterTemp,
                        ),
                        Senml.Record(
                            SenmlNames.ECU_INVERTER_SENSOR_INVERTERTEMP_RR,
                            SenmlUnit.DEGREES_CELSIUS,
                            v=RRinverterTemp,
                        ),
                        Senml.Record(
                            SenmlNames.ECU_INVERTER_SENSOR_INVERTERACTUALRPM_FL,
                            SenmlUnit.EVENT_RATE_PER_MINUTE,
                            v=FLspeed,
                        ),
                        Senml.Record(
                            SenmlNames.ECU_INVERTER_SENSOR_INVERTERACTUALRPM_FR,
                            SenmlUnit.EVENT_RATE_PER_MINUTE,
                            v=FRspeed,
                        ),
                        Senml.Record(
                            SenmlNames.ECU_INVERTER_SENSOR_INVERTERACTUALRPM_RL,
                            SenmlUnit.EVENT_RATE_PER_MINUTE,
                            v=RLspeed,
                        ),
                        Senml.Record(
                            SenmlNames.ECU_INVERTER_SENSOR_INVERTERACTUALRPM_RR,
                            SenmlUnit.EVENT_RATE_PER_MINUTE,
                            v=RRspeed,
                        ),
                    ],
                )

    class Accu(SenmlMessage):
        def __init__(
            self,
            accuPower: int = None,
            averagePower: int = None,
            charge: int = None,
            voltage: int = None,
            current: int = None,
            accuTemperature: int = None,
        ) -> None:
            super().__init__(
                SenmlNames.ECU_ACCU_SENSOR,
                [
                    Senml.Record(
                        SenmlNames.ECU_ACCU_SENSOR_ACCUPOWER,
                        SenmlUnit.AMPERE,
                        accuPower,
                    ),
                    Senml.Record(
                        SenmlNames.ECU_ACCU_SENSOR_AVERAGEPOWER,
                        SenmlUnit.AMPERE,
                        averagePower,
                    ),
                    Senml.Record(
                        SenmlNames.ECU_ACCU_SENSOR_ACCUSTATEOFCHARGE,
                        SenmlUnit.PERCENTAGE,
                        charge,
                    ),
                    Senml.Record(
                        SenmlNames.ECU_ACCU_SENSOR_HVVOLTAGE,
                        SenmlUnit.VOLT,
                        voltage,
                    ),
                    Senml.Record(
                        SenmlNames.ECU_ACCU_SENSOR_HVCURRENT,
                        SenmlUnit.AMPERE,
                        current,
                    ),
                    Senml.Record(
                        SenmlNames.ECU_ACCU_SENSOR_ACCUTEMPERATURE,
                        SenmlUnit.DEGREES_CELSIUS,
                        accuTemperature,
                    ),
                ],
            )

    class Error(SenmlMessage):
        def __init__(
            self,
            code: int = None,
        ) -> None:
            super().__init__(
                SenmlNames.ECU_ERROR_CODE,
                [
                    Senml.Record(
                        SenmlNames.ECU_ERROR_CODE_CODE,
                        v=code,
                    ),
                ],
            )

    class Driverless(SenmlMessage):
        def __init__(
            self,
            steeringAngle: int = None,
            throttle: int = None,
            brake: int = None,
        ) -> None:
            super().__init__(
                SenmlNames.ECU_DRIVERLESS_CONTROL,
                [
                    Senml.Record(
                        SenmlNames.ECU_DRIVERLESS_CONTROL_STEERINGANGLE,
                        SenmlUnit.DEGREES_CELSIUS,
                        steeringAngle,
                    ),
                    Senml.Record(
                        SenmlNames.ECU_DRIVERLESS_CONTROL_DVTHROTTLE,
                        SenmlUnit.PERCENTAGE,
                        throttle,
                    ),
                    Senml.Record(
                        SenmlNames.ECU_DRIVERLESS_CONTROL_DVBRAKE,
                        SenmlUnit.PERCENTAGE,
                        brake,
                    ),
                ],
            )

    class Motor(SenmlMessage):
        def __init__(
            self,
            FLmotorTemp: int = None,
            FRmotorTemp: int = None,
            BLmotorTemp: int = None,
            BRmotorTemp: int = None,
        ) -> None:
            super().__init__(
                SenmlNames.ECU_MOTOR_SENSOR,
                [
                    Senml.Record(
                        SenmlNames.ECU_MOTOR_SENSOR_MOTORTEMP_FL,
                        SenmlUnit.DEGREES_CELSIUS,
                        FLmotorTemp,
                    ),
                    Senml.Record(
                        SenmlNames.ECU_MOTOR_SENSOR_MOTORTEMP_FR,
                        SenmlUnit.DEGREES_CELSIUS,
                        FRmotorTemp,
                    ),
                    Senml.Record(
                        SenmlNames.ECU_MOTOR_SENSOR_MOTORTEMP_BL,
                        SenmlUnit.DEGREES_CELSIUS,
                        BLmotorTemp,
                    ),
                    Senml.Record(
                        SenmlNames.ECU_MOTOR_SENSOR_MOTORTEMP_BR,
                        SenmlUnit.DEGREES_CELSIUS,
                        BRmotorTemp,
                    ),
                ],
            )

    class Steering(SenmlMessage):
        def __init__(
            self,
            SteeringCurrent: int = None,
            SteeringErrorCode: int = None,
            SteeringPosition: int = None,
            SteeringSpeed: int = None,
            SteeringTemperature: int = None,
        ) -> None:
            super().__init__(
                SenmlNames.ECU_STEERING_SENSOR,
                [
                    Senml.Record(
                        SenmlNames.ECU_STEERING_SENSOR_STEERINGCURRENT,
                        SenmlUnit.AMPERE,
                        SteeringCurrent,
                    ),
                    Senml.Record(
                        SenmlNames.ECU_STEERING_SENSOR_STEERINGERRORCODE,
                        None,
                        SteeringErrorCode,
                    ),
                    Senml.Record(
                        SenmlNames.ECU_STEERING_SENSOR_STEERINGPOSITION,
                        None,
                        SteeringPosition,
                    ),
                    Senml.Record(
                        SenmlNames.ECU_STEERING_SENSOR_STEERINGSPEED,
                        SenmlUnit.VELOCITY,
                        SteeringSpeed,
                    ),
                    Senml.Record(
                        SenmlNames.ECU_STEERING_SENSOR_STEERINGTEMPERATURE,
                        SenmlUnit.DEGREES_CELSIUS,
                        SteeringTemperature,
                    ),
                ],
            )

    class Pedal(SenmlMessage):
        def __init__(
            self,
            FbreakPressure: int = None,
            RbreakPressure: int = None,
            LthrottleMax: int = None,
            LthrottleMin: int = None,
            LthrottleValue: int = None,
            RthrottleMax: int = None,
            RthrottleMin: int = None,
            RthrottleValue: int = None,
        ) -> None:
            super().__init__(
                SenmlNames.ECU_PEDAL_SENSOR,
                [
                    Senml.Record(
                        SenmlNames.ECU_PEDAL_SENSOR_BREAKPRESSUREFRONT,
                        SenmlUnit.PASCAL,
                        FbreakPressure,
                    ),
                    Senml.Record(
                        SenmlNames.ECU_PEDAL_SENSOR_BREAKPRESSUREREAR,
                        SenmlUnit.PASCAL,
                        RbreakPressure,
                    ),
                    Senml.Record(
                        SenmlNames.ECU_PEDAL_SENSOR_THROTTLELEFTMAX,
                        SenmlUnit.PERCENTAGE,
                        LthrottleMax,
                    ),
                    Senml.Record(
                        SenmlNames.ECU_PEDAL_SENSOR_THROTTLELEFTMIN,
                        SenmlUnit.PERCENTAGE,
                        LthrottleMin,
                    ),
                    Senml.Record(
                        SenmlNames.ECU_PEDAL_SENSOR_THROTTLELEFTVALUE,
                        SenmlUnit.PERCENTAGE,
                        LthrottleValue,
                    ),
                    Senml.Record(
                        SenmlNames.ECU_PEDAL_SENSOR_THROTTLERIGHTMAX,
                        SenmlUnit.PERCENTAGE,
                        RthrottleMax,
                    ),
                    Senml.Record(
                        SenmlNames.ECU_PEDAL_SENSOR_THROTTLERIGHTMIN,
                        SenmlUnit.PERCENTAGE,
                        RthrottleMin,
                    ),
                    Senml.Record(
                        SenmlNames.ECU_PEDAL_SENSOR_THROTTLERIGHTVALUE,
                        SenmlUnit.PERCENTAGE,
                        RthrottleValue,
                    ),
                ],
            )

    class Other(SenmlMessage):
        def __init__(
            self,
            AIRNegative: int = None,
            AIRPositive: int = None,
            DC_DC_24V: int = None,
            DVon: bool = None,
            LV_Battery_24V: int = None,
            RTDButton: int = None,
            SDC_Pressed: int = None,
            TSButton: int = None,
            current: int = None,
            input_12V: int = None,
            prechargeRelay: int = None,
        ) -> None:
            super().__init__(
                SenmlNames.ECU_OTHER_STATUS,
                [
                    Senml.Record(
                        SenmlNames.ECU_OTHER_STATUS_AIRNEGATIVE,
                        None,
                        AIRNegative,
                    ),
                    Senml.Record(
                        SenmlNames.ECU_OTHER_STATUS_AIRPOSITIVE,
                        None,
                        AIRPositive,
                    ),
                    Senml.Record(
                        SenmlNames.ECU_OTHER_STATUS_DC_DC_24V,
                        None,
                        DC_DC_24V,
                    ),
                    Senml.Record(
                        SenmlNames.ECU_OTHER_STATUS_DVON,
                        False,
                        DVon,
                    ),
                    Senml.Record(
                        SenmlNames.ECU_OTHER_STATUS_LV_BATTERY_24,
                        None,
                        LV_Battery_24V,
                    ),
                    Senml.Record(
                        SenmlNames.ECU_OTHER_STATUS_RTDBUTTON,
                        None,
                        RTDButton,
                    ),
                    Senml.Record(
                        SenmlNames.ECU_OTHER_STATUS_SDC_PRESSED,
                        None,
                        SDC_Pressed,
                    ),
                    Senml.Record(
                        SenmlNames.ECU_OTHER_STATUS_TSBUTTON,
                        None,
                        TSButton,
                    ),
                    Senml.Record(
                        SenmlNames.ECU_OTHER_STATUS_CURRENT,
                        None,
                        current,
                    ),
                    Senml.Record(
                        SenmlNames.ECU_OTHER_STATUS_INPUT_12V,
                        None,
                        input_12V,
                    ),
                    Senml.Record(
                        SenmlNames.ECU_OTHER_STATUS_PRECHARGERELAY,
                        None,
                        prechargeRelay,
                    ),
                ],
            )
