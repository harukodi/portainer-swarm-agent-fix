#!/usr/bin/env python3
import subprocess, psutil, time, argparse
wait_time = 120
parser = argparse.ArgumentParser(description="Recreate Portainer agents.")
parser.add_argument("--skip-wait", action="store_true", help="Skip initial wait time.")
args = parser.parse_args()

def check_docker_service_status(timeout=10):
    print("Checking Docker service status...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == 'dockerd':
                print("Docker service is running!")
                return True
    print("Docker service is not running exiting!")
    exit()
            
def cleanup_portainer_service_and_network():
    print("Cleaning up Portainer service and network...")
    time.sleep(5)
    try:
        subprocess.run("sudo docker service rm portainer_agent; sudo docker network rm portainer_agent_network", shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        print("Portainer service and network cleaned up!")
    except:
        pass

def recreate_portainer_agents():
    print("Recreating Portainer agents...")
    time.sleep(5)
    subprocess.run("sudo docker network create --driver overlay portainer_agent_network; sudo docker service create --name portainer_agent --network portainer_agent_network -p 9001:9001/tcp --mode global --constraint 'node.platform.os == linux' --mount type=bind,src=/var/run/docker.sock,dst=/var/run/docker.sock --mount type=bind,src=/var/lib/docker/volumes,dst=/var/lib/docker/volumes --mount type=bind,src=/,dst=/host portainer/agent:2.27.3", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("Portainer agents recreated.")

if __name__ == "__main__":
    if args.skip_wait:
        check_docker_service_status()
        cleanup_portainer_service_and_network()
        recreate_portainer_agents()
    elif not args.skip_wait:
        print(f"Waiting {wait_time} seconds for other nodes to become available...")
        time.sleep(wait_time)
        check_docker_service_status()
        cleanup_portainer_service_and_network()
        recreate_portainer_agents()
