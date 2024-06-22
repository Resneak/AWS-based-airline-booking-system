package com.example.flightmanagementservice.service;

import com.example.flightmanagementservice.model.Flight;
import com.example.flightmanagementservice.repository.FlightRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class FlightService {

    @Autowired
    private FlightRepository flightRepository;

    public List<Flight> getAllFlights() {
        return flightRepository.findAll();
    }

    public Optional<Flight> getFlightById(Long id) {
        return flightRepository.findById(id);
    }

    public Flight createFlight(Flight flight) {
        return flightRepository.save(flight);
    }

    public Flight updateFlight(Long id, Flight flightDetails) {
        Flight flight = flightRepository.findById(id).orElseThrow(() -> new RuntimeException("Flight not found"));
        flight.setFlightNumber(flightDetails.getFlightNumber());
        flight.setDeparture(flightDetails.getDeparture());
        flight.setArrival(flightDetails.getArrival());
        flight.setTotalSeats(flightDetails.getTotalSeats());
        flight.setAvailableSeats(flightDetails.getAvailableSeats());
        return flightRepository.save(flight);
    }

    public void deleteFlight(Long id) {
        Flight flight = flightRepository.findById(id).orElseThrow(() -> new RuntimeException("Flight not found"));
        flightRepository.delete(flight);
    }
}
