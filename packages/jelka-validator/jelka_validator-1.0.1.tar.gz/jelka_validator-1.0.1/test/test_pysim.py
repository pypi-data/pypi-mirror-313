from simulator import Simulation

from subprocess import Popen, PIPE
import sys
import time
from jelka_validator.datareader import DataReader


if __name__ == "__main__":
    # Popen(["-m", "writer.py"], executable=sys.executable, stdout=PIPE)
    # Popen(["writer.exe"], stdout=PIPE)
    with Popen([sys.executable, "writer.py"], stdout=PIPE, bufsize=10000) as p:
        sim = Simulation()
        dr = DataReader(p.stdout.read1)  # type: ignore
        dr.update()
        # assert dr.header is not None
        sim.init()
        time.sleep(1)
        while sim.running:
            c = next(dr)
            assert all(c[i] == c[0] for i in range(len(c)))
            dr.user_print()
            sim.set_colors(dict(zip(range(len(c)), c)))
            sim.frame()
        sim.quit()
