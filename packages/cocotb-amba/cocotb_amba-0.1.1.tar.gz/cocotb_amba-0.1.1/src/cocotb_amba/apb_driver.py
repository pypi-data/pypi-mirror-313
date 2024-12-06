#
# MIT License
#
# Copyright (c) 2024 nbiotcloud
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

"""
Unified Chip Design Platform - AMBA - APB Drivers.
"""

from logging import getLogger
from typing import Literal

from cocotb.handle import SimHandle
from cocotb.triggers import RisingEdge
from humannum import Hex


class APBMasterDriver:
    """APB Master bus driver."""

    def __init__(
        self,
        name: str,
        clk: SimHandle,
        rst_an: SimHandle,
        paddr: SimHandle,
        pwrite: SimHandle,
        pwdata: SimHandle,
        penable: SimHandle,
        psel: SimHandle,
        prdata: SimHandle,
        pready: SimHandle,
        pslverr: SimHandle,
        log_level: int | None = None,
    ):
        self.name = name
        self.clk = clk
        self.rst_an = rst_an
        self.paddr = paddr
        self.pwrite = pwrite
        self.pwdata = pwdata
        self.prdata = prdata
        self.penable = penable
        self.psel = psel
        self.pready = pready
        self.pslverr = pslverr
        self.addr_width = len(paddr)
        self.data_width = len(pwdata)
        self.logger = getLogger(name)
        if log_level is not None:  # important explicit check for None as 0 would be a valid value
            self.logger.setLevel(log_level)

    async def write(
        self,
        addr: int,
        data: int,
    ) -> bool:
        """APB Write."""
        await RisingEdge(self.clk)
        self.paddr.value = addr
        self.pwdata.value = data
        self.pwrite.value = 1
        self.psel.value = 1
        self.penable.value = 0
        await RisingEdge(self.clk)
        self.penable.value = 1
        await RisingEdge(self.clk)
        while self.pready == 0:
            await RisingEdge(self.clk)
        self.paddr.value = 0
        self.pwdata.value = 0xDEADDEAD
        self.pwrite.value = 0
        self.penable.value = 0
        self.psel.value = 0
        err_resp = bool(self.pslverr.value)
        err = " ERROR" if err_resp else ""
        hexaddr = str(Hex(addr, self.addr_width))
        hexdata = str(Hex(data, self.data_width))
        self.logger.info(f"=MST WRITE{err}= address: {hexaddr} data: {hexdata}")
        return err_resp

    async def read(self, addr: int) -> tuple[bool, int]:
        """APB Read."""
        self.paddr.value = addr
        self.pwrite.value = 0
        await RisingEdge(self.clk)
        self.penable.value = 1
        await RisingEdge(self.clk)
        self.psel.value = 1
        await RisingEdge(self.clk)
        while self.pready == 0:
            await RisingEdge(self.clk)
        self.penable.value = 0
        self.psel.value = 0
        rdata = self.prdata.value.integer
        err_resp = bool(self.pslverr.value)
        err = " ERROR" if err_resp else ""
        hexaddr = str(Hex(addr, self.addr_width))
        hexdata = str(Hex(rdata, self.data_width))
        self.logger.info(f"=MST READ{err}= address: {hexaddr} data: {hexdata}")
        return (err_resp, rdata)

    async def reset(self):
        """Reset APB Master."""
        self.paddr.value = 0
        self.pwrite.value = 0
        self.pwdata.value = 0


class APBSlaveDriver:
    """Active APB Slave that can respond to Master requests."""

    def __init__(
        self,
        name: str,
        clk: SimHandle,
        rst_an: SimHandle,
        paddr: SimHandle,
        pwrite: SimHandle,
        pwdata: SimHandle,
        penable: SimHandle,
        psel: SimHandle,
        prdata: SimHandle,
        pready: SimHandle,
        pslverr: SimHandle,
        pstrb: SimHandle = None,
        pready_delay: int = 0,
        size_bytes: int = 1024,
        err_addr: dict[Literal["r", "w", "rw"], list[int]] | None = None,
        log_level: int | None = None,
    ):
        """APB Slave Init."""
        self.name = name
        self.clk = clk
        self.rst_an = rst_an
        self.paddr = paddr
        self.pwrite = pwrite
        self.pwdata = pwdata
        self.prdata = prdata
        self.penable = penable
        self.psel = psel
        self.pready = pready
        self.pslverr = pslverr
        self.pstrb = pstrb
        self.err_addr = err_addr
        self.addr_width = len(paddr)
        self.data_width = len(pwdata)
        self.byte_width = len(pwdata) // 8

        self.logger = getLogger(name)
        if log_level is not None:  # important explicit check for None as 0 would be a valid value
            self.logger.setLevel(log_level)

        self.mem = bytearray(size_bytes)  # Initialize memory
        self.pready_delay = pready_delay  # Delay for PREADY signal to simulate longer access times
        self.state = 0

    def _read(self, addr: int) -> int:
        """APB Read."""
        bwidth = self.byte_width
        addr = addr & ((1 << self.addr_width) - bwidth)  # align address to data width
        bytes = self.mem[addr : addr + bwidth]
        rdata = int.from_bytes(bytes, "little")
        hexaddr = str(Hex(addr, self.addr_width))
        hexdata = str(Hex(rdata, self.data_width))
        hexbytes = ",".join(str(Hex(x, 8)) for x in bytes)
        self.logger.info(f"=SLV READ= address: {hexaddr} data: {hexdata} data (bytes): {hexbytes}")
        return rdata

    def _write(self, addr: int, data: int, strb: int) -> None:
        """APB Write."""
        bwidth = self.byte_width
        addr = addr & ((1 << self.addr_width) - bwidth)  # align address to data width
        strbs = [(strb >> i) & 1 for i in range(bwidth)]
        bytes = bytearray(int.to_bytes(data, self.byte_width, "little"))
        for b in range(bwidth):
            if not strbs[b]:
                bytes[b] = self.mem[addr + b]  # replace with read value
        hexaddr = str(Hex(addr, self.addr_width))
        hexdata = str(Hex(data, self.data_width))
        hexbytes = ",".join(str(Hex(x, 8)) for x in bytes)
        self.logger.info(f"=SLV WRITE= address: {hexaddr} data: {hexdata} data (bytes): {hexbytes} strb: {strbs}")
        self.mem[addr : addr + bwidth] = bytes

    def _check_err_addr(self, paddr: int, pwrite: int) -> bool:
        """Check for Error Address."""
        if self.err_addr is None:
            return False
        if pwrite:
            if (paddr in self.err_addr.get("w", [])) or (paddr in self.err_addr.get("rw", [])):
                return True
        elif (paddr in self.err_addr.get("r", [])) or (paddr in self.err_addr.get("rw", [])):
            return True
        return False

    async def run(self):
        """Slave Main Loop."""
        self.pready.value = 1
        self.prdata.value = 0xDEADDEAD
        self.pslverr.value = 0
        allstrb = (1 << self.byte_width) - 1
        while True:
            await RisingEdge(self.clk)
            if self.state:
                for _ in range(self.pready_delay):  # delay the answer if configured
                    self.pready.value = 0
                    await RisingEdge(self.clk)
                self.pready.value = 1
                self.pslverr.value = 0
                if (self.state == 1) and self.pwrite.value:
                    self._write(
                        self.paddr.value.integer,
                        self.pwdata.value.integer,
                        self.pstrb.value.integer if self.pstrb else allstrb,
                    )
            # Check if there's an APB request starting
            if self.psel.value and not self.penable.value:
                self.state = 1
            else:
                self.state = 0
            if self.state and self._check_err_addr(self.paddr.value, self.pwrite.value):
                acc = "WRITE" if self.pwrite.value else "READ"
                hexaddr = str(Hex(self.paddr.value.integer, self.addr_width))
                self.logger.info(f"=SLV ERROR RESP for {acc}= address: {hexaddr}")
                self.pslverr.value = 1
                self.state = 2

            if (self.state == 1) and not self.pwrite.value:
                # Handle read request (need to apply read value for next cycle)
                rdata = self._read(self.paddr.value.integer)
                self.prdata.value = rdata
            else:
                self.prdata.value = 0xDEADBEEF

    def set_pready_delay(self, delay):
        """Set pready Delay."""
        self.pready_delay = delay

    def set_data(self, data):
        """Preload Slave Memory."""
        self.mem = data

    def log_data(self, start_addr=0, end_addr=None, chunk_size=16):
        """Request logging of Slave Memory content."""
        if end_addr is None:
            end_addr = len(self.mem) - 1
        elif end_addr > len(self.mem) - 1:
            self.logger.error(
                f"=MEMORY CONTENTS= Provided end_addr {hex(end_addr)} to log_data is beyond size of slave memory."
            )
            return
        for i in range(start_addr, end_addr + 1, chunk_size):
            hexstart = str(Hex(i, self.addr_width))
            hexend = str(Hex(i + chunk_size - 1, self.addr_width))
            memcts = ",".join(str(Hex(x, 8)) for x in self.mem[i : min(i + chunk_size, end_addr + 1)])
            self.logger.info(f"=MEMORY CONTENTS= {hexstart}-{hexend} [{memcts}]")
