#!/usr/bin/env python
############################################################################
# INTEL CONFIDENTIAL - DO NOT RE-DISTRUBUTE
# Copyright 2013 Intel Corporation All Rights Reserved.
#
# The source code contained or described herein and all documents related
# to the source code ("Material") are owned by Intel Corporation or its
# suppliers or licensors. Title to the Material remains with Intel Corp-
# oration or its suppliers and licensors. The Material may contain trade
# secrets and proprietary and confidential information of Intel Corpor-
# ation and its suppliers and licensors, and is protected by worldwide
# copyright and trade secret laws and treaty provisions. No part of the
# Material may be used, copied, reproduced, modified, published, uploaded,
# posted, transmitted, distributed, or disclosed in any way without
# Intel"s prior express written permission.
#
# No license under any patent, copyright, trade secret or other intellect-
# ual property right is granted to or conferred upon you by disclosure or
# delivery of the Materials, either expressly, by implication, inducement,
# estoppel or otherwise. Any license under such intellectual property
# rights must be express and approved by Intel in writing.
############################################################################

import os,string
#import namednodes
from namednodes import sv

#namednodes.sv.initialize()
sv.initialize()
#touch = namednodes.sv.touch0

# itp = itpii.baseaccess()
from __main__ import itp,pcd
try:
	touch = sv.socket0.pcd
except:
	print ("ERROR ")
#from registerReadWrite import *

#Write_Value = 0x12345678 #Need to design to make a set of values to be written
#THC_M_PRT_SW_SEQ_CNTRL = 0x1040
#THC_M_PRT_SW_SEQ_STS = 0x1044
#THC_M_PRT_SW_SEQ_DATA0_ADDR = 0x1048
#THC_M_PRT_SPI_CFG = 0x1010
#Address = 0x0   #Should read from the cmd line

READ = 0x4
WRITE = 0x6  # should input bulk write with 0x8
#ByteCountRead = 0x4
#ByteCountWrite = 0x4
WriteType = { "Single": 0x0, "Dual" : 0x1, "Quad" : 0x2, "QuadParrellel" :0x3}
WriteMode = "Quad" #should read from cmd line
ReadType = { "Single": 0x0, "Dual" : 0x1, "Quad" : 0x2, "QuadParrellel" :0x3}
ReadMode = "Quad" #should read from cmd line
SPIFrequency = { "42MHz":0x3, "30MHz": 0x4, "24MHz" : 0x5, "20MHz" : 0x6, "17MHz" :0x7 }
SPIReadFrequency = "42MHz"   #default values
SPIWriteFrequency = "42MHz"  #default values

def Init_DataRegisters(Value=0):
	touch.thc0.port.mem.thc_m_prt_sw_seq_data1=Value
	touch.thc0.port.mem.thc_m_prt_sw_seq_data2=Value
	touch.thc0.port.mem.thc_m_prt_sw_seq_data3=Value
	touch.thc0.port.mem.thc_m_prt_sw_seq_data4=Value
	touch.thc0.port.mem.thc_m_prt_sw_seq_data5=Value
	touch.thc0.port.mem.thc_m_prt_sw_seq_data6=Value
	touch.thc0.port.mem.thc_m_prt_sw_seq_data7=Value
	touch.thc0.port.mem.thc_m_prt_sw_seq_data8=Value
	touch.thc0.port.mem.thc_m_prt_sw_seq_data9=Value
	touch.thc0.port.mem.thc_m_prt_sw_seq_data10=Value
	touch.thc0.port.mem.thc_m_prt_sw_seq_data11=Value
	touch.thc0.port.mem.thc_m_prt_sw_seq_data12=Value
	touch.thc0.port.mem.thc_m_prt_sw_seq_data13=Value
	touch.thc0.port.mem.thc_m_prt_sw_seq_data14=Value
	touch.thc0.port.mem.thc_m_prt_sw_seq_data15=Value
	touch.thc0.port.mem.thc_m_prt_sw_seq_data16=Value
	print(("thc_m_prt_sw_seq_data1= %x" %touch.thc0.port.mem.thc_m_prt_sw_seq_data1))
	print(("thc_m_prt_sw_seq_data2= %x" %touch.thc0.port.mem.thc_m_prt_sw_seq_data2))
	print(("thc_m_prt_sw_seq_data3= %x" %touch.thc0.port.mem.thc_m_prt_sw_seq_data3))
	print(("thc_m_prt_sw_seq_data4= %x" %touch.thc0.port.mem.thc_m_prt_sw_seq_data4))
	print(("thc_m_prt_sw_seq_data5= %x" %touch.thc0.port.mem.thc_m_prt_sw_seq_data5))
	print(("thc_m_prt_sw_seq_data6= %x" %touch.thc0.port.mem.thc_m_prt_sw_seq_data6))
	print(("thc_m_prt_sw_seq_data7= %x" %touch.thc0.port.mem.thc_m_prt_sw_seq_data7))
	print(("thc_m_prt_sw_seq_data8= %x" %touch.thc0.port.mem.thc_m_prt_sw_seq_data8))
	print(("thc_m_prt_sw_seq_data9= %x" %touch.thc0.port.mem.thc_m_prt_sw_seq_data9))
	print(("thc_m_prt_sw_seq_data10= %x" %touch.thc0.port.mem.thc_m_prt_sw_seq_data10))
	print(("thc_m_prt_sw_seq_data11= %x" %touch.thc0.port.mem.thc_m_prt_sw_seq_data11))
	print(("thc_m_prt_sw_seq_data12= %x" %touch.thc0.port.mem.thc_m_prt_sw_seq_data12))
	print(("thc_m_prt_sw_seq_data13= %x" %touch.thc0.port.mem.thc_m_prt_sw_seq_data13))
	print(("thc_m_prt_sw_seq_data14= %x" %touch.thc0.port.mem.thc_m_prt_sw_seq_data14))
	print(("thc_m_prt_sw_seq_data15= %x" %touch.thc0.port.mem.thc_m_prt_sw_seq_data15))
	print(("thc_m_prt_sw_seq_data16= %x" %touch.thc0.port.mem.thc_m_prt_sw_seq_data16))

def pollSTSAndPrint(Result):
	count = 0
	#rRdVal = regReadMMIO(THC_M_PRT_SW_SEQ_STS)
	rRdVal = touch.thc0.port.mem.thc_m_prt_sw_seq_sts
	while(Result) :
		rRdVal = touch.thc0.port.mem.thc_m_prt_sw_seq_sts
		if ((rRdVal & 3 == 1) and ((rRdVal & 8) == 0)):
			break
		count = count + 1
		if(count == 100): # Can have a threshold value
			print("Error: Pooling for the status Failed.")
			break
	print(("The value of the Register is", hex(rRdVal)))

	### THC Port 0 Read / Write:##################

def PIO_Read(Address,ByteCountRead):

	#Driver strenght regs
##	pcd.gpio.com1.sb.gpio_mem_1.fam_rcomp_a_dw0_thc0_gspi0.pdstrval = 0x0 #eston son de clk
##	pcd.gpio.com1.sb.gpio_mem_1.fam_rcomp_a_dw0_thc0_gspi0.pustrval = 0x0 #eston son de clk
	#pcd.gpio.com1.sb.gpio_mem_1.fam_rcomp_b_dw0_thc0_gspi0.pdstrval
	#pcd.gpio.com1.sb.gpio_mem_1.fam_rcomp_b_dw0_thc0_gspi0.pustrval
	print("## Step 1: Initialize Data Registers")
	Init_DataRegisters(0) ## Step 1: Initialize Data Registers

	print("## Step 2: Clear Status fields")
	touch.thc0.port.mem.thc_m_prt_sw_seq_sts = 0x3  ## Step 2: Clear Status fields

	#if ReadMode != "Single":SPI read Frequency to 17MHz
	print(("Setting the Read mode to", ReadMode))
	rRdVal = touch.thc0.port.mem.thc_m_prt_spi_cfg
	WrtVal = ((rRdVal&0xFFFFFF83)|(ReadType[ReadMode]<<2)|(SPIFrequency[SPIReadFrequency]<<4))
	touch.thc0.port.mem.thc_m_prt_spi_cfg = WrtVal
	touch.thc0.port.mem.thc_m_prt_spi_cfg.spi_twmode = WriteType[WriteMode]

	print("## Step 3,4: Program THC_M_PRT_SW_SEQ_CNTRL.THC_SS_BC[15:0] with Length of read.")
	WrtVal = ByteCountRead<<16 | READ <<8
	touch.thc0.port.mem.thc_m_prt_sw_seq_cntrl = WrtVal

	print("## Step 5: Program THC_M_PRT_SW_SEQ_DATA0.THC_SW_SEQ_DATA0_ADDR[31:0] with 0")
	touch.thc0.port.mem.thc_m_prt_sw_seq_data0_addr = Address

	## Step 6: Disable Interrupts.. Done in Step 2
	print("## Step 6: Disable Interrupts.. Done in Step 2")
	pollSTSAndPrint(False)

	## Step 7: Set THC_M_PRT_SW_SEQ_CNTRL.TSSGO=1
	print("## Step 7: Set THC_M_PRT_SW_SEQ_CNTRL.TSSGO=1")
	WrtVal = ByteCountRead<<16 | READ <<8 | 1
	touch.thc0.port.mem.thc_m_prt_sw_seq_cntrl = WrtVal

	## echo "Go bit set.."
	## Print Status register before setting go bit
	print("## Print Status register before setting go bit")
	pollSTSAndPrint(True)
	#print "touch.thc0.port.mem.thc_m_prt_sw_seq_data1 = " % touch.thc0.port.mem.thc_m_prt_sw_seq_data1

def PIO_Write(Address,ByteCountWrite, Write_Value = 0x12345678):


	#Driver strenght regs
##	pcd.gpio.com1.sb.gpio_mem_1.fam_rcomp_a_dw0_thc0_gspi0.pdstrval = 0x0 #eston son de clk
##	pcd.gpio.com1.sb.gpio_mem_1.fam_rcomp_a_dw0_thc0_gspi0.pustrval = 0x0 #eston son de clk

	#Configure the GPIO pins
	#touch.gpio.com4.sb.pad_cfg_dw0_gppc_e_1.pmode = 1
	#touch.gpio.com4.sb.pad_cfg_dw0_gppc_e_2.pmode = 1
	#touch.gpio.com4.sb.pad_cfg_dw0_gppc_e_10.pmode = 1
	#touch.gpio.com4.sb.pad_cfg_dw0_gppc_e_6.pmode = 1
	#touch.gpio.com4.sb.pad_cfg_dw0_gppc_e_11.pmode = 1
	#touch.gpio.com4.sb.pad_cfg_dw0_gppc_e_12.pmode = 1
	#touch.gpio.com4.sb.pad_cfg_dw0_gppc_e_13.pmode = 1
	#touch.gpio.com4.sb.pad_cfg_dw0_gppc_e_17.pmode = 1
	#touch.thc0.port.mem.thc_m_prt_spi_cfg.spi_tcwf = 6 # clock divider settings



	print("## Step 1: Initialize Data Registers")
	Init_DataRegisters(Write_Value) ## Step 1: Initialize Data Registers

	print("## Step 2: Clear Status fields") # Step 2: Clear Status fields
	touch.thc0.port.mem.thc_m_prt_sw_seq_sts = 0x3
	#if SPI Write frequency mode != "17Mhz":
	#rRdVal = regReadMMIO(THC_M_PRT_SPI_CFG)
	#regWriteMMIO(THC_M_PRT_SPI_CFG,(rRdVal&0xFF8FFFFF)|SPIFrequency[SPIWriteFrequency]<<20)
	rRdVal = touch.thc0.port.mem.thc_m_prt_spi_cfg
	WrtVal = ((rRdVal&0xFF8FFFFF)|(SPIFrequency[SPIWriteFrequency]<<20))
	touch.thc0.port.mem.thc_m_prt_spi_cfg = WrtVal
	print(WrtVal)
	print("## Step 3,4: Program THC_M_PRT_SW_SEQ_CNTRL.THC_SS_BC[15:0] with Length of read.")
	WrtVal = ByteCountWrite<<16 | WRITE <<8
	touch.thc0.port.mem.thc_m_prt_sw_seq_cntrl = WrtVal

	print("## Step 5: Program THC_M_PRT_SW_SEQ_DATA0.THC_SW_SEQ_DATA0_ADDR[31:0] with 0")
	touch.thc0.port.mem.thc_m_prt_sw_seq_data0_addr = Address

	## Step 6: Disable Interrupts.. Done in Step 2
	print("## Step 6: Disable Interrupts.. Done in Step 2")
	pollSTSAndPrint(False)

	## Step 7: Set THC_M_PRT_SW_SEQ_CNTRL.TSSGO=1
	print("## Step 7: Set THC_M_PRT_SW_SEQ_CNTRL.TSSGO=1")
	WrtVal = ByteCountWrite<<16 | WRITE <<8 | 1
	touch.thc0.port.mem.thc_m_prt_sw_seq_cntrl = WrtVal

	## echo "Go bit set.."
	## Print Status register before setting go bit
	print("## Print Status register before setting go bit")
	pollSTSAndPrint(True)

if __name__ == "__main__":
	PIO_Write(0x0, 4, 0x123465789)
	PIO_Read(0x0, 4)
