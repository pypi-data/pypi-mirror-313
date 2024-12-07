#!/usr/bin/env python

import argparse
import asyncio
import sys
from pyituran import Ituran
from pyituran.exceptions import IturanApiError, IturanAuthError


async def async_main(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(
        description="Ituran command line tool.\n"
        + "When executing this tool, please provide a phone number on"
        + "first use or a mobile ID if already authenticated",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--id-number",
        action="store",
        dest="id_number",
        default=None,
        help="ID number of the account owner",
        required=True,
    )
    parser.add_argument(
        "--phone-number",
        action="store",
        dest="phone_number",
        default="",
        help="Phone number of the account owner, required for OTP",
    )
    parser.add_argument(
        "--mobile-id",
        action="store",
        dest="mobile_id",
        default=None,
        help="A unique, 16 hex-digit, ID for this client. "
        + "Once authenticated via OTP, it must remain constant",
    )
    args = parser.parse_args(args)

    if not (args.phone_number or args.mobile_id):
        parser.error("Must provide either a phone number or a mobile ID")

    ituran = Ituran(args.id_number, args.phone_number, args.mobile_id)
    if not await ituran.is_authenticated():
        print("The provided credentials aren't authenticated.")
        response = input(
            f"Would you like to authenticate now with ID '{args.id_number}'"
            + f" and phone number '{args.phone_number}' (y/n)? "
        )
        if response != "y":
            return
        try:
            await ituran.request_otp()
        except IturanAuthError:
            print("Failed requesting OTP, please verify ID and phone number")
            return
        except IturanApiError:
            print("Error accessing Ituran service, please try again")
            return
        print("OTP request sent.")
        while True:
            otp = input("Please input the received one-time code: ")
            try:
                await ituran.authenticate(otp)
            except IturanAuthError:
                print("Incorrect code, please try again.")
            except IturanApiError:
                print("Error accessing Ituran service, please try again")
            else:
                break
        print(
            "Success!\nPlease keep the following mobile ID "
            + f"for future use: {ituran.mobile_id}"
        )

    vehicles = await ituran.get_vehicles()
    for vehicle in vehicles:
        print(
            f"License plate: {vehicle.license_plate}:\n"
            + f"\tMake: {vehicle.make}\n"
            + f"\tModel: {vehicle.model}\n"
            + f"\tLocation: {vehicle.gps_coordinates}\n"
            + f"\tAddress: {vehicle.address}\n"
            + f"\tHeading: {vehicle.heading}\n"
            + f"\tSpeed: {vehicle.speed}\n"
            + f"\tMileage: {vehicle.mileage}\n"
            + f"\tBattery voltage: {vehicle.battery_voltage}\n"
            + f"\tLast update: {vehicle.last_update}\n"
        )


def main(args=None):
    asyncio.run(async_main(args))


if __name__ == "__main__":
    main()  # pragma: no cover
