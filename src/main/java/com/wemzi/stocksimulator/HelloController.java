package com.wemzi.stocksimulator;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HelloController {

    @GetMapping("/backend")
    public String index() {
        return "Greetings from Spring Boot!";
    }

}