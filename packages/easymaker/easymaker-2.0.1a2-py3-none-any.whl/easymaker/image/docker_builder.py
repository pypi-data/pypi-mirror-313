# -*- coding: utf-8 -*-
import json
import os
import tarfile
import tempfile

import docker

from easymaker.common import constants, exceptions


class DockerBuilder:
    def __init__(self, container_registry=None, container_username=None, container_password=None):

        self.container_registry = container_registry
        self.container_username = container_username
        self.container_password = container_password

        # TODO Default Worker 생성된 별도의 외부 Docker 빌드서버 사용 (base_url)
        self.docker_client = docker.APIClient(version="auto")

    def _login(self, registry, username, password):
        self.docker_client.login(registry=registry, username=username, password=password, reauth=True)

    def build(
        self,
        build_image,
        dockerfile_path=None,
        base_image=None,
        docker_command=None,
        contents_dir=None,
        work_dir=None,
        install_requirements_before_copy=False,
    ):
        """
        :param build_image: 빌드된 이미지가 저장될 이미지 이름
        :param dockerfile_path: dockerfile path가 주어진 경우 그대로 빌드, 없는 경우 아래 파라미터들 사용해서 도커파일 생성,
        :param contents_dir: 도커 이미지에 포함시킬 파일들이 있는 로컬 경로
        :param base_image: docker base image
        :param docker_command: dockerfile CMD 명령에 추가될 내용
        :param work_dir: 빌드된 도커 이미지 내 작업 경로
        :return:
        """
        self._login(constants.DEFAULT_CONTAINER_REGISTRY_URI, constants.DEFAULT_CONTAINER_REGISTRY_USERNAME, constants.DEFAULT_CONTAINER_REGISTRY_PASSWORD)

        if dockerfile_path:
            if not contents_dir:
                contents_dir = os.path.dirname(dockerfile_path)
        else:
            dockerfile_path = self._write_dockerfile(
                docker_command=docker_command,
                base_image=base_image,
                work_dir=work_dir,
                install_requirements_before_copy=install_requirements_before_copy,
            )

        _context_tar_path = self._context_tar_gz(dockerfile_path=dockerfile_path, contents_dir=contents_dir)

        with open(_context_tar_path, "rb") as fileobj:
            build_output = self.docker_client.build(fileobj=fileobj, tag=build_image, custom_context=True, encoding="utf-8")
            for line in build_output:
                self._process_stream(line)

    def push(self, image):
        self._login(self.container_registry, self.container_username, self.container_password)

        print("Publishing image {}...".format(image))
        for line in self.docker_client.push(image, stream=True):
            self._process_stream(line)

    def _process_stream(self, line):
        """
        Parse the docker command output by line
        """
        lines = line.decode("utf-8").strip().split("\n")
        for line in lines:
            try:
                json_data = json.loads(line)
                if json_data.get("error"):
                    msg = str(json_data.get("error", json_data))
                    print("Build failed: %s", msg)
                    raise exceptions.EasyMakerDockerError("Image build failed: " + msg)
                else:
                    if json_data.get("stream"):
                        msg = "Build output: {}".format(json_data["stream"].strip())
                    elif json_data.get("status"):
                        msg = "Push output: {} {}".format(json_data["status"], json_data.get("progress"))
                    elif json_data.get("aux"):
                        msg = "Push finished: {}".format(json_data.get("aux"))
                    else:
                        msg = str(json_data)
                    print(msg)

            except json.JSONDecodeError:
                print("JSON decode error: {}".format(line))

    def _write_dockerfile(
        self,
        base_image=None,
        docker_command=None,
        destination=None,
        work_dir=None,
        install_requirements_before_copy=False,
    ):
        if not work_dir:
            work_dir = constants.DEFAULT_WORKDIR
        if not destination:
            _, destination = tempfile.mkstemp(prefix="/tmp/dockerfile_")

        content_lines = ["FROM {}".format(base_image), "WORKDIR {}".format(work_dir), "ENV EASYMAKER_RUNTIME 1"]

        if install_requirements_before_copy:
            content_lines.append("COPY ./requirements.txt {}".format(work_dir))
        content_lines.append("RUN if [ -e requirements.txt ];" + "then pip install --no-cache -r requirements.txt; fi")
        copy_context = "COPY ./ {}".format(work_dir)
        content_lines.append(copy_context)

        if docker_command:
            content_lines.append("CMD {}".format(" ".join(docker_command)))

        content = "\n".join(content_lines)
        with open(destination, "w") as f:
            f.write(content)
        return destination

    def _context_tar_gz(self, dockerfile_path, contents_dir=None, output_file=None):
        if not output_file:
            _, output_file = tempfile.mkstemp(prefix="/tmp/fairing_context_")
        print(f"Creating docker context: {output_file}")
        with tarfile.open(output_file, "w:gz", dereference=True) as tar:
            print(f"Context: {output_file}, Adding {dockerfile_path}")
            tar.add(dockerfile_path, arcname="Dockerfile")
            if contents_dir:
                print(f"Context: {output_file}, Adding {contents_dir}")
                tar.add(contents_dir, arcname=".")

        return output_file


# TODO. 배포시 제거
if __name__ == "__main__":
    USER_CONTAINER_REGISTRY_URI = "1bc85ba3-kr1-registry.container.cloud.toast.com/easymaker"
    CONTAINER_USERNAME = "I7XDyq6mxK4DKLUfWbFB"
    CONTAINER_PASSWORD = "z6aJqeCXAtYCFNCI"

    TRAINING_IMAGE = USER_CONTAINER_REGISTRY_URI + "/build_test:0.5"

    docker_builder = DockerBuilder(USER_CONTAINER_REGISTRY_URI, CONTAINER_USERNAME, CONTAINER_PASSWORD)

    # build example
    docker_builder.build(build_image=TRAINING_IMAGE, dockerfile_path="/Users/nhn/IdeaProjects/EasyMaker.SDK/sample/docker/Dockerfile")
    # docker_builder.build(build_image=TRAINING_IMAGE,
    #                      base_image='centos:latest',
    #                      contents_dir='/Users/nhn/IdeaProjects/EasyMaker.SDK/sample/docker',
    #                      work_dir='/app/',
    #                      docker_command=['echo hello'])

    # push
    docker_builder.push(TRAINING_IMAGE)
