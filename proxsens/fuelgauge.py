"""
A library for reading from a MAX17043 lithium battery fuel gauge over I2C

"""
from __future__ import print_function

import Adafruit_I2C

import argparse
import datetime
import time

I2C_BUS = 1
FUEL_ADDRESS = 0x36

VCELL_REGISTER = 0x02
SOC_REGISTER = 0x04
MODE_REGISTER = 0x06
VERSION_REGISTER = 0x08
CONFIG_REGISTER = 0x0C
COMMAND_REGISTER = 0xFE

wire = Adafruit_I2C.Adafruit_I2C(0x36, busnum=I2C_BUS)


def writeReset():
    """ reset the fuel guage """
    return writeRegister(COMMAND_REGISTER, 0x00, 0x54)


def writeQuickStart():
    """ set the fuel guage to quick start mode """
    return writeRegister(MODE_REGISTER, 0x40, 0x00)


def writeAlertThreshold(threshold):
    """ set the alert threshold % between 1 and 32 """
    msb, lsb = readRegister(CONFIG_REGISTER)
    threshold = max(1, min(32, threshold))  # threshold between 1 & 32
    threshold = 32 - threshold
    return writeRegister(CONFIG_REGISTER, msb, (lsb & 0xE0) | threshold)


def writeAlertReset():
    """ reset the alert bit to 0 """
    msb, lsb = readRegister(CONFIG_REGISTER)
    return writeRegister(CONFIG_REGISTER, msb, (lsb & ~(0x20)))


def readVCell():
    """ read the voltage of the battery """
    msb, lsb = readRegister(VCELL_REGISTER)
    value = (msb << 4) | (lsb >> 4)
    return mapValue(value, 0x000, 0xFFF, 0, 50000) / 10000.0


def readSOC():
    """ read the "state of charge" (% remaining) of the battery """
    msb, lsb = readRegister(SOC_REGISTER)
    return msb + lsb / 256.0




def readRegister(address):
    """ utility function for reading 2 bytes from a register address """
    return wire.readList(address, 2)


def writeRegister(address, msb, lsb):
    """ utility function for writing 2 bytes to a register address """
    return wire.writeList(address, [msb, lsb])


def mapValue(x, in_min, in_max, out_min, out_max):
    """ utility function for mapping a value from one range to another """
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min



def mma(observation, mma_yesterday=0, n=0):
    """
    Compute the modified moving average for a series of observations.

    Formally:

        MMAtoday = (((N-1) * MMAyesterday) + observation) / N

        (which is, in short, an exponential moving average with alpha=1/N)

    """
    if n == 0:
        return observation
    return (((n - 1) * mma_yesterday) + observation) / (n)


def split_seconds(seconds):
    """ split seconds into hours, minutes, and seconds """
    seconds = int(seconds)
    if seconds < 0:
        return 0, 0, 0
    hours = seconds / 3600
    seconds = seconds % 3600
    minutes = seconds / 60
    seconds = seconds % 60
    return hours, minutes, seconds


