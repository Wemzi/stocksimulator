# Read Me First
One thing worth noting is that the application was developed on tested on an Apple Silicon Mac, so other operating systems and architectures might experience issues, as those were not tested.

# Getting Started
The repository does not contain the Docker container and it must be built using the included Dockerfile.

This can be done using: 
` docker build -t stocksimulator . `

The docker image can be built and launched with the following options: 
` docker run -p 30000:8080 -p 30001:8000 stocksimulator:latest `

### Reference Documentation
For further reference, please consider the following sections:

* [Official Gradle documentation](https://docs.gradle.org)
* [Spring Boot Gradle Plugin Reference Guide](https://docs.spring.io/spring-boot/3.4.0/gradle-plugin)
* [Create an OCI image](https://docs.spring.io/spring-boot/3.4.0/gradle-plugin/packaging-oci-image.html)
* [Spring Boot DevTools](https://docs.spring.io/spring-boot/3.4.0/reference/using/devtools.html)
* [OAuth2 Client](https://docs.spring.io/spring-boot/3.4.0/reference/web/spring-security.html#web.security.oauth2.client)

### Additional Links
These additional references should also help you:

* [Gradle Build Scans – insights for your project's build](https://scans.gradle.com#gradle)

