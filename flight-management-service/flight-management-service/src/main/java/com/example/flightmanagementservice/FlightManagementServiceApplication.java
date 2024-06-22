package com.example.flightmanagementservice;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;

@SpringBootApplication(scanBasePackages = "com.example.flightmanagementservice")
@EnableJpaRepositories(basePackages = "com.example.flightmanagementservice.repository")
public class FlightManagementServiceApplication {
    public static void main(String[] args) {
        SpringApplication.run(FlightManagementServiceApplication.class, args);
    }
}
