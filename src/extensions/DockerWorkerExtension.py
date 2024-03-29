import docker


def build_docker_image(dockerfile_path, image_name):
    client = docker.from_env()

    print("Строим образ Docker...")
    try:
        response = client.images.build(
            path=dockerfile_path,
            tag=image_name,
            rm=True,  # Удалить промежуточные контейнеры после построения образа
            quiet=True,  # Выводить информацию о процессе сборки
        )
    except docker.errors.BuildError as e:
        print(f"Ошибка при сборке образа: {e}")
    else:
        print(f"Образ Docker {image_name} успешно создан.")


def create_docker_container(
    container_name=None, image_name=None, host_port=None, container_port=None
):
    if container_port == None:
        container_port = host_port
    
    client = docker.from_env()

    if not container_name or not image_name:
        print("none container or image name")
        return False

    if not host_port or not container_port:
        ports = None
    else:
        ports = {f"{container_port}/tcp": host_port}

    print("creating new Docker container...")
    try:
        container = client.containers.run(
            image=image_name, name=container_name, ports=ports, detach=True
        )
    except docker.errors.ContainerError as e:
        print(f"Ошибка при создании контейнера: {e}")
        return False
    else:
        print(f"Docker container {container_name} successfully created.")
        print(f"container id: {container.id}")
        return container.id


if __name__ == "__main__":
    create_docker_container(
        container_name="factorio_test_server_python",
        image_name="factorio:1.1.87",
        host_port="8090",
        container_port="8090",
    )
