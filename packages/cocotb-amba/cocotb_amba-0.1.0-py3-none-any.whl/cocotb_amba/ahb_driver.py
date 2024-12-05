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
Unified Chip Design Platform - AMBA - AHB Drivers.
"""

from collections.abc import Iterable
from enum import IntEnum
from logging import getLogger
from typing import Literal

from cocotb.handle import SimHandle
from cocotb.triggers import RisingEdge
from humannum import Hex


class BurstType(IntEnum):
    """HBURST encoding as per AHB spec."""

    SINGLE = 0  # Single transfer
    INCR = 1  # Unknown length burst
    WRAP4 = 2  # Four-beat wrap burst
    INCR4 = 3  # Four-beat incrementing burst
    WRAP8 = 4  # Eight-beat wrap burst
    INCR8 = 5  # Eight-beat incrementing burst
    WRAP16 = 6  # Sixteen-beat wrap burst
    INCR16 = 7  # Sixteen-beat incrementing burst


class TransType(IntEnum):
    """HTRANS encoding as per AHB spec."""

    IDLE = 0  # No transfer
    BUSY = 1  # Busy transfer
    NONSEQ = 2  # Non-sequential transfer
    SEQ = 3  # Sequential transfer


class SizeType(IntEnum):
    """HSIZE encoding as per AHB spec."""

    BYTE = 0  # 8-bit
    HALFWORD = 1  # 16-bit
    WORD = 2  # 32-bit
    DOUBLEWORD = 3  # 64-bit
    WORD4 = 4  # 128-bit
    WORD8 = 5  # 256-bit
    WORD16 = 6  # 512-bit
    WORD32 = 7  # 1024-bit


def _prep_addr_iter(addr: int, burst_length: int, size: SizeType, burst_type=BurstType) -> tuple[int, int, int, int]:
    """Prepare Address Iterations."""
    match burst_type:
        case BurstType.INCR16 | BurstType.WRAP16:
            mask = (1 << (size + 4)) - 1
            len = 16
        case BurstType.INCR8 | BurstType.WRAP8:
            mask = (1 << (size + 3)) - 1
            len = 8
        case BurstType.INCR4 | BurstType.WRAP4:
            mask = (1 << (size + 2)) - 1
            len = 4
        case BurstType.INCR:
            mask = -1
            len = burst_length
        case BurstType.SINGLE:
            mask = -1
            len = 1
    base = addr & ~mask
    offs = addr & mask
    return (base, offs, mask, len)


def _check_bus_acc(data_width: int, addr: int, offs: int, size: SizeType, burst_type: BurstType) -> None:
    """Check AHB Bus Access."""
    assert data_width >= (8 << size), f"Size argument {size!r} -> {8<<size} too big for data width of {data_width}!"
    assert (addr & ((1 << size) - 1)) == 0, f"Address {addr:x} is not aligned to size argument {size!r}!"
    assert (burst_type not in (BurstType.INCR16, BurstType.INCR8, BurstType.INCR4)) or (
        offs == 0
    ), f"Address {addr:x} is not aligned to BurstType {burst_type!r} at size {size!r}!"


def _bottomless(value: int) -> Iterable[int]:
    """Bottomless Iterator."""
    while True:
        yield value


class SlaveFsmState(IntEnum):
    """Internal AHB Slave State."""

    IDLE = 0
    ACTIVE = 1


class AHBMasterDriver:
    """AHB Master bus driver."""

    def __init__(
        self,
        name: str,
        clk: SimHandle,
        rst_an: SimHandle,
        haddr: SimHandle,
        hwrite: SimHandle,
        hwdata: SimHandle,
        htrans: SimHandle,
        hburst: SimHandle,
        hsize: SimHandle,
        hrdata: SimHandle,
        hready: SimHandle,
        hresp: SimHandle,
        hsel: SimHandle = None,
        hprot: SimHandle = None,
        hwstrb: SimHandle = None,
        hreadyout: SimHandle = None,
        hnonsec: SimHandle = None,
        hmastlock: SimHandle = None,
        hexcl: SimHandle = None,
        hmaster: SimHandle = None,
        hexokay: SimHandle = None,
        hauser: SimHandle = None,
        log_level: int | None = None,
    ):
        self.name = name
        self.clk = clk
        self.rst_an = rst_an
        self.haddr = haddr
        self.hwrite = hwrite
        self.hwdata = hwdata
        self.htrans = htrans
        self.hburst = hburst
        self.hsize = hsize
        self.hrdata = hrdata
        self.hready = hready
        self.hresp = hresp
        # optional signals:
        self.hsel = hsel
        self.hprot = hprot
        self.hwstrb = hwstrb
        self.hreadyout = hreadyout
        self.hnonsec = hnonsec
        self.hmastlock = hmastlock
        self.hexcl = hexcl
        self.hmaster = hmaster
        self.hexokay = hexokay
        self.hauser = hauser
        self.addr_width = len(haddr)
        self.data_width = len(hwdata)

        self.logger = getLogger(name)
        if log_level is not None:  # important explicit check for None as 0 would be a valid value
            self.logger.setLevel(log_level)

    async def write(  # noqa: C901, PLR0912
        self,
        addr: int,
        data: int | Iterable,
        wstrb: int | Iterable | None = None,
        size: SizeType = SizeType.WORD,
        burst_length: int = 1,
        burst_type: BurstType = BurstType.SINGLE,
        hauser: int = 0,
        hmaster: int = 5,
    ) -> bool:
        """AHB Write (Burst)."""
        base, offs, mask, burst_length = _prep_addr_iter(
            addr=addr, burst_length=burst_length, size=size, burst_type=burst_type
        )
        _check_bus_acc(data_width=self.data_width, addr=addr, offs=offs, size=size, burst_type=burst_type)

        err_resp = False
        if isinstance(data, int):
            log_data = [data]
            data = iter((data,))
        else:
            log_data = list(data)
            data = iter(data)
        allstrb = (1 << (1 << size)) - 1
        if wstrb is None:
            wstrb = iter(_bottomless(allstrb))
        elif isinstance(wstrb, int):
            wstrb = iter(_bottomless(wstrb))
        else:
            wstrb = iter(wstrb)
        shift_mask = self.data_width - 1
        self.haddr.value = base + offs
        if self.hauser:
            self.hauser.value = hauser
        if self.hmaster:
            self.hmaster.value = hmaster
        self.hwdata.value = 0xDEADDEAD
        if self.hwstrb:
            self.hwstrb.value = 0
        self.hwrite.value = 1
        if self.hsel:
            self.hsel.value = 1
        if self.hreadyout:
            self.hreadyout.value = 1
        self.htrans.value = TransType.NONSEQ
        self.hburst.value = burst_type
        self.hsize.value = size
        await RisingEdge(self.clk)
        if self.hreadyout:
            self.hreadyout = self.hready
        for _ in range(burst_length - 1):
            self.htrans.value = TransType.SEQ
            self.hwdata.value = next(data) << ((offs << 3) & shift_mask)
            if self.hwstrb:
                self.hwstrb.value = next(wstrb) << (offs & (shift_mask >> 3))
            offs = (offs + (1 << size)) & mask
            self.haddr.value = base + offs
            if self.hauser:
                self.hauser.value = hauser
            if self.hmaster:
                self.hmaster.value = hmaster
            await RisingEdge(self.clk)
            while self.hready == 0:
                await RisingEdge(self.clk)
            if self.hresp.value:
                err_resp = True
        if self.hsel:
            self.hsel.value = 0
        self.haddr.value = 0
        if self.hmaster:
            self.hmaster.value = 0
        self.hwdata.value = next(data) << ((offs << 3) & shift_mask)
        if self.hwstrb:
            self.hwstrb.value = next(wstrb) << (offs & (shift_mask >> 3))
        self.hwrite.value = 0
        self.htrans.value = TransType.IDLE
        self.hburst.value = BurstType.SINGLE
        self.hsize.value = SizeType.BYTE
        await RisingEdge(self.clk)
        if self.hreadyout:
            self.hreadyout = self.hready
        while self.hready == 0:
            await RisingEdge(self.clk)
        if self.hresp.value:
            err_resp = True
        self.hwdata.value = 0xDEADDEAD
        if self.hwstrb:
            self.hwstrb.value = 0
        self._info_log(
            rw="WRITE",
            addr=addr,
            burst_type=burst_type,
            burst_length=burst_length,
            size=size,
            data=log_data,
            err_resp=err_resp,
        )
        return err_resp

    async def read(  # noqa: C901
        self,
        addr: int,
        burst_length: int = 1,
        size: SizeType = SizeType.WORD,
        burst_type: BurstType = BurstType.SINGLE,
        hauser: int = 0,
        hmaster: int = 0,
    ) -> tuple[bool, tuple[int]]:
        """AHB Read (Burst)."""
        base, offs, mask, burst_length = _prep_addr_iter(
            addr=addr, burst_length=burst_length, size=size, burst_type=burst_type
        )
        _check_bus_acc(data_width=self.data_width, addr=addr, offs=offs, size=size, burst_type=burst_type)

        rdata = []
        err_resp = False
        poffs = offs
        shift_mask = self.data_width - 1
        szmsk = (1 << (8 << size)) - 1
        self.haddr.value = base + offs
        if self.hauser:
            self.hauser.value = hauser
        if self.hmaster:
            self.hmaster.value = hmaster
        if self.hsel:
            self.hsel.value = 1
        self.hwrite.value = 0
        self.htrans.value = TransType.NONSEQ
        self.hburst.value = burst_type
        self.hsize.value = size
        await RisingEdge(self.clk)

        for _ in range(burst_length - 1):
            self.htrans.value = TransType.SEQ
            offs = (offs + (1 << size)) & mask
            self.haddr.value = base + offs
            if self.hauser:
                self.hauser.value = hauser
            if self.hmaster:
                self.hmaster.value = hmaster
            await RisingEdge(self.clk)
            while self.hready == 0:
                await RisingEdge(self.clk)
            rdata.append((self.hrdata.value.integer >> ((poffs << 3) & shift_mask)) & szmsk)
            if self.hresp.value:
                err_resp = True
            poffs = offs
        if self.hsel:
            self.hsel.value = 0
        self.haddr.value = 0
        self.htrans.value = TransType.IDLE
        self.hsize.value = SizeType.BYTE
        await RisingEdge(self.clk)
        while self.hready == 0:
            await RisingEdge(self.clk)
        rdata.append((self.hrdata.value.integer >> ((poffs << 3) & shift_mask)) & szmsk)
        if self.hresp.value:
            err_resp = True
        self._info_log(
            rw="READ",
            addr=addr,
            burst_type=burst_type,
            burst_length=burst_length,
            size=size,
            data=rdata,
            err_resp=err_resp,
        )
        return (err_resp, tuple(rdata))

    async def reset(self):
        """Reset AHB Master."""
        if self.hsel:
            self.hsel.value = 0
        self.hwrite.value = 0
        self.hwdata.value = 0
        self.htrans.value = 0  # IDLE
        self.hburst.value = 0
        self.hprot.value = 0

    def calc_wrmem(
        self,
        offs: int,
        size: SizeType,
        blen: int,
        mmask: int,
        wdata: int | Iterable[int],
        wstrb: int | Iterable[int] | None = None,
        mem: bytearray | None = None,
    ) -> bytearray:
        """Calculate Reference Write Data for a Burst in Bytes."""
        memimg = bytearray(blen << size)
        if mem is not None:
            memimg = mem[(offs & ~mmask) : (offs & ~mmask) + (blen << size)]
        allstrb = (1 << (1 << size)) - 1
        if isinstance(wdata, int):
            wdata = iter((wdata,))
        else:
            wdata = iter(wdata)
        if wstrb is None:
            wstrb = iter(_bottomless(allstrb))
        elif isinstance(wstrb, int):
            wstrb = iter(_bottomless(wstrb))
        else:
            wstrb = iter(wstrb)
        for widx in range(blen):
            midx = (offs + (widx << size)) & mmask
            bytes = bytearray(int.to_bytes(next(wdata), 1 << size, "little"))
            strbs = next(wstrb)
            for b in range(1 << size):
                if strbs & 1:
                    memimg[midx + b] = bytes[b]
                strbs >>= 1
        return memimg

    def calc_expected(self, offs: int, size: SizeType, blen: int, mmask: int, mem: bytearray) -> list[int]:
        """Calculate Expected Read Data for a Burst according to Size."""
        xdata = []
        for widx in range(blen):
            xd = 0
            for bidx in range(1 << size):
                xd |= mem[(offs & ~mmask) + ((offs + (widx << size) + bidx) & mmask)] << (bidx << 3)
            xdata.append(xd)
        return xdata

    def _info_log(
        self,
        rw: str,
        addr: int,
        burst_type: BurstType,
        burst_length: int,
        size: SizeType,
        data: list[int],
        err_resp: bool,
    ) -> None:
        """Handle Master Logging."""
        if burst_type == BurstType.INCR:
            blenstr = f" burst length: {burst_length}"
        else:
            blenstr = ""
        err = " ERROR RESP" if err_resp else ""
        hexaddr = str(Hex(addr, self.addr_width))
        hexdata = ",".join(str(Hex(x, 8 << size)) for x in data)
        self.logger.info(
            f"=MST {rw}{err}= address: {hexaddr} data: [{hexdata}] "
            f"size: {size.name} burst: {burst_type.name}{blenstr}"
        )


class AHBSlaveDriver:
    """Active AHB Slave that can respond to Master requests."""

    def __init__(
        self,
        name: str,
        clk: SimHandle,
        rst_an: SimHandle,
        haddr: SimHandle,
        hwrite: SimHandle,
        hwdata: SimHandle,
        htrans: SimHandle,
        hburst: SimHandle,
        hsize: SimHandle,
        hrdata: SimHandle,
        hready: SimHandle,
        hreadyout: SimHandle,
        hresp: SimHandle,
        hsel: SimHandle,
        hprot: SimHandle = None,
        hwstrb: SimHandle = None,
        hnonsec: SimHandle = None,
        hmastlock: SimHandle = None,
        hexcl: SimHandle = None,
        hmaster: SimHandle = None,
        hexokay: SimHandle = None,
        hauser: SimHandle = None,
        hreadyout_delay: int = 0,
        size_bytes: int = 1024,
        err_addr: dict[Literal["r", "w", "rw"], list[int]] | None = None,
        log_level: int | None = None,
    ):
        """AHB Slave Init."""
        self.name = name
        self.clk = clk
        self.rst_an = rst_an
        self.haddr = haddr
        self.hwrite = hwrite
        self.hwdata = hwdata
        self.htrans = htrans
        self.hburst = hburst
        self.hsize = hsize
        self.hrdata = hrdata
        self.hready = hready
        self.hreadyout = hreadyout
        self.hresp = hresp
        self.hsel = hsel
        # optional signals:
        self.hprot = hprot
        self.hwstrb = hwstrb
        self.hnonsec = hnonsec
        self.hmastlock = hmastlock
        self.hexcl = hexcl
        self.hmaster = hmaster
        self.hexokay = hexokay
        self.hauser = hauser
        self.addr_width = len(haddr)
        self.data_width = len(hwdata)
        self.byte_width = len(hwdata) // 8
        self.err_addr = err_addr

        self.logger = getLogger(name)
        if log_level is not None:  # important explicit check for None as 0 would be a valid value
            self.logger.setLevel(log_level)

        self.mem = bytearray(size_bytes)  # Initialize a 1KB memory
        self.hreadyout_delay = hreadyout_delay  # Delay for HREADYOUT signal to simulate longer access times
        self.addrmask = size_bytes - 1

        # state variables
        self.state = 0
        self.burst_count = 0  # Burst count for burst transactions
        self.curr_addr = None
        self.curr_wdata = None
        self.curr_write = None
        self.curr_size = None
        self.curr_wstrb = None
        self.curr_hauser = None
        self.curr_hmaster = None

    def _read(self, addr: int, size: int) -> int:
        """AHB Read."""
        # number of bytes in this transfer according to transfer size
        byte_cnt = 2**size
        # extract the data from the bus
        alignmask = byte_cnt - 1
        shift_mask = self.data_width - 1
        datashift_bit = (addr << 3) & shift_mask
        masked_addr = self.addrmask & addr
        unaligned = alignmask & addr
        assert not unaligned, f"Address is unaligned for read with HSIZE of {SizeType(size)!r} at HADDR {addr}."

        rdata = int.from_bytes(self.mem[masked_addr : masked_addr + byte_cnt], "little") << datashift_bit
        hexaddr = str(Hex(addr, self.addr_width))
        hexdata = str(Hex(rdata, 8 << size))
        self.logger.info(f"=SLV READ= address: {hexaddr} data: {hexdata} size: {SizeType(size).name}")
        self.logger.debug(
            f"=SLV READ= alignment mask: {hex(alignmask)} "
            f"shift mask: {hex(shift_mask)} datashift in bits: {hex(datashift_bit)} "
            f"address (masked): {hex(masked_addr)} byte count: {byte_cnt}"
        )
        return rdata

    def _write(self, addr: int, size: int, data: int, strb: int) -> None:
        """AHB Write."""
        # number of bytes in this transfer according to transfer size
        byte_cnt = 2**size
        shift_mask = self.data_width - 1
        # extract the data from the bus
        alignmask = byte_cnt - 1
        lower_datamask = (2 ** (byte_cnt * 8)) - 1
        datashift_bit = (addr << 3) & shift_mask
        unaligned = alignmask & addr
        assert not unaligned, f"Address is unaligned for write with HSIZE of {size} at HADDR {addr}."

        masked_addr = self.addrmask & addr
        wdata = (data >> datashift_bit) & lower_datamask
        wstrb = strb >> (datashift_bit >> 3)
        strbs = [(wstrb >> i) & 1 for i in range(byte_cnt)]
        bytes = bytearray(int.to_bytes(wdata, byte_cnt, "little"))
        for b in range(byte_cnt):
            if not strbs[b]:
                bytes[b] = self.mem[masked_addr + b]  # replace with read value

        hexaddr = str(Hex(addr, self.addr_width))
        hexdata = str(Hex(wdata, 8 << size))
        self.logger.info(f"=SLV WRITE= address: {hexaddr} data: {hexdata} size: {SizeType(size).name} strb: {strbs}")
        self.logger.debug(
            f"=SLV WRITE= alignment mask: {hex(alignmask)} shift mask: {hex(shift_mask)} "
            f"lower data mask {hex(lower_datamask)} datashift in bits: {hex(datashift_bit)} "
            f"address (masked): {hex(masked_addr)} byte count: {byte_cnt} "
            f"data (bytes): {','.join([hex(x) for x in bytes])} "
        )
        self.mem[masked_addr : masked_addr + byte_cnt] = bytes

    def _check_err_addr(self, haddr: int, hwrite: int) -> bool:
        """Check for Error Address."""
        if self.err_addr is None:
            return False
        if hwrite:
            if (haddr in self.err_addr.get("w", [])) or (haddr in self.err_addr.get("rw", [])):
                return True
        elif (haddr in self.err_addr.get("r", [])) or (haddr in self.err_addr.get("rw", [])):
            return True
        return False

    async def run(self):
        """Slave Main Loop."""
        self.hreadyout.value = 1
        self.hrdata.value = 0xDEADDEAD
        self.hresp.value = 0
        allstrb = (1 << self.byte_width) - 1
        while True:
            await RisingEdge(self.clk)
            if self.state:
                for _ in range(self.hreadyout_delay):  # delay the answer if configured
                    await RisingEdge(self.clk)
                    self.hreadyout.value = 0
                self.hreadyout.value = 1
                self.curr_wdata = self.hwdata.value if self.curr_write else 0
                self.curr_wstrb = self.hwstrb.value.integer if self.hwstrb is not None else allstrb
                if (self.state == 1) and self.curr_write:
                    # Handle write request
                    self._write(self.curr_addr, self.curr_size, self.curr_wdata, self.curr_wstrb)
            # Check if there's an AHB request
            if self.hsel.value and self.htrans.value in (TransType.SEQ, TransType.NONSEQ):
                self.curr_addr = self.haddr.value.integer
                self.curr_trans = self.htrans.value.integer
                self.curr_write = self.hwrite.value.integer
                self.curr_size = self.hsize.value.integer
                self.curr_hauser = self.hauser.value.integer if self.hauser is not None else None
                self.curr_hmaster = self.hmaster.value.integer if self.hmaster is not None else None
                self.state = 1
            else:
                self.state = 0
            if self.state and self._check_err_addr(self.curr_addr, self.curr_write):
                acc = "WRITE" if self.curr_write else "READ"
                hexaddr = str(Hex(self.curr_addr, self.addr_width))
                self.logger.info(f"=SLV ERROR RESP for {acc}= address: {hexaddr}")
                # TODO: response handling w/ delay cycle...
                self.state = 2
            if self.state == 1 and self.curr_trans == TransType.NONSEQ:
                acc = "WRITE" if self.curr_write else "READ"
                hauser = f" hauser: {hex(self.curr_hauser)}" if self.curr_hauser is not None else ""
                hmaster = f" hmaster: {hex(self.curr_hmaster)}" if self.curr_hmaster is not None else ""
                hexaddr = str(Hex(self.curr_addr, self.addr_width))
                self.logger.info(f"=SLV NEW {acc}= address: {hexaddr}{hauser}{hmaster}")
            if self.state and not self.curr_write:
                # Handle read request (need to apply read value for next cycle)
                rdata = self._read(self.curr_addr, self.curr_size)
                self.hrdata.value = rdata
            else:
                self.hrdata.value = 0xDEADDEAD

    def set_hreadyout_delay(self, delay):
        """Set hreadyout Delay."""
        self.hreadyout_delay = delay

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
            chunk = ",".join(str(Hex(x, 8)) for x in self.mem[i : min(i + chunk_size, end_addr + 1)])
            self.logger.info(f"=MEMORY CONTENTS= {hexstart}-{hexend} [{chunk}]")
