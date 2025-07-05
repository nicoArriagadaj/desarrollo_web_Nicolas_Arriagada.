package com.example.tarea4.services;

import com.example.tarea4.models.*;
import com.example.tarea4.repos.*;
import org.springframework.stereotype.Service;
import java.time.LocalDateTime;
import java.util.List;

@Service
public class ActividadService {

    private final ActividadRepository actRepo;
    private final NotaRepository notaRepo;

    public ActividadService(ActividadRepository a, NotaRepository n) {
        this.actRepo = a;
        this.notaRepo = n;
    }

    public List<Actividad> actividadesFinalizadas() {
        return actRepo.findByDiaHoraTerminoBefore(LocalDateTime.now());
    }

    public record NotaStats(double promedio, long total) {}

    public NotaStats agregarNota(int actividadId, int valor) {
        Actividad act = actRepo.findById(actividadId)
                               .orElseThrow(() -> new IllegalArgumentException("Actividad no existe"));

        notaRepo.save(new Nota(valor, act));

        List<Nota> notas = notaRepo.findByActividad(act);
        double promedio = notas.stream().mapToInt(Nota::getValor).average().orElse(0.0);
        long   total    = notas.size();
        return new NotaStats(promedio, total);
    }
}
