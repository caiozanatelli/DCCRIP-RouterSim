# Loopback addresses

The tests run on IP addresses in the `127.0.1.0/24` network.  Use
the `lo-addresses.sh` script to add the IP addresses to the loopback
interface before starting tests.  When done testing, use the
`lo-addresses.sh` script to remove the IP addresses from the
loopback interface.

# tmux automation

Each test contains a `tmux.sh` script that starts multiple routers
in multiple `tmux` panes.  You can run these scripts if you are
within a `tmux` session.  Read up more on `tmux` [here][1] and
[here][2].

 [1]: https://www.hamvocke.com/blog/a-quick-and-easy-guide-to-tmux/
 [2]: https://danielmiessler.com/study/tmux/


