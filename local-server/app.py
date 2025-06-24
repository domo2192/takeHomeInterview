import os
import json
import time
import paramiko
import logging
from flask import Flask, jsonify, request
from datetime import datetime
import threading

logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/local-server.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class LegacySystemClient:
    def __init__(self):
        self.ssh_config = {
            'hostname': os.environ.get('LEGACY_HOST', 'remote-server-1'),
            'port': 22,
            'username': os.environ.get('LEGACY_USER', 'legacy'), 
            'key_filename': os.environ.get('SSH_KEY_PATH', '/app/ssh_keys/id_rsa'),
            'timeout': 30
        }
        self.job_timeout = int(os.environ.get('JOB_TIMEOUT', '60'))
        logger.info(f"SSH Config: {self.ssh_config}")
        
    def submit_file_request(self, filename):
        try:
            logger.info(f"Submitting file request for: {filename}")
            
            with paramiko.SSHClient() as ssh:
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                
                logger.info(f"Attempting SSH connection to {self.ssh_config['hostname']}:{self.ssh_config['port']}")
                ssh.connect(**self.ssh_config)
                logger.info("SSH connection established successfully")
                
                command = f"/home/legacy/proxy_request.sh '{filename}'"
                logger.info(f"Executing command: {command}")
                
                stdin, stdout, stderr = ssh.exec_command(command)
                
                stdout_output = stdout.read().decode('utf-8')
                stderr_output = stderr.read().decode('utf-8')
                exit_status = stdout.channel.recv_exit_status()
                
                logger.info(f"Command exit status: {exit_status}")
                logger.info(f"STDOUT: {stdout_output}")
                logger.info(f"STDERR: {stderr_output}")
                
                if exit_status == 0:
                    output = stdout_output.strip()
                    logger.info(f"Legacy system response: {output}")
                    
                    try:
                        return json.loads(output)
                    except json.JSONDecodeError:
                        logger.error(f"Invalid JSON response: {output}")
                        return self._error_response(filename, f"Invalid response format: {output}")
                else:
                    logger.error(f"Legacy system error - Exit code: {exit_status}")
                    return self._error_response(filename, f"Legacy system processing failed - Exit code: {exit_status}, Error: {stderr_output}")
                    
        except paramiko.AuthenticationException as e:
            logger.error(f"SSH Authentication failed: {e}")
            return self._error_response(filename, f"SSH Authentication failed: {e}")
        except paramiko.SSHException as e:
            logger.error(f"SSH connection error: {e}")
            return self._error_response(filename, f"SSH connection error: {e}")
        except Exception as e:
            logger.error(f"Error communicating with legacy system: {e}")
            return self._error_response(filename, str(e))
    
    def _error_response(self, filename, error_msg):
        return {
            "status": "error",
            "data": "",
            "msg": f"there was an error retrieving {filename}, {error_msg}"
        }


@app.route('/file/<filename>')
def get_file(filename):
    start_time = time.time()
    logger.info(f"Received request for file: {filename}")
    
    client = LegacySystemClient()
    result = client.submit_file_request(filename)
    
    processing_time = time.time() - start_time
    logger.info(f"Request completed in {processing_time:.2f} seconds")
    
    return jsonify(result)

@app.route('/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "local-server"
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting Local Server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)