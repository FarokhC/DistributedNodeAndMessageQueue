package gash.comm.core;

import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentMap;

class Sessions {
	private ConcurrentMap<SessionHandler, SessionHandler> connections = new ConcurrentHashMap<SessionHandler, SessionHandler>();

	public Set<SessionHandler> getConnections() {
		return connections.keySet();
	}

	public void add(SessionHandler connection) {
		if (connection == null)
			return;
		connection.registerBack(this);
		this.connections.put(connection, connection);
	}

	public void remove(SessionHandler session) {
		this.connections.remove(session);
	}
}
