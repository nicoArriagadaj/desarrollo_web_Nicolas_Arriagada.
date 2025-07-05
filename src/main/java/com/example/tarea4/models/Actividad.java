package com.example.tarea4.models;

import jakarta.persistence.*;
import java.time.LocalDateTime;
import java.util.Set;

@Entity
@Table(name = "actividad")
public class Actividad {


    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(name = "comuna_id")
    private Integer comunaId;

    private String sector;
    private String nombre;
    private String email;
    private String celular;

    @Column(name = "dia_hora_inicio")
    private LocalDateTime diaHoraInicio;

    @Column(name = "dia_hora_termino")
    private LocalDateTime diaHoraTermino;

    private String descripcion;



    @OneToMany(mappedBy = "actividad", cascade = CascadeType.ALL)
    private Set<Nota> notas;

    @OneToMany(mappedBy = "actividad", cascade = CascadeType.ALL)
    private Set<ActividadTema> temas;

   
    public Integer getId()                 { return id; }
    public LocalDateTime getDiaHoraInicio(){ return diaHoraInicio; }
    public LocalDateTime getDiaHoraTermino(){ return diaHoraTermino; }
    public String getSector()              { return sector; }
    public String getNombre()              { return nombre; }
    public String getEmail()               { return email; }
    public String getCelular()             { return celular; }
    public String getDescripcion()         { return descripcion; }
    public Set<Nota> getNotas()            { return notas; }
    public Set<ActividadTema> getTemas()   { return temas; }
}
