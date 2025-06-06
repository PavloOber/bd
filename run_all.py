import subprocess
import sys
import os
import time
import threading
from pathlib import Path

class ServerThread(threading.Thread):
    def __init__(self, command, cwd=None):
        super().__init__()
        self.command = command
        self.cwd = cwd
        self.process = None
        
    def run(self):
        try:
            self.process = subprocess.Popen(
                self.command,
                cwd=self.cwd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Mostrar la salida del proceso
            if self.process.stdout:
                for line in self.process.stdout:
                    print(f"[{self.command[:20]}...] {line.strip()}")
                    
        except Exception as e:
            print(f"Error en {self.command}: {e}")
    
    def stop(self):
        if self.process:
            self.process.terminate()
            self.process.wait()

def main():
    # Obtener el directorio base del proyecto
    base_dir = Path(__file__).parent
    servers = []
    
    try:
        print("Iniciando servidores...")
        
        # Iniciar el servidor de MongoDB (API de reseñas)
        print("Iniciando API de MongoDB en http://localhost:5000")
        mongo_server = ServerThread("python mongobd/mongo.py", cwd=base_dir)
        mongo_server.daemon = True
        mongo_server.start()
        servers.append(mongo_server)
        time.sleep(2)  # Esperar a que el servidor arranque
        
        # Iniciar el servidor de FastAPI (API principal)
        print("Iniciando API en http://localhost:5001")
        api_server = ServerThread("python run_api.py", cwd=base_dir)
        api_server.daemon = True
        api_server.start()
        servers.append(api_server)
        time.sleep(2)  # Esperar a que el servidor arranque
        
        # Iniciar el servidor HTTP para el frontend
        print("Iniciando servidor frontend en http://localhost:3000")
        frontend_server = ServerThread("python -m http.server 3000", cwd=base_dir)
        frontend_server.daemon = True
        frontend_server.start()
        servers.append(frontend_server)
        
        print("\n¡Servidores iniciados!")
        print("- API de MongoDB: http://localhost:5000")
        print("- API Principal: http://localhost:5001")
        print("- Frontend: http://localhost:3000")
        print("\nPresiona Ctrl+C para detener los servidores")
        
        # Mantener el script principal en ejecución
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nDeteniendo servidores...")
    finally:
        # Detener todos los servidores
        for server in servers:
            server.stop()
        print("Todos los servidores han sido detenidos.")
        sys.exit(0)

if __name__ == "__main__":
    main()
