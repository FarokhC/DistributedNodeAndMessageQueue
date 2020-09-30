package gash.comm.core;

import java.net.ServerSocket;
import java.net.Socket;
import java.util.Properties;

/**
 * server to manage incoming clients
 * 
 * @author gash
 * 
 */
public class BasicSocketServer {
	private Properties setup;
	private ServerSocket socket;
	private long idCounter = 1;
	private boolean forever = true;
	private Sessions connections;

	public static final String PropertyPort = "port";

	public BasicSocketServer() {
		this.setup = new Properties();
		this.setup.setProperty(PropertyPort, "1900");

		this.connections = new Sessions();
	}

	/**
	 * construct a new server listening on the specified port
	 */
	public BasicSocketServer(Properties setup) {
		this.setup = setup;
		this.connections = new Sessions();
	}

	/**
	 * start monitoring socket for new connections
	 */
	public void start() {
		if (setup == null)
			throw new RuntimeException("Missing configuration properties");

		try {
			int port = Integer.parseInt(setup.getProperty("port"));
			socket = new ServerSocket(port);

			System.out.println("Server Host: " + socket.getInetAddress().getHostAddress());

			// monitors and removes idle sessions
			MonitorSessions monitor = new MonitorSessions(this.connections, 30 * 1000 * 60, 60 * 1000 * 60);

			while (forever) {
				Socket s = socket.accept();
				if (!forever) {
					break;
				}

				System.out.println("--> server got a client connection");
				System.out.flush();

				SessionHandler sh = new SessionHandler(s, idCounter++);
				connections.add(sh);
				sh.start();
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	public synchronized void stopSessions() {
		for (SessionHandler sh : connections.getConnections()) {
			sh.stopSession();
		}

		connections = null;
		forever = false;
	}
}
