// Frontend logging utility for Lost and Found functionality

interface LogEntry {
  timestamp: string;
  level: 'INFO' | 'WARN' | 'ERROR' | 'DEBUG';
  component: string;
  action: string;
  message: string;
  details?: any;
  error?: any;
  userId?: string;
  qrId?: string;
}

class Logger {
  private component: string;
  private isDevelopment: boolean;

  constructor(component: string) {
    this.component = component;
    this.isDevelopment = import.meta.env.DEV || import.meta.env.MODE === 'development';
  }

  private createLogEntry(
    level: LogEntry['level'],
    action: string,
    message: string,
    details?: any,
    error?: any,
    userId?: string,
    qrId?: string
  ): LogEntry {
    return {
      timestamp: new Date().toISOString(),
      level,
      component: this.component,
      action,
      message,
      details,
      error: error ? {
        message: error.message,
        stack: error.stack,
        name: error.name
      } : undefined,
      userId,
      qrId
    };
  }

  private log(entry: LogEntry): void {
    // Always log to console in development
    if (this.isDevelopment) {
      const consoleMethod = entry.level === 'ERROR' ? 'error' : 
                           entry.level === 'WARN' ? 'warn' : 
                           entry.level === 'DEBUG' ? 'debug' : 'log';
      
      console[consoleMethod](
        `[${entry.timestamp}] [${entry.level}] [${entry.component}] ${entry.action}: ${entry.message}`,
        entry.details ? entry.details : '',
        entry.error ? entry.error : ''
      );
    }

    // Store in localStorage for debugging (limited to last 100 entries)
    this.storeLog(entry);
  }

  private storeLog(entry: LogEntry): void {
    try {
      const logsKey = 'quickqr_lost_and_found_logs';
      const existingLogs = localStorage.getItem(logsKey);
      const logs: LogEntry[] = existingLogs ? JSON.parse(existingLogs) : [];
      
      logs.push(entry);
      
      // Keep only last 100 entries
      if (logs.length > 100) {
        logs.splice(0, logs.length - 100);
      }
      
      localStorage.setItem(logsKey, JSON.stringify(logs));
    } catch (error) {
      // Silently fail if localStorage is not available
      console.warn('Failed to store log entry:', error);
    }
  }

  info(action: string, message: string, details?: any, userId?: string, qrId?: string): void {
    const entry = this.createLogEntry('INFO', action, message, details, undefined, userId, qrId);
    this.log(entry);
  }

  warn(action: string, message: string, details?: any, userId?: string, qrId?: string): void {
    const entry = this.createLogEntry('WARN', action, message, details, undefined, userId, qrId);
    this.log(entry);
  }

  error(action: string, message: string, error?: any, details?: any, userId?: string, qrId?: string): void {
    const entry = this.createLogEntry('ERROR', action, message, details, error, userId, qrId);
    this.log(entry);
  }

  debug(action: string, message: string, details?: any, userId?: string, qrId?: string): void {
    if (this.isDevelopment) {
      const entry = this.createLogEntry('DEBUG', action, message, details, undefined, userId, qrId);
      this.log(entry);
    }
  }

  // Utility method to log API calls
  logApiCall(
    endpoint: string,
    method: string,
    requestData?: any,
    responseData?: any,
    error?: any,
    userId?: string,
    qrId?: string
  ): void {
    const action = `API_${method.toUpperCase()}`;
    const message = `${method} ${endpoint}`;
    const details = {
      endpoint,
      method,
      requestData,
      responseData,
      hasError: !!error
    };

    if (error) {
      this.error(action, message, error, details, userId, qrId);
    } else {
      this.info(action, message, details, userId, qrId);
    }
  }

  // Utility method to log user actions
  logUserAction(
    action: string,
    message: string,
    details?: any,
    userId?: string,
    qrId?: string
  ): void {
    this.info(`USER_${action.toUpperCase()}`, message, details, userId, qrId);
  }

  // Get stored logs for debugging
  getStoredLogs(): LogEntry[] {
    try {
      const logsKey = 'quickqr_lost_and_found_logs';
      const existingLogs = localStorage.getItem(logsKey);
      return existingLogs ? JSON.parse(existingLogs) : [];
    } catch (error) {
      console.warn('Failed to retrieve stored logs:', error);
      return [];
    }
  }

  // Clear stored logs
  clearStoredLogs(): void {
    try {
      localStorage.removeItem('quickqr_lost_and_found_logs');
    } catch (error) {
      console.warn('Failed to clear stored logs:', error);
    }
  }
}

// Create specific loggers for different components
export const lostAndFoundLogger = new Logger('LostAndFound');
export const apiLogger = new Logger('API');
export const uiLogger = new Logger('UI');

// Export the Logger class for custom loggers
export { Logger };
export type { LogEntry };
