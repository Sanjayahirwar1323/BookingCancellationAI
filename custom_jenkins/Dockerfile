# Use Jenkins LTS image with OpenJDK 17 (ARM64 compatible)
FROM jenkins/jenkins:lts-jdk17

# Switch to root user to install dependencies
USER root

# Install prerequisites and Docker for ARM64 architecture
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends apt-transport-https ca-certificates curl gnupg software-properties-common && \
    install -m 0755 -d /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | tee /etc/apt/keyrings/docker.asc > /dev/null && \
    chmod a+r /etc/apt/keyrings/docker.asc && \
    echo "deb [arch=arm64 signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian bullseye stable" > /etc/apt/sources.list.d/docker.list && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends docker-ce docker-ce-cli containerd.io && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Add Jenkins user to the Docker group (create if not exists)
RUN groupadd -f docker && usermod -aG docker jenkins

# Create Docker directory and set volume
VOLUME /var/lib/docker

# Switch back to the Jenkins user
USER jenkins