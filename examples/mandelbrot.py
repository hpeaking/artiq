import sys

from artiq import *
from artiq.coredevice import comm_serial, core


class Mandelbrot(AutoContext):
    def col(self, i):
        sys.stdout.write(" .,-:;i+hHM$*#@ "[i])

    def row(self):
        print("")

    # based on: http://warp.povusers.org/MandScripts/python.html
    @kernel
    def run(self):
        minX = -2.0
        maxX = 1.0
        width = 78
        height = 36
        aspectRatio = 2

        yScale = (maxX-minX)*(height/width)*aspectRatio

        for y in range(height):
            for x in range(width):
                c_r = minX+x*(maxX-minX)/width
                c_i = y*yScale/height-yScale/2
                z_r = c_r
                z_i = c_i
                for i in range(16):
                    if z_r*z_r + z_i*z_i > 4:
                        break
                    new_z_r = (z_r*z_r)-(z_i*z_i) + c_r
                    z_i = 2*z_r*z_i + c_i
                    z_r = new_z_r
                self.col(i)
            self.row()


def main():
    with comm_serial.Comm() as comm:
        exp = Mandelbrot(core=core.Core(comm))
        exp.run()

if __name__ == "__main__":
    main()
