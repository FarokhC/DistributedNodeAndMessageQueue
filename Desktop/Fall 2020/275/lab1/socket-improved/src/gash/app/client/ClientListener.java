package gash.app.client;

import java.io.IOException;
import java.net.Socket;
import java.util.List;

import gash.comm.extra.Message;
import gash.comm.payload.BasicBuilder;

public class ClientListener extends Thread {
	private Socket socket;
	private boolean forever = true;
	private BasicBuilder builder;
	private long receievedCount = 0;

	private boolean verbose = true;

	public ClientListener(Socket socket) {
		this.socket = socket;
		builder = new BasicBuilder();
	}

	public void stopListening() {
		forever = false;
		this.interrupt();
	}

	@Override
	public void run() throws RuntimeException {
		byte[] raw = new byte[2048];
		while (forever) {
			try {
				int len = socket.getInputStream().read(raw);
				if (len <= 0)
					continue;

				if (verbose) {
					String rs = new String(raw);
					System.out.println("--> RCV: " + rs);
				}

				try {
					List<Message> list = builder.decode(new String(raw, 0, len).getBytes());
					for (Message msg : list) {
						receievedCount++;
						if (verbose)
							System.out.println("--> " + msg);
					}
				} catch (Exception e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
			} catch (IOException e) {
				// TODO report but, continue
			}
		}

	}

	public long getReceievedCount() {
		return receievedCount;
	}
}
