"""Tests to check if the package was built properly and works."""

from dspsim.framework import Context, Clock, signal, dff, SignalT, Signal8, Model
from dspsim.axis import Axis, AxisTx, AxisRx
from dspsim.library import Skid


def test_skid_basic():
    context = Context(1e-9, 1e-9)

    clk = Clock(10e-9)
    rst = dff(clk, 1)

    b0 = Axis(width=Skid.DW)
    b1 = Axis(width=Skid.DW)

    skid = Skid(clk, rst, *b0, *b1)

    axis_tx = AxisTx(clk, rst, *b0)
    axis_rx = AxisRx(clk, rst, *b1)

    context.elaborate()

    rst.d = 1
    context.advance(100)
    rst.d = 0
    context.advance(100)

    tx_data = list(range(1, 42))
    axis_tx.write(tx_data)
    context.advance(100)
    axis_rx.ready = 1
    context.advance(1000)

    rx_data = axis_rx.read()

    assert all(rx_data == tx_data)
