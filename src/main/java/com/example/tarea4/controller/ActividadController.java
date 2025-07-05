package com.example.tarea4.controller;

import com.example.tarea4.models.Actividad;
import com.example.tarea4.services.ActividadService;
import java.util.List;

import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;                 
import org.springframework.web.bind.annotation.*;

@Controller
@RequestMapping
public class ActividadController {

    private final ActividadService svc;
    public ActividadController(ActividadService s){ this.svc = s; }

    @ResponseBody
    @GetMapping("/api/actividades/finalizadas")
    public List<Actividad> finalizadas(){
        return svc.actividadesFinalizadas();
    }

    public record NotaDTO(Integer actividadId, Integer valor) {}
    public record NotaResp(double promedio, long total) {}

    @ResponseBody
    @PostMapping("/api/notas")
    public ResponseEntity<NotaResp> agregar(@RequestBody NotaDTO dto){
        if (dto.valor() == null || dto.valor() < 1 || dto.valor() > 7)
            return ResponseEntity.badRequest().build();

        var stats = svc.agregarNota(dto.actividadId(), dto.valor());
        return ResponseEntity.ok(new NotaResp(stats.promedio(), stats.total()));
    }


    @GetMapping({"/", "/web/actividades"})
    public String index(Model model){
        model.addAttribute("actividades", svc.actividadesFinalizadas());
        return "index";   
    }
}
