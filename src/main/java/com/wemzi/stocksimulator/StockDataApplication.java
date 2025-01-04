package com.wemzi.stocksimulator;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.ComponentScan;

@SpringBootApplication
@ComponentScan(basePackages = "com.wemzi.stocksimulator")
public class StockDataApplication {

    public static void main(String[] args) {
        SpringApplication.run(StockDataApplication.class, args);
    }
}
