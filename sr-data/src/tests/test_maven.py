"""
Test case for maven.
"""
# The MIT License (MIT)
#
# Copyright (c) 2024 Aliaksei Bialiauski
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import os
import unittest
from tempfile import TemporaryDirectory

import pandas as pd
import pytest
from sr_data.steps.maven import main, merge


class TestMaven(unittest.TestCase):

    @pytest.mark.nightly
    def test_finds_maven_projects(self):
        with TemporaryDirectory() as temp:
            path = os.path.join(temp, "maven.csv")
            main(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    "resources/to-maven.csv"
                ),
                path,
                os.environ["GH_TESTING_TOKEN"]
            )
            frame = pd.read_csv(path)
            self.assertEqual(
                frame.iloc[0]["maven_plugins"],
                "[com.github.volodya-lombrozo:jtcop-maven-plugin,maven-surefire-plugin,org.apache.maven.plugins:maven-checkstyle-plugin,org.apache.maven.plugins:maven-compiler-plugin,org.apache.maven.plugins:maven-gpg-plugin,org.apache.maven.plugins:maven-invoker-plugin,org.apache.maven.plugins:maven-javadoc-plugin,org.apache.maven.plugins:maven-source-plugin,org.apache.maven.plugins:maven-verifier-plugin,org.jacoco:jacoco-maven-plugin,org.sonatype.plugins:nexus-staging-maven-plugin,ru.l3r8y:sa-tan]"
            )
            self.assertEqual(frame.iloc[0]["maven_projects_count"], 1.0)
            self.assertEqual(frame.iloc[0]["maven_wars_count"], 0.0)
            self.assertEqual(frame.iloc[0]["maven_jars_count"], 1.0)
            self.assertEqual(frame.iloc[0]["maven_poms_count"], 0.0)

    @pytest.mark.nightly
    def test_skips_repos_without_maven(self):
        with TemporaryDirectory() as temp:
            path = os.path.join(temp, "maven.csv")
            main(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    "resources/to-maven-skip.csv"
                ),
                path,
                os.environ["GH_TESTING_TOKEN"]
            )
            frame = pd.read_csv(path)
            self.assertTrue(len(frame) == 0)

    @pytest.mark.nightly
    def test_skips_plugin_without_artifact(self):
        with TemporaryDirectory() as temp:
            path = os.path.join(temp, "maven.csv")
            main(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    "resources/to-maven-without-artifact.csv"
                ),
                path,
                os.environ["GH_TESTING_TOKEN"]
            )
            frame = pd.read_csv(path)
            self.assertEqual(
                frame.iloc[0]["maven_plugins"],
                "[org.jetbrains.kotlin:kotlin-maven-plugin,org.springframework.boot:spring-boot-maven-plugin]"
            )

    @pytest.mark.fast
    def test_merges_projects_in_one_profile(self):
        merged = merge(
            [
                {
                    "path": "core-spring/auto-configure/pom.xml",
                    "content": "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<project xmlns=\"http://maven.apache.org/POM/4.0.0\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n\txsi:schemaLocation=\"http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd\">\n\t<modelVersion>4.0.0</modelVersion>\n\n\t<groupId>com.therealdanvega</groupId>\n\t<artifactId>auto-configure</artifactId>\n\t<version>0.0.1-SNAPSHOT</version>\n\t<packaging>jar</packaging>\n\n\t<name>auto-configure</name>\n\t<description>Spring Boot Auto Configure demo</description>\n\n\t<parent>\n\t\t<groupId>org.springframework.boot</groupId>\n\t\t<artifactId>spring-boot-starter-parent</artifactId>\n\t\t<version>1.3.0.BUILD-SNAPSHOT</version>\n\t\t<relativePath/> <!-- lookup parent from repository -->\n\t</parent>\n\n\t<properties>\n\t\t<project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>\n\t\t<java.version>1.8</java.version>\n\t</properties>\n\n\t<dependencies>\n\t\t<dependency>\n\t\t\t<groupId>org.springframework.boot</groupId>\n\t\t\t<artifactId>spring-boot-starter-web</artifactId>\n\t\t</dependency>\n\t\t\n\t\t<dependency>\n\t\t\t<groupId>org.springframework.boot</groupId>\n\t\t\t<artifactId>spring-boot-starter-test</artifactId>\n\t\t\t<scope>test</scope>\n\t\t</dependency>\n\t</dependencies>\n\t\n\t<build>\n\t\t<plugins>\n\t\t\t<plugin>\n\t\t\t\t<groupId>org.springframework.boot</groupId>\n\t\t\t\t<artifactId>spring-boot-maven-plugin</artifactId>\n\t\t\t</plugin>\n\t\t</plugins>\n\t</build>\n\t\n\t<repositories>\n\t\t<repository>\n\t\t\t<id>spring-snapshots</id>\n\t\t\t<name>Spring Snapshots</name>\n\t\t\t<url>https://repo.spring.io/snapshot</url>\n\t\t\t<snapshots>\n\t\t\t\t<enabled>true</enabled>\n\t\t\t</snapshots>\n\t\t</repository>\n\t\t<repository>\n\t\t\t<id>spring-milestones</id>\n\t\t\t<name>Spring Milestones</name>\n\t\t\t<url>https://repo.spring.io/milestone</url>\n\t\t\t<snapshots>\n\t\t\t\t<enabled>false</enabled>\n\t\t\t</snapshots>\n\t\t</repository>\n\t</repositories>\n\t<pluginRepositories>\n\t\t<pluginRepository>\n\t\t\t<id>spring-snapshots</id>\n\t\t\t<name>Spring Snapshots</name>\n\t\t\t<url>https://repo.spring.io/snapshot</url>\n\t\t\t<snapshots>\n\t\t\t\t<enabled>true</enabled>\n\t\t\t</snapshots>\n\t\t</pluginRepository>\n\t\t<pluginRepository>\n\t\t\t<id>spring-milestones</id>\n\t\t\t<name>Spring Milestones</name>\n\t\t\t<url>https://repo.spring.io/milestone</url>\n\t\t\t<snapshots>\n\t\t\t\t<enabled>false</enabled>\n\t\t\t</snapshots>\n\t\t</pluginRepository>\n\t</pluginRepositories>\n\n</project>\n"
                },
                {
                    "path": "core-spring/beans/pom.xml",
                    "content": "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<project xmlns=\"http://maven.apache.org/POM/4.0.0\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n\txsi:schemaLocation=\"http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd\">\n\t<modelVersion>4.0.0</modelVersion>\n\n\t<groupId>com.therealdanvega</groupId>\n\t<artifactId>sbeans</artifactId>\n\t<version>0.0.1-SNAPSHOT</version>\n\t<packaging>jar</packaging>\n\n\t<name>SpringBeans</name>\n\t<description>Spring Beans Demo</description>\n\n\t<parent>\n\t\t<groupId>org.springframework.boot</groupId>\n\t\t<artifactId>spring-boot-starter-parent</artifactId>\n\t\t<version>1.3.0.BUILD-SNAPSHOT</version>\n\t\t<relativePath/> <!-- lookup parent from repository -->\n\t</parent>\n\n\t<properties>\n\t\t<project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>\n\t\t<java.version>1.8</java.version>\n\t</properties>\n\n\t<dependencies>\n\t\t<dependency>\n\t\t\t<groupId>org.springframework.boot</groupId>\n\t\t\t<artifactId>spring-boot-starter-web</artifactId>\n\t\t</dependency>\n\t\t\n\t\t<dependency>\n\t\t\t<groupId>org.springframework.boot</groupId>\n\t\t\t<artifactId>spring-boot-starter-test</artifactId>\n\t\t\t<scope>test</scope>\n\t\t</dependency>\n\t</dependencies>\n\t\n\t<build>\n\t\t<plugins>\n\t\t\t<plugin>\n\t\t\t\t<groupId>org.springframework.boot</groupId>\n\t\t\t\t<artifactId>spring-boot-maven-plugin</artifactId>\n\t\t\t</plugin>\n\t\t</plugins>\n\t</build>\n\t\n\t<repositories>\n\t\t<repository>\n\t\t\t<id>spring-snapshots</id>\n\t\t\t<name>Spring Snapshots</name>\n\t\t\t<url>https://repo.spring.io/snapshot</url>\n\t\t\t<snapshots>\n\t\t\t\t<enabled>true</enabled>\n\t\t\t</snapshots>\n\t\t</repository>\n\t\t<repository>\n\t\t\t<id>spring-milestones</id>\n\t\t\t<name>Spring Milestones</name>\n\t\t\t<url>https://repo.spring.io/milestone</url>\n\t\t\t<snapshots>\n\t\t\t\t<enabled>false</enabled>\n\t\t\t</snapshots>\n\t\t</repository>\n\t</repositories>\n\t<pluginRepositories>\n\t\t<pluginRepository>\n\t\t\t<id>spring-snapshots</id>\n\t\t\t<name>Spring Snapshots</name>\n\t\t\t<url>https://repo.spring.io/snapshot</url>\n\t\t\t<snapshots>\n\t\t\t\t<enabled>true</enabled>\n\t\t\t</snapshots>\n\t\t</pluginRepository>\n\t\t<pluginRepository>\n\t\t\t<id>spring-milestones</id>\n\t\t\t<name>Spring Milestones</name>\n\t\t\t<url>https://repo.spring.io/milestone</url>\n\t\t\t<snapshots>\n\t\t\t\t<enabled>false</enabled>\n\t\t\t</snapshots>\n\t\t</pluginRepository>\n\t</pluginRepositories>\n\n</project>\n"
                },
            ],
            "foo/bar"
        )
        self.assertEqual(merged["projects"], 2)
        self.assertEqual(merged["plugins"], ["org.springframework.boot:spring-boot-maven-plugin"])
        self.assertEqual(merged["packages"]["jars"], 2)
        self.assertEqual(merged["packages"]["wars"], 0)
        self.assertEqual(merged["packages"]["poms"], 0)

    @pytest.mark.nightly
    def test_returns_default_values_for_non_maven(self):
        with TemporaryDirectory() as temp:
            path = os.path.join(temp, "maven.csv")
            main(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    "resources/to-maven-non-maven.csv"
                ),
                path,
                os.environ["GH_TESTING_TOKEN"]
            )
            frame = pd.read_csv(path)
            self.assertEqual(len(frame.columns), 7)
            self.assertTrue("maven_projects_count" in frame.columns)
            self.assertTrue("maven_plugins" in frame.columns)
            self.assertTrue("maven_wars_count" in frame.columns)
            self.assertTrue("maven_jars_count" in frame.columns)
            self.assertTrue("maven_poms_count" in frame.columns)
