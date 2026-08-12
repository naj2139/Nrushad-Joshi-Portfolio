CXX = g++
# MathExpr uses unordered_set::contains() (C++20) and structured bindings.
CXXFLAGS = -std=c++20 -Wall

# Source files (each lives in its own subdirectory)
LARGESUM_SRC  = LargeSum/LargeSum.cpp
SUBDIV_SRC    = SubstringDivisibility/SubstringDivisibility.cpp
CONTACTS_SRC  = Contacts/contacts.cpp
MATHEXPR_SRC  = MathExpr/MathExpr.cpp

# Output binaries are built inside their respective source directories.
LARGESUM_BIN = LargeSum/largesum
SUBDIV_BIN   = SubstringDivisibility/substringdivisibility
CONTACTS_BIN = Contacts/contacts
MATHEXPR_BIN = MathExpr/mathexpr

.PHONY: all clean largesum subdiv contacts mathexpr

all: $(LARGESUM_BIN) $(SUBDIV_BIN) $(CONTACTS_BIN) $(MATHEXPR_BIN)

largesum: $(LARGESUM_BIN)
subdiv: $(SUBDIV_BIN)
contacts: $(CONTACTS_BIN)
mathexpr: $(MATHEXPR_BIN)

$(LARGESUM_BIN): $(LARGESUM_SRC)
	$(CXX) $(CXXFLAGS) $(LARGESUM_SRC) -o $(LARGESUM_BIN)

$(SUBDIV_BIN): $(SUBDIV_SRC)
	$(CXX) $(CXXFLAGS) $(SUBDIV_SRC) -o $(SUBDIV_BIN)

$(CONTACTS_BIN): $(CONTACTS_SRC)
	$(CXX) $(CXXFLAGS) $(CONTACTS_SRC) -o $(CONTACTS_BIN)

$(MATHEXPR_BIN): $(MATHEXPR_SRC)
	$(CXX) $(CXXFLAGS) $(MATHEXPR_SRC) -o $(MATHEXPR_BIN)

clean:
	rm -f $(LARGESUM_BIN) $(SUBDIV_BIN) $(CONTACTS_BIN) $(MATHEXPR_BIN)