# nlevo
- this is common lib for evo.

## 1. nlevoconn
- docker
    - def run_command : command in docker
- rabbitmq
    - class RabbitMQConnection : singleton blocking connector
    - class RabbitMQConfig

## 2. nlevoutils
- common
    - def get_parents_path
    - def seconds_to_time
- constant
    - global constant
    - class ServiceType
    - class MessageType
    - class Exchange
    - class RoutingKey
    - class RedisDBEnum
-default
    - global constant
- docker
    - def is_running_in_docker
- exceptions
    - def handle_errors
    - def handle_none_return
- log_organizer
    - class LogOrganizer
- multi_process
    - class ProcessMaintainer
    - class ProcessUtil
- subprocess
    - def get_output
    - def command_generator
    - def get_pid
    - def get_pid_grep
    - def get_pid_by_pgrep
    - def kill_pid
    - def kill_pid_grep
    - def kill_process_by_command
- timezone
    - def timestamp_to_datetime_with_timezone_str
    - def timestamp_to_datetime_with_timezone
