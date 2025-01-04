FROM oraclelinux:9
WORKDIR /app
COPY . .
RUN dnf update
RUN dnf install java-21-openjdk-devel.aarch64
RUN dnf install python3.12.aarch64
RUN python3 -m ensurepip --upgrade
RUN python3 -m pip install fastapi[standard]
RUN chmod +x ./gradlew
RUN chmod +x ./fastapi-backend/backend.py
#Python must run first as the SpringBoot application requires its input to be able to generate a stock chart on request. 
CMD ["sh", "-c", "fastapi run ./fastapi-backend/backend.py & sleep 10 & ./gradlew bootRun & wait"]
EXPOSE 30000:8080
EXPOSE 30001:8000