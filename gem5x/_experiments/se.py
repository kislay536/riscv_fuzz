import sys
import m5
from m5.objects import *
from gem5.components.cachehierarchies.classic.private_l1_private_l2_cache_hierarchy import *

#from caches import *

system = System()

# Initialize the CPU
system.cpu = RiscvO3CPU()

# Set up the clock domain and voltage domain
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()

# Set the memory mode and range
system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('3GB')]

# Initialize the system buses
system.membus = SystemXBar()
system.l2bus = L2XBar()

# Initialize the L1 instruction and data caches
system.cpu.icache = L1ICache(size='2kB', assoc=4)
system.cpu.dcache = L1DCache(size='2kB', assoc=4)

# Manually connect the L1 caches to the CPU
system.cpu.icache.cpu_side = system.cpu.icache_port
system.cpu.dcache.cpu_side = system.cpu.dcache_port

# Connect the L1 caches to the L2 bus
system.cpu.icache.mem_side = system.l2bus.cpu_side_ports
system.cpu.dcache.mem_side = system.l2bus.cpu_side_ports

# Set up and connect the L2 cache
system.l2cache = L2Cache(size='256kB', assoc=8)
system.l2cache.cpu_side = system.l2bus.mem_side_ports
system.l2cache.mem_side = system.membus.cpu_side_ports

# Create and connect the interrupt controller
system.cpu.createInterruptController()
# Set the system port
system.system_port = system.membus.cpu_side_ports

# Set up memory control
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

# Specify the binary for the simulation

# Default binary path
binary = '_experiments/binaries/test'

# Check if a binary argument is provided
if len(sys.argv) > 1:
    binary = sys.argv[1].split('=')[1]  # Extract the binary path from the argument


# Set up the workload and process
system.workload = SEWorkload.init_compatible(binary)
process = Process()
process.cmd = [binary]
system.cpu.workload = process
system.cpu.createThreads()

# Instantiate the root and system
root = Root(full_system=False, system=system)
m5.instantiate()

# Begin the simulation
print("Beginning simulation!")
exit_event = m5.simulate()

print('Exiting @ tick {} because {}'.format(m5.curTick(), exit_event.getCause()))
