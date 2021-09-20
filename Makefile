
.PHONY: all clean

CXXFLAGS= -O2 -g

LIST=xray_client_tcp xray_fake_server_tcp

all: $(LIST)

% :: %.cc
	g++ $< -o $@

clean:
	rm -f $(LIST)
