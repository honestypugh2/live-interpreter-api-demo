import { ConnectionStatus as ConnectionStatusType } from '../types/translation';

interface Props {
  status: ConnectionStatusType;
}

const ConnectionStatus = ({ status }: Props) => {
  const statusConfig = {
    disconnected: {
      color: 'status-disconnected',
      text: 'Disconnected',
      bgColor: 'bg-red-50 dark:bg-red-900/20',
      textColor: 'text-red-700 dark:text-red-300',
    },
    connecting: {
      color: 'status-connecting',
      text: 'Connecting...',
      bgColor: 'bg-yellow-50 dark:bg-yellow-900/20',
      textColor: 'text-yellow-700 dark:text-yellow-300',
    },
    connected: {
      color: 'status-connected',
      text: 'Connected',
      bgColor: 'bg-green-50 dark:bg-green-900/20',
      textColor: 'text-green-700 dark:text-green-300',
    },
    error: {
      color: 'status-disconnected',
      text: 'Connection Error',
      bgColor: 'bg-red-50 dark:bg-red-900/20',
      textColor: 'text-red-700 dark:text-red-300',
    },
  };

  const config = statusConfig[status];

  return (
    <div className={`card ${config.bgColor} border-l-4 ${config.textColor.includes('green') ? 'border-green-500' : config.textColor.includes('yellow') ? 'border-yellow-500' : 'border-red-500'}`}>
      <div className="flex items-center justify-center">
        <span className={`status-indicator ${config.color}`}></span>
        <span className={`font-semibold ${config.textColor}`}>
          {config.text}
        </span>
      </div>
    </div>
  );
};

export default ConnectionStatus;
