CXX = g++

# Source files (each lives in its own subdirectory)
LARGESUM_SRC  = LargeSum/LargeSum.cpp
SUBDIV_SRC    = SubstringDivisibility/SubstringDivisibility.cpp
CONTACTS_SRC  = Contacts/contacts.cpp

# Output binaries are built inside their respective source directories.
LARGESUM_BIN = LargeSum/largesum
SUBDIV_BIN   = SubstringDivisibility/substringdivisibility
CONTACTS_BIN = Contacts/contacts

.PHONY: all clean largesum subdiv contacts

all: $(LARGESUM_BIN) $(SUBDIV_BIN) $(CONTACTS_BIN)

largesum: $(LARGESUM_BIN)
subdiv: $(SUBDIV_BIN)
contacts: $(CONTACTS_BIN)

$(LARGESUM_BIN): $(LARGESUM_SRC)
	$(CXX) $(LARGESUM_SRC) -o $(LARGESUM_BIN)
$(SUBDIV_BIN): $(SUBDIV_SRC)
	$(CXX) $(SUBDIV_SRC) -o $(SUBDIV_BIN)
$(CONTACTS_BIN): $(CONTACTS_SRC)
	$(CXX) $(CONTACTS_SRC) -o $(CONTACTS_BIN)

clean:
	rm -f $(LARGESUM_BIN) $(SUBDIV_BIN) $(CONTACTS_BIN)
