.PHONY: design1 design2 design3 design4 design5 base delete compile clean check_and_rename stats se boom show spectre

CODES_DIR := /home/riscv_sec/gem5-riscv/gem5/_experiments/codes
BINARIES_DIR := /home/riscv_sec/gem5-riscv/gem5/_experiments/binaries
STATS_SRC := /home/riscv_sec/gem5-riscv/gem5/m5out/stats.txt
STATS_DEST := /home/riscv_sec/gem5-riscv/gem5/_experiments/gem5-stats
BOOM_SRC := /home/riscv_sec/gem5-riscv/boom-attacks/src
SPECTRE_SRC := /home/riscv_sec/gem5-riscv/spectre-v2-v5/src

CC := riscv64-unknown-elf-gcc

# Find all .c files in the codes directory
C_SOURCES := $(wildcard $(CODES_DIR)/*.c)

# Derive binary filenames from source filenames
BINARIES := $(patsubst $(CODES_DIR)/%.c,$(BINARIES_DIR)/%,$(C_SOURCES))

# Helper function to check and rename src folder if needed
check_and_rename:
	@if [ ! -d "src-design-1" ] && [ -d "src" ]; then \
		echo "src-design-1 not found. Renaming src to src-design-1..."; \
		mv src src-design-1; \
	fi
	@if [ ! -d "src-design-2" ] && [ -d "src" ]; then \
		echo "src-design-2 not found. Renaming src to src-design-2..."; \
		mv src src-design-2; \
	fi
	@if [ ! -d "src-design-3" ] && [ -d "src" ]; then \
		echo "src-design-3 not found. Renaming src to src-design-3..."; \
		mv src src-design-3; \
	fi
	@if [ ! -d "src-design-4" ] && [ -d "src" ]; then \
		echo "src-design-4 not found. Renaming src to src-design-4..."; \
		mv src src-design-4; \
	fi
	@if [ ! -d "src-design-5" ] && [ -d "src" ]; then \
		echo "src-design-5 not found. Renaming src to src-design-5..."; \
		mv src src-design-5; \
	fi
	@if [ ! -d "src-baseline" ] && [ -d "src" ]; then \
		echo "src-baseline not found. Renaming src to src-baseline..."; \
		mv src src-baseline; \
	fi


#designs
design1:check_and_rename
	@echo "Waiting for checks to complete..."
	@sleep 1  # Optional: Add a delay if needed
	# @echo "Deleting existing RISCV Binary"
	# @rm -rf build/RISCV
	@echo "Switching folder from src-design-1 to src..."
	@mv src-design-1 src
	@echo "Building gem5..."
	@scons build/RISCV/gem5.opt -j80
	@echo "Switching folder back to src-design-1..."
	@mv src src-design-1
	@echo "Done."

design2:check_and_rename
	@echo "Waiting for checks to complete..."
	@sleep 1  # Optional: Add a delay if needed
	# @echo "Deleting existing RISCV Binary"
	# @rm -rf build/RISCV
	@echo "Switching folder from src-design-2 to src..."
	@mv src-design-2 src
	@echo "Building gem5..."
	@scons build/RISCV/gem5.opt -j80
	@echo "Switching folder back to src-design-2..."
	@mv src src-design-2
	@echo "Done."

design3:check_and_rename
	@echo "Waiting for checks to complete..."
	@sleep 1  # Optional: Add a delay if needed
	# @echo "Deleting existing RISCV Binary"
	# @rm -rf build/RISCV
	@echo "Switching folder from src-design-3 to src..."
	@mv src-design-3 src
	@echo "Building gem5..."
	@scons build/RISCV/gem5.opt -j80
	@echo "Switching folder back to src-design-3..."
	@mv src src-design-3
	@echo "Done."

design4:check_and_rename
	@echo "Waiting for checks to complete..."
	@sleep 1  # Optional: Add a delay if needed
	# @echo "Deleting existing RISCV Binary"
	# @rm -rf build/RISCV
	@echo "Switching folder from src-design-4 to src..."
	@mv src-design-4 src
	@echo "Building gem5..."
	@scons build/RISCV/gem5.opt -j80
	@echo "Switching folder back to src-design-4..."
	@mv src src-design-4
	@echo "Done."

design5:check_and_rename
	@echo "Waiting for checks to complete..."
	@sleep 1  # Optional: Add a delay if needed
	# @echo "Deleting existing RISCV Binary"
	# @rm -rf build/RISCV
	@echo "Switching folder from src-design-5 to src..."
	@mv src-design-5 src
	@echo "Building gem5..."
	@scons build/RISCV/gem5.opt -j80
	@echo "Switching folder back to src-design-5..."
	@mv src src-design-5
	@echo "Done."

base:check_and_rename
	@echo "Waiting for checks to complete..."
	@sleep 1  # Optional: Add a delay if needed
	# @echo "Deleting existing RISCV Binary"
	# @rm -rf build/RISCV
	@echo "Switching folder from src-baseline to src..."
	@mv src-baseline src
	@echo "Building gem5..."
	@scons build/RISCV/gem5.opt -j80
	@echo "Switching folder back to src-baseline..."
	@mv src src-baseline
	@echo "Done."

#deletes the build folder
delete:
	@echo "Deleting build folder...."
	@rm -rf build
	@echo "Done."

# Compile target
compile: $(BINARIES)

# Rule to build each binary
$(BINARIES_DIR)/%: $(CODES_DIR)/%.c
	@mkdir -p $(BINARIES_DIR)
	$(CC) -o $@ $<

# Clean up binaries
clean:
	rm -rf $(BINARIES_DIR)


# Stats
stats:
	@if [ "$(exp)" = "" ]; then \
		echo "Usage: make stats exp=<experiment_name>"; \
		exit 1; \
	fi
	@if [ ! -f "$(STATS_SRC)" ]; then \
		echo "Error: stats.txt file not found in folder A."; \
		exit 1; \
	fi
	@echo "Copying stats.txt to $(STATS_DEST)/$(exp)-stats.txt..."
	@mkdir -p $(STATS_DEST)
	@cp $(STATS_SRC) $(STATS_DEST)/$(exp)-stats.txt
	@echo "Saved stats as $(STATS_DEST)/$(exp)-stats.txt."


se:
	@if [ "$(bin)" = "" ]; then \
		echo "Usage: make se bin=<binary_name>"; \
		exit 1; \
	fi
	@echo "Running gem5 with binary _experiments/binaries/$(bin)..."
	@build/RISCV/gem5.opt _experiments/se.py --binary=_experiments/binaries/$(bin)

boom:
	@echo "Creating binaries directory if not exists..."
	@mkdir -p $(BINARIES_DIR)
	@echo "Compiling condBranchMispred.c..."
	@riscv64-unknown-elf-gcc -o $(BINARIES_DIR)/condBranchMispred $(BOOM_SRC)/condBranchMispred.c
	@echo "Compiling indirBranchMispred.c..."
	@riscv64-unknown-elf-gcc -o $(BINARIES_DIR)/indirBranchMispred $(BOOM_SRC)/indirBranchMispred.c
	@echo "Compiling returnStackBuffer.c with stack.S..."
	@riscv64-unknown-elf-gcc -o $(BINARIES_DIR)/returnStackBuffer-boom $(BOOM_SRC)/returnStackBuffer.c $(BOOM_SRC)/stack.S
	@echo "All binaries created successfully in $(BINARIES_DIR)."

spectre:
	@echo "Creating binaries directory if not exists..."
	@mkdir -p $(BINARIES_DIR)
	@echo "Compiling indirectBranchFunction.c..."
	@riscv64-unknown-elf-gcc -o $(BINARIES_DIR)/indirectBranchFunction $(SPECTRE_SRC)/indirectBranchFunction.c
	@echo "Compiling indirectBranchSwitch.c..."
	@riscv64-unknown-elf-gcc -o $(BINARIES_DIR)/indirectBranchSwitch $(SPECTRE_SRC)/indirectBranchSwitch.c
	@echo "Compiling returnStackBuffer.c with stack.S..."
	@riscv64-unknown-elf-gcc -o $(BINARIES_DIR)/returnStackBuffer-spec $(SPECTRE_SRC)/returnStackBuffer.c $(BOOM_SRC)/rsb.S
	@echo "All binaries created successfully in $(BINARIES_DIR)."

show:
	@echo "Available binaries"
	@ls _experiments/binaries