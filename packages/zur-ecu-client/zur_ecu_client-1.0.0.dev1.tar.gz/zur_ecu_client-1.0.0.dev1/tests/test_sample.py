from zur_ecu_client.messages import *
from zur_ecu_client.senml.senml_unit import SenmlUnit
from zur_ecu_client.senml.senml_msg_ecu import Ecu
from zur_ecu_client.senml.senml import Senml
from zur_ecu_client.senml.senml_zur_names import SenmlNames


# Test parsing of all ECU messages
def test_parse_ecu_inverter_info_msg():
    msg = Messages.parse(
        '[{"bn": "ECU", "n": "inverter", "vs": "info"},'
        '{"n": "FLon", "vb": false},'
        '{"n": "FRon", "vb": false},'
        '{"n": "RLon", "vb": false},'
        '{"n": "RRon", "vb": false},'
        '{"n": "FLdcOn", "vb": false},'
        '{"n": "FRdcOn", "vb": false},'
        '{"n": "RLdcOn", "vb": false},'
        '{"n": "RRdcOn", "vb": false},'
        '{"n": "FLready", "vb": false},'
        '{"n": "FRready", "vb": false},'
        '{"n": "RLready", "vb": false},'
        '{"n": "RRready", "vb": false}]'
    )
    assert msg == {
        SenmlNames.ECU_INVERTER_INFO_INVERTERON_FL: False,
        SenmlNames.ECU_INVERTER_INFO_INVERTERON_FR: False,
        SenmlNames.ECU_INVERTER_INFO_INVERTERON_RL: False,
        SenmlNames.ECU_INVERTER_INFO_INVERTERON_RR: False,
        SenmlNames.ECU_INVERTER_INFO_INVERTERDCON_FL: False,
        SenmlNames.ECU_INVERTER_INFO_INVERTERDCON_FR: False,
        SenmlNames.ECU_INVERTER_INFO_INVERTERDCON_RL: False,
        SenmlNames.ECU_INVERTER_INFO_INVERTERDCON_RR: False,
        SenmlNames.ECU_INVERTER_INFO_INVERTERSYSTEMREADY_FL: False,
        SenmlNames.ECU_INVERTER_INFO_INVERTERSYSTEMREADY_FR: False,
        SenmlNames.ECU_INVERTER_INFO_INVERTERSYSTEMREADY_RL: False,
        SenmlNames.ECU_INVERTER_INFO_INVERTERSYSTEMREADY_RR: False,
    }


def test_parse_ecu_inverter_status_msg():
    msg = Messages.parse(
        '[{"bn": "ECU", "n": "inverter", "vs": "status"},'
        '{"n": "FLderating", "vb": false},'
        '{"n": "FRderating", "vb": false},'
        '{"n": "RLderating", "vb": false},'
        '{"n": "RRderating", "vb": false},'
        '{"n": "FLerror", "vb": false},'
        '{"n": "FRerror", "vb": false},'
        '{"n": "RLerror", "vb": false},'
        '{"n": "RRerror", "vb": false},'
        '{"n": "FLerrorCode", "v": 0},'
        '{"n": "FRerrorCode", "v": 0},'
        '{"n": "RLerrorCode", "v": 0},'
        '{"n": "RRerrorCode", "v": 0}]'
    )
    assert msg == {
        SenmlNames.ECU_INVERTER_STATUS_INVERTERDERATNG_FL: False,
        SenmlNames.ECU_INVERTER_STATUS_INVERTERDERATNG_FR: False,
        SenmlNames.ECU_INVERTER_STATUS_INVERTERDERATNG_RL: False,
        SenmlNames.ECU_INVERTER_STATUS_INVERTERDERATNG_RR: False,
        SenmlNames.ECU_INVERTER_STATUS_INVERTERERROR_FL: False,
        SenmlNames.ECU_INVERTER_STATUS_INVERTERERROR_FR: False,
        SenmlNames.ECU_INVERTER_STATUS_INVERTERERROR_RL: False,
        SenmlNames.ECU_INVERTER_STATUS_INVERTERERROR_RR: False,
        SenmlNames.ECU_INVERTER_STATUS_INVERTERERRORCODE_FL: 0,
        SenmlNames.ECU_INVERTER_STATUS_INVERTERERRORCODE_FR: 0,
        SenmlNames.ECU_INVERTER_STATUS_INVERTERERRORCODE_RL: 0,
        SenmlNames.ECU_INVERTER_STATUS_INVERTERERRORCODE_RR: 0,
    }


def test_parse_ecu_inverter_sensor_msg():
    msg = Messages.parse(
        '[{"bn": "ECU", "n": "inverter", "vs": "sensor"},'
        '{"n": "FLtorque", "u": "N", "v": 0},'
        '{"n": "FRtorque", "u": "N", "v": 0},'
        '{"n": "RLtorque", "u": "N", "v": 0},'
        '{"n": "RRtorque", "u": "N", "v": 0},'
        '{"n": "FLinverterVoltage", "u": "V", "v": 0},'
        '{"n": "FRinverterVoltage", "u": "V", "v": 0},'
        '{"n": "RLinverterVoltage", "u": "V", "v": 0},'
        '{"n": "RRinverterVoltage", "u": "V", "v": 0},'
        '{"n": "FLinverterTemp", "u": "Cel", "v": 0},'
        '{"n": "FRinverterTemp", "u": "Cel", "v": 0},'
        '{"n": "RLinverterTemp", "u": "Cel", "v": 0},'
        '{"n": "RRinverterTemp", "u": "Cel", "v": 0},'
        '{"n": "FLspeed", "u": "1/min", "v": 0},'
        '{"n": "FRspeed", "u": "1/min", "v": 0},'
        '{"n": "RLspeed", "u": "1/min", "v": 0},'
        '{"n": "RRspeed", "u": "1/min", "v": 0}]'
    )
    assert msg == {
        SenmlNames.ECU_INVERTER_SENSOR_INVERTERACTUALTORQUE_FL: 0,
        SenmlNames.ECU_INVERTER_SENSOR_INVERTERACTUALTORQUE_FR: 0,
        SenmlNames.ECU_INVERTER_SENSOR_INVERTERACTUALTORQUE_RL: 0,
        SenmlNames.ECU_INVERTER_SENSOR_INVERTERACTUALTORQUE_RR: 0,
        SenmlNames.ECU_INVERTER_SENSOR_INVERTERSVOLTAGE_FL: 0,
        SenmlNames.ECU_INVERTER_SENSOR_INVERTERSVOLTAGE_FR: 0,
        SenmlNames.ECU_INVERTER_SENSOR_INVERTERSVOLTAGE_RL: 0,
        SenmlNames.ECU_INVERTER_SENSOR_INVERTERSVOLTAGE_RR: 0,
        SenmlNames.ECU_INVERTER_SENSOR_INVERTERTEMP_FL: 0,
        SenmlNames.ECU_INVERTER_SENSOR_INVERTERTEMP_FR: 0,
        SenmlNames.ECU_INVERTER_SENSOR_INVERTERTEMP_RL: 0,
        SenmlNames.ECU_INVERTER_SENSOR_INVERTERTEMP_RR: 0,
        SenmlNames.ECU_INVERTER_SENSOR_INVERTERACTUALRPM_FL: 0,
        SenmlNames.ECU_INVERTER_SENSOR_INVERTERACTUALRPM_FR: 0,
        SenmlNames.ECU_INVERTER_SENSOR_INVERTERACTUALRPM_RL: 0,
        SenmlNames.ECU_INVERTER_SENSOR_INVERTERACTUALRPM_RR: 0,
    }


def test_parse_ecu_accu_sensor_msg():
    msg = Messages.parse(
        '[{"bn":"ECU","n":"accu","vs":"sensor"},'
        '{"n":"accuPower","u":"A","v":0},'
        '{"n":"averagePower","u":"A","v":0},'
        '{"n":"charge","u":"%","v":0},'
        '{"n":"voltage","u":"V","v":0},'
        '{"n":"current","u":"A","v":0},'
        '{"n":"accuTemperature","u":"Cel","v":0}]'
    )
    assert msg == {
        SenmlNames.ECU_ACCU_SENSOR_ACCUPOWER: 0,
        SenmlNames.ECU_ACCU_SENSOR_AVERAGEPOWER: 0,
        SenmlNames.ECU_ACCU_SENSOR_ACCUSTATEOFCHARGE: 0,
        SenmlNames.ECU_ACCU_SENSOR_HVVOLTAGE: 0,
        SenmlNames.ECU_ACCU_SENSOR_HVCURRENT: 0,
        SenmlNames.ECU_ACCU_SENSOR_ACCUTEMPERATURE: 0,
    }


def test_parse_ecu_error_code_msg():
    msg = Messages.parse(
        '[{"bn":"ECU","n":"error","vs":"code"},{"n":"code","u":"code","v":0}]'
    )
    assert msg == {
        SenmlNames.ECU_ERROR_CODE_CODE: 0,
    }


def test_parse_ecu_driverless_control_msg():
    msg = Messages.parse(
        '[ {"bn":"ECU","n":"driverless","vs":"control"},'
        '{"n":"steeringAngle","u":"Cel","v":0},'
        '{"n":"throttle","u":"%","v":0},'
        '{"n":"brake","u":"%","v":0}]'
    )

    assert msg == {
        SenmlNames.ECU_DRIVERLESS_CONTROL_STEERINGANGLE: 0,
        SenmlNames.ECU_DRIVERLESS_CONTROL_DVTHROTTLE: 0,
        SenmlNames.ECU_DRIVERLESS_CONTROL_DVBRAKE: 0,
    }


def test_parse_ecu_motor_sensor_msg():
    msg = Messages.parse(
        '[{"bn":"ECU","n":"motor","vs":"sensor"},'
        '{"n":"FLmotorTemp","u":"Cel","v":0},'
        '{"n":"FRmotorTemp","u":"Cel","v":0},'
        '{"n":"BLmotorTemp","u":"Cel","v":0},'
        '{"n":"BRmotorTemp","u":"Cel","v":0}]'
    )
    assert msg == {
        SenmlNames.ECU_MOTOR_SENSOR_MOTORTEMP_FL: 0,
        SenmlNames.ECU_MOTOR_SENSOR_MOTORTEMP_FR: 0,
        SenmlNames.ECU_MOTOR_SENSOR_MOTORTEMP_BL: 0,
        SenmlNames.ECU_MOTOR_SENSOR_MOTORTEMP_BR: 0,
    }


def test_parse_ecu_steering_sensor_msg():
    msg = Messages.parse(
        '[{"bn":"ECU","n":"steering","vs":"sensor"},'
        '{"n":"SteeringCurrent","u":"A","v":0},'
        '{"n":"SteeringErrorCode","v":0},'
        '{"n":"SteeringPosition","v":0},'
        '{"n":"SteeringSpeed","u":"m/s","v":0},'
        '{"n":"SteeringTemperature","u":"Cel","v":0}]'
    )
    assert msg == {
        SenmlNames.ECU_STEERING_SENSOR_STEERINGCURRENT: 0,
        SenmlNames.ECU_STEERING_SENSOR_STEERINGERRORCODE: 0,
        SenmlNames.ECU_STEERING_SENSOR_STEERINGPOSITION: 0,
        SenmlNames.ECU_STEERING_SENSOR_STEERINGSPEED: 0,
        SenmlNames.ECU_STEERING_SENSOR_STEERINGTEMPERATURE: 0,
    }


def test_parse_ecu_pedal_sensor_msg():
    msg = Messages.parse(
        '[{"bn":"ECU","n":"pedal","vs":"sensor"},{"n":"FbreakPressure","u":"Pa","v":0},'
        '{"n":"RbreakPressure","u":"Pa","v":0},{"n":"LthrottleMax","u":"%","v":0},'
        '{"n":"LthrottleMin","u":"%","v":0},{"n":"LthrottleValue","u":"%","v":0},'
        '{"n":"RthrottleMax","u":"%","v":0}, {"n":"RthrottleMin","u":"%","v":0}, {"n":"RthrottleValue","u":"%","v":0}]'
    )
    assert msg == {
        SenmlNames.ECU_PEDAL_SENSOR_BREAKPRESSUREFRONT: 0,
        SenmlNames.ECU_PEDAL_SENSOR_BREAKPRESSUREREAR: 0,
        SenmlNames.ECU_PEDAL_SENSOR_THROTTLELEFTMAX: 0,
        SenmlNames.ECU_PEDAL_SENSOR_THROTTLELEFTMIN: 0,
        SenmlNames.ECU_PEDAL_SENSOR_THROTTLELEFTVALUE: 0,
        SenmlNames.ECU_PEDAL_SENSOR_THROTTLERIGHTMAX: 0,
        SenmlNames.ECU_PEDAL_SENSOR_THROTTLERIGHTMIN: 0,
        SenmlNames.ECU_PEDAL_SENSOR_THROTTLERIGHTVALUE: 0,
    }


def test_parse_ecu_other_status_msg():
    msg = Messages.parse(
        '[{"bn":"ECU","n":"other","vs":"status"},{"n":"AIRNegative","v":0},'
        '{"n":"AIRPositive","v":0},{"n":"DC_DC_24V","v":0},'
        '{"n":"DVon","v":false},{"n":"LV_Battery_24V","v":0},'
        '{"n":"RTDButton","v":0},{"n":"SDC_Pressed","v":0},'
        '{"n":"TSButton","v":0}, {"n":"current","v":0}, {"n":"current","v":0},'
        '{"n":"input_12V","v":0}, {"n":"prechargeRelay","v":0}]'
    )
    assert msg == {
        SenmlNames.ECU_OTHER_STATUS_AIRPOSITIVE: 0,
        SenmlNames.ECU_OTHER_STATUS_AIRNEGATIVE: 0,
        SenmlNames.ECU_OTHER_STATUS_DC_DC_24V: 0,
        SenmlNames.ECU_OTHER_STATUS_DVON: False,
        SenmlNames.ECU_OTHER_STATUS_LV_BATTERY_24: 0,
        SenmlNames.ECU_OTHER_STATUS_RTDBUTTON: 0,
        SenmlNames.ECU_OTHER_STATUS_SDC_PRESSED: 0,
        SenmlNames.ECU_OTHER_STATUS_TSBUTTON: 0,
        SenmlNames.ECU_OTHER_STATUS_CURRENT: 0,
        SenmlNames.ECU_OTHER_STATUS_INPUT_12V: 0,
        SenmlNames.ECU_OTHER_STATUS_PRECHARGERELAY: 0,
    }


# Test building of all ECU messages
def test_build_ecu_inverter_info_msg():
    msg = Ecu.Inverter.Info(
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
    ).get()

    assert msg == [
        {"bn": "ECU", "n": "inverter", "vs": "info"},
        {"n": "FLon", "vb": False},
        {"n": "FRon", "vb": False},
        {"n": "RLon", "vb": False},
        {"n": "RRon", "vb": False},
        {"n": "FLdcOn", "vb": False},
        {"n": "FRdcOn", "vb": False},
        {"n": "RLdcOn", "vb": False},
        {"n": "RRdcOn", "vb": False},
        {"n": "FLready", "vb": False},
        {"n": "FRready", "vb": False},
        {"n": "RLready", "vb": False},
        {"n": "RRready", "vb": False},
    ]


def test_build_ecu_inverter_status_msg():
    msg = Ecu.Inverter.Status(
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        0,
        0,
        0,
        0,
    ).get()

    assert msg == [
        {"bn": "ECU", "n": "inverter", "vs": "status"},
        {"n": "FLderating", "vb": False},
        {"n": "FRderating", "vb": False},
        {"n": "RLderating", "vb": False},
        {"n": "RRderating", "vb": False},
        {"n": "FLerror", "vb": False},
        {"n": "FRerror", "vb": False},
        {"n": "RLerror", "vb": False},
        {"n": "RRerror", "vb": False},
        {"n": "FLerrorCode", "v": 0},
        {"n": "FRerrorCode", "v": 0},
        {"n": "RLerrorCode", "v": 0},
        {"n": "RRerrorCode", "v": 0},
    ]


def test_build_ecu_inverter_sensor_msg():
    msg = Ecu.Inverter.Sensor(
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    ).get()

    assert msg == [
        {"bn": "ECU", "n": "inverter", "vs": "sensor"},
        {"n": "FLtorque", "u": "N", "v": 0},
        {"n": "FRtorque", "u": "N", "v": 0},
        {"n": "RLtorque", "u": "N", "v": 0},
        {"n": "RRtorque", "u": "N", "v": 0},
        {"n": "FLinverterVoltage", "u": "V", "v": 0},
        {"n": "FRinverterVoltage", "u": "V", "v": 0},
        {"n": "RLinverterVoltage", "u": "V", "v": 0},
        {"n": "RRinverterVoltage", "u": "V", "v": 0},
        {"n": "FLinverterTemp", "u": "Cel", "v": 0},
        {"n": "FRinverterTemp", "u": "Cel", "v": 0},
        {"n": "RLinverterTemp", "u": "Cel", "v": 0},
        {"n": "RRinverterTemp", "u": "Cel", "v": 0},
        {"n": "FLspeed", "u": "1/min", "v": 0},
        {"n": "FRspeed", "u": "1/min", "v": 0},
        {"n": "RLspeed", "u": "1/min", "v": 0},
        {"n": "RRspeed", "u": "1/min", "v": 0},
    ]


def test_build_ecu_accu_sensor_msg():
    msg = Ecu.Accu(0, 0, 0, 0, 0, 0).get()
    assert msg == [
        {"bn": "ECU", "n": "accu", "vs": "sensor"},
        {"n": "accuPower", "u": "A", "v": 0},
        {"n": "averagePower", "u": "A", "v": 0},
        {"n": "charge", "u": "%", "v": 0},
        {"n": "voltage", "u": "V", "v": 0},
        {"n": "current", "u": "A", "v": 0},
        {"n": "accuTemperature", "u": "Cel", "v": 0},
    ]


def test_build_ecu_error_code_msg():
    msg = Ecu.Error(0).get()
    assert msg == [{"bn": "ECU", "n": "error", "vs": "code"}, {"n": "code", "v": 0}]


def test_build_ecu_driverless_control_msg():
    msg = Ecu.Driverless(0, 0, 0).get()
    assert msg == [
        {"bn": "ECU", "n": "driverless", "vs": "control"},
        {"n": "steeringAngle", "u": "Cel", "v": 0},
        {"n": "throttle", "u": "%", "v": 0},
        {"n": "brake", "u": "%", "v": 0},
    ]


def test_build_ecu_motor_sensor_msg():
    msg = Ecu.Motor(0, 0, 0, 0).get()
    assert msg == [
        {"bn": "ECU", "n": "motor", "vs": "sensor"},
        {"n": "FLmotorTemp", "u": "Cel", "v": 0},
        {"n": "FRmotorTemp", "u": "Cel", "v": 0},
        {"n": "BLmotorTemp", "u": "Cel", "v": 0},
        {"n": "BRmotorTemp", "u": "Cel", "v": 0},
    ]


def test_build_ecu_steering_sensor_msg():
    msg = Ecu.Steering(0, 0, 0, 0, 0).get()
    assert msg == [
        {"bn": "ECU", "n": "steering", "vs": "sensor"},
        {"n": "SteeringCurrent", "u": "A", "v": 0},
        {"n": "SteeringErrorCode", "v": 0},
        {"n": "SteeringPosition", "v": 0},
        {"n": "SteeringSpeed", "u": "m/s", "v": 0},
        {"n": "SteeringTemperature", "u": "Cel", "v": 0},
    ]


def test_build_ecu_pedal_sensor_msg():
    msg = Ecu.Pedal(0, 0, 0, 0, 0, 0, 0, 0).get()
    assert msg == [
        {"bn": "ECU", "n": "pedal", "vs": "sensor"},
        {"n": "FbreakPressure", "u": "Pa", "v": 0},
        {"n": "RbreakPressure", "u": "Pa", "v": 0},
        {"n": "LthrottleMax", "u": "%", "v": 0},
        {"n": "LthrottleMin", "u": "%", "v": 0},
        {"n": "LthrottleValue", "u": "%", "v": 0},
        {"n": "RthrottleMax", "u": "%", "v": 0},
        {"n": "RthrottleMin", "u": "%", "v": 0},
        {"n": "RthrottleValue", "u": "%", "v": 0},
    ]


def test_build_ecu_other_status_msg():
    msg = Ecu.Other(0, 0, 0, False, 0, 0, 0, 0, 0, 0, 0).get()
    assert msg == [
        {"bn": "ECU", "n": "other", "vs": "status"},
        {"n": "AIRNegative", "v": 0},
        {"n": "AIRPositive", "v": 0},
        {"n": "DC_DC_24V", "v": 0},
        {"n": "DVon", "vb": False},
        {"n": "LV_Battery_24V", "v": 0},
        {"n": "RTDButton", "v": 0},
        {"n": "SDC_Pressed", "v": 0},
        {"n": "TSButton", "v": 0},
        {"n": "current", "v": 0},
        {"n": "input_12V", "v": 0},
        {"n": "prechargeRelay", "v": 0},
    ]
