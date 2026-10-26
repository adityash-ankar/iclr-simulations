
"""
Ghost-cell support for the discretised feed system.

This module defines a lightweight ghostCellJIT component that acts as a
boundary cell to enforce inlet/outlet conditions and to carry velocity
and massflow information between computational cells. Inputs: neighbor
cell references and their pressures/velocities. Outputs: propagated
boundary pressures and mdot where appropriate. Intended for use only as
an internal boundary helper within FeedSystemCriticalPath.
"""

from util_funcs import *

from component_classes.system_component import (
    systemComponentJIT,
)


class ghostCellJIT(systemComponentJIT):
    """
    Boundary ghost cell used to enforce inlet and outlet conditions.

    This lightweight helper mirrors neighbor pressures/velocities to
    maintain stable boundary conditions. Inputs: neighbor component
    references (cell) to read pressureOut/mdot. Outputs: enforced
    pressureIn/pressureOut and mdot where applicable. Not a physical
    component — used solely by FeedSystemCriticalPath for numerical
    boundary handling.
    """
    def __init__(self, u=None, pos=None, pressureIn=None, pressureOut=None, temp=None, rho=None, mdot=None, prevComp=None, location=None):
        """Create a boundary placeholder that carries boundary values into the main solver."""
        super().__init__(type="g", pos=pos, pressureIn=pressureIn, pressureOut=pressureOut, temp=temp, rho=rho, mdot=mdot, location=location)
        self.length = 0.0
        self.uIn = u
        self.uOut = self.uIn
        self.u_iterate = u

    def getVelocity(self):
        """Return the ghost-cell velocity state used for boundary propagation."""
        return self.u_iterate

    def dp(self, cell):
        """Return the simple pressure differential between neighboring physical cells."""
        return cell.getPressureIn() - cell.getPressureOut()

    def setU(self, uIn):
        """Set both the inlet and outlet ghost velocities to the same applied boundary value."""
        self.setuIn(uIn)
        self.setuOut(uIn)

    def update(self, cell=None):
        """Refresh the ghost-cell pressure state based on the neighboring physical cell."""
        if cell:
            self.pressureIn = cell.getPressureOut()
            self.pressureOut = self.pressureIn - self.dp(cell)

    def solveMdot(self, cell=None):
        """Propagate mass-flow information from the adjacent physical cell into the boundary."""
        if cell:
            self.mdot = cell.getMdot()
            self.pressureIn = cell.getPressureOut()
            self.pressureOut = self.pressureIn