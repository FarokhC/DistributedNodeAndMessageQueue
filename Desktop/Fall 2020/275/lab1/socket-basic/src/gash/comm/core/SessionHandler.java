package gash.comm.core;

import java.io.BufferedInputStream;
import java.io.InterruptedIOException;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.List;

import gash.comm.extra.Message;
import gash.comm.payload.BasicBuilder;
import gash.comm.payload.BasicBuilder.MessageType;

/**
 * 
 * @author gash
 * 
 */
class SessionHandler extends Thread {
	private Socket connection;
	private long id;
	private String name;
	private long lastContact;
	private long count = 0;
	private boolean forever = true;
	private int timeout = 10 * 1000; // 10 seconds
	private BufferedInputStream in = null;
	private PrintWriter out = null;
	private Sessions sessions;

	public SessionHandler(Socket connection, long id) {
		this.connection = connection;
		this.id = id;

		// allow server to exit if
		this.setDaemon(true);
	}

	@Override
	public String toString() {
		StringBuilder sb = new StringBuilder();
		sb.append(name).append(" - Idle: ").append(((System.currentTimeMillis() - lastContact) / 1000))
				.append(" sec, Num msgs: ").append(count);
		return sb.toString();
	}

	/**
	 * register for self removal
	 * 
	 * @param sessions
	 */
	void registerBack(Sessions sessions) {
		this.sessions = sessions;
	}

	/**
	 * stops session on next timeout cycle
	 */
	public void stopSession() {
		forever = false;
		if (connection != null) {
			try {
				sessions.remove(this);
				connection.close();
			} catch (Exception e) {
				e.printStackTrace();
			}
		}
		connection = null;
	}

	public long getSessionId() {
		return id;
	}

	public long getLastContact() {
		return lastContact;
	}

	public void setTimeOut(int v) {
		timeout = v;
	}

	public void setSessionName(String n) {
		name = n;
	}

	public String getSessionName() {
		return name;
	}

	public long getCount() {
		return count;
	}

	/**
	 * process incoming data
	 */
	public void run() {
		System.out.println("Session " + id + " started");

		try {
			connection.setSoTimeout(timeout);
			in = new BufferedInputStream(connection.getInputStream());
			out = new PrintWriter(connection.getOutputStream(), true);

			if (in == null || out == null)
				throw new RuntimeException("Unable to get in/out streams");

			byte[] raw = new byte[2048];
			BasicBuilder builder = new BasicBuilder();
			while (forever) {
				try {
					int len = in.read(raw);
					if (len == 0)
						continue;
					else if (len == -1)
						break;

					List<Message> list = builder.decode(new String(raw, 0, len).getBytes());
					for (Message msg : list) {
						if (msg.getType() == MessageType.leave) {
							return;
						} else if (msg.getType() == MessageType.join) {
							System.out.println("--> join: " + msg.getSource());
						} else if (msg.getType() == MessageType.msg) {
							System.out.println("--> msg: " + msg.getPayload());
						} else if (msg.getType() == MessageType.stat) {
							System.out.println("--> stats: ");
							for (SessionHandler sh : sessions.getConnections()) {
								System.out.println(sh);
							}
						}
					}

					updateLastMsgReceived();

				} catch (InterruptedIOException ioe) {
				}
			}
		} catch (Exception e) {
			e.printStackTrace();
		} finally {
			try {
				System.out.println("Session " + (name == null ? "" : name) + " [" + id + "] exiting");
				System.out.flush();
				stopSession();
			} catch (Exception re) {
				re.printStackTrace();
			}
		}
	}

	/**
	 * record when last message was received - used for timing out of
	 * channel/socket
	 */
	private void updateLastMsgReceived() {
		this.lastContact = System.currentTimeMillis();
		this.count++;
	}

	/**
	 * send message to all connections
	 * 
	 * @param msg
	 *            String
	 * @throws Exception
	 */
	private synchronized void send(String msg) throws Exception {
		for (SessionHandler sh : sessions.getConnections()) {
		}
	}

	/**
	 * send message to a connection
	 * 
	 * @param msg
	 *            String
	 * @throws Exception
	 */
	private synchronized void send(String to, String msg) throws Exception {
		for (SessionHandler sh : sessions.getConnections()) {
			if (sh.getSessionName().equalsIgnoreCase(to)) {
				break;
			}
		}
	}

} // class SessionHandler