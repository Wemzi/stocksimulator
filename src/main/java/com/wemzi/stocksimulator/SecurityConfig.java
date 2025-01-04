package com.wemzi.stocksimulator;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
@EnableWebSecurity
public class SecurityConfig {
    @Bean
    protected SecurityFilterChain filterChain(HttpSecurity http) throws Exception
    {
        http.authorizeHttpRequests().requestMatchers("/login").permitAll()
                .requestMatchers("/welcome").permitAll()
                .requestMatchers("/").permitAll()
                .requestMatchers("/backend").permitAll();
        return http.build();
    }
}