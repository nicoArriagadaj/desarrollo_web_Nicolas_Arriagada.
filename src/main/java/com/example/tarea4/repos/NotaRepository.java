package com.example.tarea4.repos;

import com.example.tarea4.models.*;
import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;

public interface NotaRepository extends JpaRepository<Nota, Integer> {
    List<Nota> findByActividad(Actividad actividad);
}