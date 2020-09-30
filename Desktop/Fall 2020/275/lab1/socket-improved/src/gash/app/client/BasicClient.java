package gash.app.client;

import java.net.Socket;
import java.util.Properties;

import gash.comm.extra.Message;
import gash.comm.payload.BasicBuilder;

/**
 * client chat
 * 
 * @author gash
 * 
 */
public class BasicClient {
	private Properties setup;

	private long count = 0l;
	private long sentCount = 0l;

	private String _host = "localhost"; // "127.0.0.1" ;
	private ClientListener listener;
	private Socket socket;
	private String name;

	/**
	 * empty constructor
	 */
	public BasicClient() {
	}

	/**
	 * specify the host and port to connect to
	 */
	public BasicClient(Properties setup) {
		this.setup = setup;
	}

	public void setName(String name) {
		this.name = name;
	}

	public String getName() {
		return name;
	}

	/**
	 * connect to server
	 */
	public void startSession() {
		if (socket != null) {
			return;
		}

		String host = setup.getProperty("host");
		String port = setup.getProperty("port");
		if (host == null || port == null)
			throw new RuntimeException("Missing port and/or host");

		try {
			socket = new Socket(host, Integer.parseInt(port));
			System.out.println("Connected to " + socket.getInetAddress().getHostAddress());

			// establish response handler
			listener = new ClientListener(socket);
			listener.start();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	/**
	 * close this session
	 */
	public void stopSession() {
		if (socket == null) {
			System.out.println("message not sent");
			return;
		}

		try {
			if (listener != null)
				listener.stopListening();

			BasicBuilder builder = new BasicBuilder();
			byte[] msg = builder.encode(BasicBuilder.MessageType.leave, getID(), name, null, null).getBytes();
			socket.getOutputStream().write(msg);
			socket.getOutputStream().flush();
			socket.close();
		} catch (Exception e) {
			e.printStackTrace();
		}

		socket = null;
	}

	/**
	 * announce that client has joined the network
	 * 
	 * @param name
	 *            String
	 */
	public void join(String name) {
		if (socket == null) {
			System.out.println("message not sent");
			return;
		}

		try {
			BasicBuilder builder = new BasicBuilder();
			byte[] msg = builder.encode(BasicBuilder.MessageType.join, getID(), name, null, null).getBytes();
			socket.getOutputStream().write(msg);
			socket.getOutputStream().flush();
			sentCount++;
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	/**
	 * send a general (public) message to the server
	 * 
	 * @param msg
	 *            String
	 */
	public void sendMessage(String message) {
		if (socket == null) {
			System.out.println("message not sent");
			return;
		} else if (message != null && message.length() > 1024) {
			System.out.println("message exceeds 1024 size limit");
			return;
		}

		try {
			if (socket.isOutputShutdown()) {
				System.out.println("ERROR: socket write is blocked!");
				// TODO wait for writable again
			}

			BasicBuilder builder = new BasicBuilder();
			byte[] msg = builder.encode(BasicBuilder.MessageType.msg, getID(), name, message, null).getBytes();
			socket.getOutputStream().write(msg);
			socket.getOutputStream().flush();
			sentCount++;
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	/**
	 * for use with integrating to other code
	 * 
	 * @param msg
	 */
	public void sendMessage(Message msg) {

		try {
			BasicBuilder builder = new BasicBuilder();
			byte[] raw = builder
					.encode(msg.getType(), msg.getMid(), msg.getSource(), msg.getPayload(), msg.getReceived())
					.getBytes();

			socket.getOutputStream().write(raw);
			socket.getOutputStream().flush();
			sentCount++;
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	/**
	 * are there messages we are waiting for responses?
	 * 
	 * @return
	 */
	public boolean isPendingResponses() {
		System.out.println(sentCount + " / " + listener.getReceievedCount());
		return sentCount != listener.getReceievedCount();
	}

	private String getID() {
		return Long.toString(count++);
	}
}
