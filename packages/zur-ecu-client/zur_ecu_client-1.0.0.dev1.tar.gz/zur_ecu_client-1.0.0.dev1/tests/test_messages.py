from zur_ecu_client.messages import Acknowledgment, Data, Messages
from zur_ecu_client.senml.senml import Senml
from zur_ecu_client.senml.senml_zur_names import SenmlNames


def test_incoming_parser():
    msg = Messages.parse(
        """
        [
            [
                {"bn":"ECU","n":"pedal","vs":"sensor"}
            ],
            [
                {"bn":"ECU","n":"other","vs":"status"},
                {"n":"AIRPositive","u":"","v":0},
                {"n":"AIRNegative","u":"","v":0},
                {"n":"DC_DC_24V","u":"","v":0},
                {"n":"DVon","vb":false},
                {"n":"LV_Battery_24V","u":"","v":0},
                {"n":"RTDButton","u":"","v":0},
                {"n":"SDC_Pressed","u":"","v":0},
                {"n":"TSButton","u":"","v":0}, 
                {"n":"current","u":"","v":0}, 
                {"n":"input_12V","u":"","v":0}, 
                {"n":"prechargeRelay","u":"","v":0}
            ]
        ]"""
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


def test_incoming_parser_single_list_message():
    msg = Messages.parse(
        """
            [
                {"bn":"ECU","n":"steering","vs":"sensor"},
                {"n":"SteeringCurrent","u":"A","v":0},
                {"n":"SteeringErrorCode","v":0},
                {"n":"SteeringPosition","u":"lat","v":0},
                {"n":"SteeringSpeed","u":"m/s","v":0}, 
                {"n":"SteeringTemperature","u":"Cel","v":0}
            ]
        """
    )

    assert msg == {
        SenmlNames.ECU_STEERING_SENSOR_STEERINGCURRENT: 0,
        SenmlNames.ECU_STEERING_SENSOR_STEERINGERRORCODE: 0,
        SenmlNames.ECU_STEERING_SENSOR_STEERINGPOSITION: 0,
        SenmlNames.ECU_STEERING_SENSOR_STEERINGSPEED: 0,
        SenmlNames.ECU_STEERING_SENSOR_STEERINGTEMPERATURE: 0,
    }
