CXX = g++

# Source files (each lives in its own subdirectory)
LARGESUM_SRC = LargeSum/LargeSum.cpp
SUBDIV_SRC   = SubstringDivisibility/SubstringDivisibility.cpp

# Output binaries are built inside their respective source directories.
LARGESUM_BIN = LargeSum/largesum
SUBDIV_BIN   = SubstringDivisibility/substringdivisibility

.PHONY: all clean

all: $(LARGESUM_BIN) $(SUBDIV_BIN)

$(LARGESUM_BIN): $(LARGESUM_SRC)
	$(CXX) $(LARGESUM_SRC) -o $(LARGESUM_BIN)

$(SUBDIV_BIN): $(SUBDIV_SRC)
	$(CXX) $(SUBDIV_SRC) -o $(SUBDIV_BIN)

clean:
	rm -f $(LARGESUM_BIN) $(SUBDIV_BIN)
