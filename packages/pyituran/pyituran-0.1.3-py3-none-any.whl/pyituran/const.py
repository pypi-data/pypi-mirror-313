"""Ituran library constants."""

DOMAIN = "https://www.ituran.com"
SOAP_SERVICES = DOMAIN + "/SoapService"
ACTIVATION_URL = SOAP_SERVICES + "/APPApi.asmx/AppActivation"
OTP_VERIFICATION_URL = (
    SOAP_SERVICES + "/ituran4all.asmx/AppSerializationRequest"
)
ITURAN_GET_VEHICLES_URL = (
    DOMAIN + "/ituranmobileservice/mobileservice.asmx/GetUserPlatforms"
)

TEMP_NAMESPACE = "http://tempuri.org/"
XML_RESPONSE_STATUS = f"{{{TEMP_NAMESPACE}}}ResponseStatus"

IMS_NAMESPACE = "http://www.ituran.com/IturanMobileService"
XML_RETURN_CODE = f"{{{IMS_NAMESPACE}}}ReturnCode"
XML_ERROR_DESCRIPTION = f"{{{IMS_NAMESPACE}}}ErrorDescription"
XML_VEHICLES_LIST = f"{{{IMS_NAMESPACE}}}VehList"
XML_VEHICLE_MODEL = f"{{{IMS_NAMESPACE}}}Model"
XML_VEHICLE_MAKE = f"{{{IMS_NAMESPACE}}}Make"
XML_VEHICLE_PLATE = f"{{{IMS_NAMESPACE}}}Plate"
XML_VEHICLE_LATITUTE = f"{{{IMS_NAMESPACE}}}Lat"
XML_VEHICLE_LONGITUDE = f"{{{IMS_NAMESPACE}}}Lon"
XML_VEHICLE_ADDRESS = f"{{{IMS_NAMESPACE}}}Address"
XML_VEHICLE_SPEED = f"{{{IMS_NAMESPACE}}}Speed"
XML_VEHICLE_HEADING = f"{{{IMS_NAMESPACE}}}Head"
XML_VEHICLE_LAST_MILEAGE = f"{{{IMS_NAMESPACE}}}LastMileage"
XML_VEHICLE_BATTERY_VOLTAGE = f"{{{IMS_NAMESPACE}}}BatteryVoltage"
XML_VEHICLE_UPDATE_DATE = f"{{{IMS_NAMESPACE}}}Date"

ERROR_OK = "ok"
ERROR_INVALID_CREDENTIALS = "IncorrectUserNameOrPassword"
ERROR_WRONG_OTP_CODE = "Wrong OTPcode"
