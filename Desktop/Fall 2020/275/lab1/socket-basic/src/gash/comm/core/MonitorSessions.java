package gash.comm.core;

import java.util.Set;

/**
 * 
 * @author gash
 * 
 */
public class MonitorSessions extends Thread {
	private boolean forever = true;
	private long interval;
	private long idleTime;
	private Sessions sessions;

	/**
	 * create a new monitor
	 * 
	 * @param interval
	 *            long how often to check
	 * @param idleness
	 *            long what is considered idle
	 */
	public MonitorSessions(Sessions sessions, long interval, long idleness) {
		this.sessions = sessions;
		this.interval = interval;
		this.idleTime = idleness;
	}

	/**
	 * stop monitoring on the next interval
	 */
	public void stopMonitoring() {
		forever = false;
	}

	/**
	 * ran in the thread to monitor for idle threads
	 */
	public void run() {
		while (forever) {
			try {
				long idle = System.currentTimeMillis() - idleTime;
				Thread.sleep(interval);
				if (!forever) {
					break;
				}

				for (SessionHandler sh : sessions.getConnections()) {
					if (sh.getLastContact() < idle) {
						System.out.println("MonitorSessions stopping session " + sh.getSessionId());

						sh.stopSession();
						sessions.remove(sh);
					}
				}
			} catch (Exception e) {
				break;
			}
		}
	}
} // class MonitorSessions
