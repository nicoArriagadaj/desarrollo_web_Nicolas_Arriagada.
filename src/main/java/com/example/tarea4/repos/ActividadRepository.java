
package com.example.tarea4.repos;

import com.example.tarea4.models.Actividad;
import java.time.LocalDateTime;
import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ActividadRepository
       extends JpaRepository<Actividad, Integer> {


    List<Actividad> findByDiaHoraTerminoBefore(LocalDateTime fecha);
}
