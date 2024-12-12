# Define directories
SNIPPET_GEN = snippet_gen
SPECTRE = spectre
SNIPPETS = $(SNIPPET_GEN)/snippets
BINARIES = $(SNIPPET_GEN)/binaries
BIN_OUTPUT = $(SPECTRE)/bin

# Default target
all: check_dirs

clean:
	@rm -rf snippet_gen/binaries

# Rule to check and create directories
check_dirs: clean
	@for dir in $(BINARIES) $(SNIPPETS); do \
		if [ ! -d $$dir ]; then \
			echo "Directory $$dir does not exist. Creating..."; \
			mkdir -p $$dir; \
		else \
			echo "Directory $$dir already exists."; \
		fi \
	done

# Compile target
compile: check_dirs
	@for snippet in $(SNIPPETS)/*.s; do \
		filename=$$(basename $$snippet); \
		modified_name=$$(echo $$filename | sed 's/\./_/g'); \
		echo "Processing $$filename..."; \
		cp $$snippet $(SPECTRE)/snippet.s; \
		make -C $(SPECTRE) all RETPOLINE=1; \
		binary_file=$$(ls $(BIN_OUTPUT)/* 2>/dev/null | head -n 1); \
		if [ -z "$$binary_file" ]; then \
			echo "No binary file found in $(BIN_OUTPUT). Skipping..."; \
		else \
			new_binary_name="$${modified_name}"; \
			cp $$binary_file $(BINARIES)/$$new_binary_name; \
			echo "Copied $$binary_file to $(BINARIES)/$$new_binary_name"; \
		fi; \
		rm -f $(SPECTRE)/snippet.s; \
	done

# ASM target to run the Python script
asm: check_dirs
	@if [ -z "$(line)" ]; then \
		echo "Error: You must specify a line number. Use 'make asm line=<integer>'."; \
		exit 1; \
	fi; \
	cd $(SNIPPET_GEN) && python3 opcode_fuzz.py $(line)

.PHONY: sim

.PHONY: sim

sim:
	@if [ -z "$(binary)" ]; then \
		echo "Error: You must specify a binary file. Use 'make sim binary=<file>'."; \
		exit 1; \
	fi; \
	echo "Starting gem5 simulation in two terminals..."; \
	# Start gem5 simulation in the first gnome-terminal
	gnome-terminal -- bash -c "./gem5/build/RISCV/gem5.opt ./gem5/configs/example/riscv/fs_linux.py --kernel ./$(BINARIES)/$(binary) --bare --cpu-type=O3CPU --caches --l2cache; exec bash" & \
	PID=$$!; \
	# Wait for a few seconds for the first terminal to start
	sleep 3; \
	# Start m5term in the second gnome-terminal, appending its output to a log file
	gnome-terminal -- bash -c "./gem5/util/term/m5term localhost 3456; exec bash" >> m5term_output.txt 2>&1 & \
	# Continuously monitor the log file and check for the string "guessed secret"
	while true; do \
		if tail -n 100 m5term_output.txt | grep -q "guessed secret"; then \
			echo "Secret guessed. Terminating gem5 simulation."; \
			kill -SIGINT $$PID; \
			break; \
		fi; \
		sleep 1; \
	done






terminal:
	@echo "Starting simulation in three terminals..."
	# Open the first terminal and print "Terminal 1"
	@xterm -hold -e "echo 'Terminal 1'; sleep 60" & \
	# Capture the PID of the first terminal
	PID1=$$!; \
	# Open the second terminal and print "Terminal 2"
	@xterm -hold -e "echo 'Terminal 2'; sleep 60" & \
	# Capture the PID of the second terminal
	PID2=$$!; \
	# Open the third terminal and print "Terminal 3"
	@xterm -hold -e "echo 'Terminal 3'; sleep 60" & \
	# Capture the PID of the third terminal
	PID3=$$!; \
	# Wait for all terminals to finish and then kill them one by one
	@echo "All terminals are open, now killing them one by one..."; \
	# Wait for the first terminal to finish and kill it
	wait $$PID1; \
	kill $$PID1; \
	@echo "Terminal 1 has been killed."; \
	# Wait for the second terminal to finish and kill it
	wait $$PID2; \
	kill $$PID2; \
	@echo "Terminal 2 has been killed."; \
	# Wait for the third terminal to finish and kill it
	wait $$PID3; \
	kill $$PID3; \
	@echo "Terminal 3 has been killed."





