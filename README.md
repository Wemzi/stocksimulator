# Read Me First
One thing worth noting is that the application was developed on tested on an Apple Silicon Mac, so other operating systems and architectures might experience issues, as those were not tested.

# Getting Started
The repository does not contain the Docker image and it must be built using the included Dockerfile.


This can be done using: 
` docker build -t stocksimulator . `

Before the full application can be run, a network has to be created so that the database and the applications can communicate. We can create this with: 

` docker network create stocksim-network `

The docker image can be launched with the following options: 
` docker run --name stocksim-app --network stocksim-network -p 30000:8080 -p 30001:8000 -p 30002:5173 stocksimulator:latest `

There is another docker image that is required, named 'postgres:latest'. At this point I couldn't make one image that contains all the dependencies. this is also needed to be run, with this command:

` docker run --name stocksim-db --network stocksim-network -p 5432:5432 -e POSTGRES_PASSWORD=1999 -e POSTGRES_USER=postgres -e POSTGRES_DB=fastapi postgres:latest `

Then, the following addresses contain self-explanatory content: 

- http://localhost:30000/backend
- http://localhost:30001/backend/updatestockdata
- http://localhost:30002
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

