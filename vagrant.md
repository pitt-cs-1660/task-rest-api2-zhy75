# **Vagrant with Docker and VirtualBox**
#### **YOU SHOULD NOT NEED TO EDIT THE [VagrantFile](Vagrantfile)**

This guide will walk you through setting up your local development environment using **Vagrant** with **Docker** or **VirtualBox** as the provider.

We are using **Vagrant** to standardize our local development environment. Instead of installing dependencies directly on your machine, Vagrant will spin up a **Docker container** or a **VirtualBox virtual machine (VM)** for your development work. This ensures a consistent environment across operating systems (Windows, macOS, or Linux) and eliminates "it works on my machine" issues.

While Docker is the preferred provider for lightweight containers, **VirtualBox** serves as a reliable fallback, especially for x86-based systems, including Windows machines.

---

## **Prerequisites**

Before you begin, please ensure you have the following installed:

### 1. **Docker**
- Download and install **Docker Desktop** for your platform:
     - [Docker for Windows](https://www.docker.com/products/docker-desktop)
     - [Docker for macOS](https://www.docker.com/products/docker-desktop)
     - Linux: Install via your package manager (e.g., `sudo apt install docker.io`).
- Verify that Docker is installed:
  ```bash
  docker --version
  ```
  You should see the Docker version output.

### 2. **VirtualBox** (Windows fallback)
- Download and install **VirtualBox** from:
     - [VirtualBox Downloads](https://www.virtualbox.org/wiki/Downloads)
- Verify that VirtualBox is installed:
  ```bash
  virtualbox --version
  ```
  You should see the VirtualBox version output.

- VirtualBox is recommended for:
     - **Windows users** who face compatibility issues with Docker Desktop.
     - **x86-based machines** (e.g., older macOS devices or Linux systems).

> **Note**: VirtualBox does not work on ARM-based systems like Apple M1/M2/M3 Macs. Use Docker on these devices.

### 3. **Vagrant**
- Download and install **Vagrant**:
     - [Vagrant for all platforms](https://developer.hashicorp.com/vagrant/downloads).
- Verify that Vagrant is installed:
  ```bash
  vagrant --version
  ```
  You should see the Vagrant version output.

### 4. **Vagrant Docker Plugin (if using Docker provider)**
- If you are using Docker as the provider, ensure compatibility by installing:
  ```bash
  vagrant plugin install vagrant-docker-compose
  ```

---

## **Vagrant Commands Explained**

Below are the most commonly used Vagrant commands during development:

### 1. **Start the Development Environment:**
   ```bash
   # ARM-based systems (e.g., M1/M2/M3 Macs) or Docker users:
   vagrant up --provider=docker
   
   # For Windows or x86-based systems using VirtualBox:
   vagrant up --provider=virtualbox
   ```
- Spins up the Docker container or VirtualBox VM.
- The first run will download the base image or VM box and configure the environment.

### 2. **SSH into the Environment:**
   ```bash
   vagrant ssh
   ```
- Opens an interactive shell session inside the container or VM.

### 3. **Stop the Development Environment:**
   ```bash
   vagrant halt
   ```
- Stops the running container or VM without destroying it.

### 4. **Restart the Environment and Reprovision:**
   ```bash
   vagrant reload --provision
   ```
- Restarts the container or VM and reapplies any provisioning scripts.

### 5. **Destroy the Environment:**
   ```bash
   vagrant destroy -f
   ```
- Removes the container or VM entirely.

### 6. **Check Environment Status:**
   ```bash
   vagrant status
   ```
- Displays the current status of the Vagrant-managed environment.

---

## **Accessing the API**

After running:
```bash
vagrant ssh
cd app
poetry run uvicorn cc_simple_server.server:app --reload --host 0.0.0.0 --port 8000
```
The API will be available at:
```
http://localhost:8000
```

---

## **Why Are We Using Vagrant with Docker?**

- **Lightweight**: Docker containers are faster to spin up and have a smaller footprint than VMs.
- **Portability**: Ensures a consistent environment across macOS, Windows, and Linux.
- **Modern Systems**: Ideal for ARM-based systems like Apple M1/M2/M3 Macs.

---

## **Why Are We Using Vagrant with VirtualBox?**

- **Compatibility**: Windows and older x86-based systems sometimes face issues with Docker, particularly with file sharing.
- **Cross-Platform Support**: VirtualBox ensures students on incompatible systems can still complete the assignment.
- **Fallback**: VirtualBox provides a robust alternative when Docker cannot be used.

---

## **Troubleshooting**

### **1. File Sync Issues**
- If changes to files on your host machine do not appear in the environment:
     - For Docker:
          - Ensure the project directory is file-shared in Docker Desktop settings.
     - For VirtualBox:
          - Restart the VM:
            ```bash
            vagrant reload
            ```

### **2. Shared Folder Permissions**
- If you encounter `Permission denied` errors in the environment:
  ```bash
  sudo chmod -R u+rwx /home/vagrant/app
  ```

### **3. FastAPI Not Reloading**
- If code changes are not reflected:
     - Ensure you are running Uvicorn with the `--reload` flag:
       ```bash
       poetry run uvicorn cc_simple_server.server:app --reload --host 0.0.0.0 --port 8000
       ```

---

## **Summary**

- Use **Docker** as the preferred provider for modern systems and lightweight environments.
- Use **VirtualBox** as a fallback for Windows and x86-based systems.
- Vagrant abstracts away complex configurations, allowing you to focus on development without worrying about system-specific issues.
