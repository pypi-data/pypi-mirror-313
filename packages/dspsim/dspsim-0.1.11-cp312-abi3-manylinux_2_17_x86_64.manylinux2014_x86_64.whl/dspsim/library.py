# from dspsim._library import *

from dspsim.framework import Signal8, SignalT

# Some components have additional wrappers.
from dspsim.axis import Axis, AxisTx, AxisRx
from dspsim.fifo import FifoSync, FifoAsync, FifoAsync8
from dspsim.i2s import I2S, I2SClkGen, I2STx, I2SRx

from dspsim._library import Foo, SomeModel, X
from dspsim._library import AsyncSync8, AsyncSync

from dspsim._library import Skid as _Skid
from dspsim._library import Gain as _Gain


class Skid(_Skid):
    """Wrapper to allow connecting axis busses"""

    @classmethod
    def init_bus(cls, clk: Signal8, rst: Signal8, s_axis: Axis, m_axis: Axis):
        """"""
        return cls(
            clk=clk,
            rst=rst,
            s_axis_tdata=s_axis.tdata,
            s_axis_tvalid=s_axis.tvalid,
            s_axis_tready=s_axis.tready,
            m_axis_tdata=m_axis.tdata,
            m_axis_tvalid=m_axis.tvalid,
            m_axis_tready=m_axis.tready,
        )


class Gain(_Gain):
    """Wrapper to allow connecting axis busses"""

    @classmethod
    def init_bus(
        cls, clk: Signal8, rst: Signal8, s_axis: Axis, m_axis: Axis, gain: SignalT
    ):
        """"""
        return cls(
            clk=clk,
            rst=rst,
            s_axis_tdata=s_axis.tdata,
            s_axis_tvalid=s_axis.tvalid,
            s_axis_tready=s_axis.tready,
            m_axis_tdata=m_axis.tdata,
            m_axis_tvalid=m_axis.tvalid,
            m_axis_tready=m_axis.tready,
            gain=gain,
        )
