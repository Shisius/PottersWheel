import rnrsrv
import wheelctl

whctl = wheelctl.WheelCtl()
rnr = rnrsrv.RnRserver(whctl.cmd_handler, False)

rnr.mainloop()
