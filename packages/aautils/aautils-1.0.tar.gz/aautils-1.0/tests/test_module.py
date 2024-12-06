#!/usr/bin/env python3

import asyncio
import os
import sys

import yaml
from avocado.core.job import Job
from avocado.core.suite import TestSuite
from avocado.utils.podman import Podman

CONTAINER_IMAGE_MAPPING = {
    "CentOS Stream 9": ("redhat_based", "centos:stream9"),
    "Fedora 36": ("redhat_based", "fedora:36"),
    "Fedora 37": ("redhat_based", "fedora:37"),
}

METADATA_PATH = sys.argv[1]
with open(METADATA_PATH, "rb") as m:
    metadata = yaml.load(m, Loader=yaml.SafeLoader)

images = []
test_suites = []
for platform in metadata["supported_platforms"]:
    name = platform.replace(" ", "_")
    containerfile, image_version = CONTAINER_IMAGE_MAPPING.get(platform)
    loop = asyncio.get_event_loop()
    _, result, _ = loop.run_until_complete(
        Podman().execute(
            "build",
            "--no-cache",
            "--from",
            image_version,
            "-f",
            os.path.join("tests", "containerfiles", containerfile),
            ".",
        )
    )
    image = result.splitlines()[-1].decode()
    images.append(image)
    config = {"run.spawner": "podman", "spawner.podman.image": image}

    config["resolver.references"] = metadata["tests"]
    test_suites.append(TestSuite.from_config(config, name))


with Job(test_suites=test_suites) as j:
    rc = j.run()
    for image in images:
        loop.run_until_complete(Podman().execute("image", "rm", "-f", image))
    sys.exit(rc)
